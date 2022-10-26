#!/usr/bin/env python

"""This program moves the ``basePath`` into each ``path``.

For example:

    basePath: "/some/dir"
    paths:
        /api_endpoint:
            get:
                tags: ["some_op"]

turns into:

    # basePath is deleted
    paths:
        /some/dir/api_endpoint:
            get:
                tags: ["some_op"]
            operationId: api_endpoint_get
"""

import os.path
import re
import sys
import tempfile
from typing import Any, Dict

import yaml


def rewrite_path(prefix: str, path: str) -> str:
    """Adds the prefix onto the API path object."""
    if not path.startswith("/"):
        return path
    return prefix + "/" + path.lstrip("/")


PUNCTUATION = re.compile(r"[/{}-]+")


def maybe_add_names(
    path: str, val: Dict[str, Dict[str, Any]]
) -> Dict[str, Dict[str, Any]]:
    """Adds operation IDs to API methods if not present.

    For API methods with no operation ID, the OpenAPI generator builds a
    function name from the path of the operation and its method. We don't want
    that to change just because we stuck a prefix on the path, so we calculate
    the method name that would have been generated without the prefix attached
    and set it as the operation ID.
    """
    old_name = "_".join(filter(None, PUNCTUATION.split(path))).lower()
    return {key: maybe_add_name(key, old_name, data) for key, data in val.items()}


def maybe_add_name(key: str, old_name: str, data: Any) -> Any:
    """Adds an ``operationId`` to the entry if needed."""
    if key not in ("get", "put", "post", "delete", "options", "head", "patch"):
        # Only modify HTTP operations.
        return data
    if data.get("operationId"):
        # If it already has a name that's good.
        return data
    updated = dict(data)
    updated["operationId"] = old_name + "_" + key
    return updated


def main():
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} some-openapi-spec.yaml", file=sys.stderr)
        print(
            "will print the location of a temporary rewritten YAML file",
            file=sys.stderr,
        )
        return 2

    input_filename = sys.argv[1]

    with open(input_filename) as infile:
        data: Dict[str, Any] = yaml.safe_load(infile)

    base_path = data.pop("basePath", "/").rstrip("/")
    data["paths"] = {
        rewrite_path(base_path, path): maybe_add_names(path, val)
        for path, val in data["paths"].items()
    }

    basename = os.path.basename(input_filename)
    output_filename = os.path.join(
        tempfile.mkdtemp(prefix="openapi-url-rewriter-"), basename
    )

    with open(output_filename, "w") as outfile:
        yaml.dump(data, stream=outfile, sort_keys=False)
    print(output_filename)


if __name__ == "__main__":
    sys.exit(main())
