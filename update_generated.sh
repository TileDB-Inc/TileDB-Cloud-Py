#!/bin/bash

set -euo pipefail

USAGE='
Usage:

    update_generated.sh /path/to/TileDB-Cloud-API-Spec

This creates generated API documents in [repo root]/src/tiledb/cloud/rest_api.
'

if [[ "$#" -ne 1 ]]; then
  echo "$USAGE"
  exit 1
fi

ROOT="$(git rev-parse --show-toplevel)"
GENERATOR="$ROOT/.cache/openapi-generator-cli-4.3.1.jar"
TEMP_PACKAGE_NAME="zzz_replace_me_zzz"

OPENAPI_GENERATOR_IGNORE='
docs/*
test/
test/*
git_push.sh
tox.ini
test-requirements.txt
setup.py
.gitignore
.travis.yml
'

OPENAPI_GENERATOR_CONFIG='
{
  "projectName": "tiledb-cloud",
  "packageName": "'"${TEMP_PACKAGE_NAME}"'",
  "documentationPage": false,
  "generateSourceCodeOnly": true
}
'

download_generator() {
  if [[ ! -f "$GENERATOR" ]]; then
    mkdir -p "$ROOT/.cache"
    wget -O "$GENERATOR" "https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/4.3.1/openapi-generator-cli-4.3.1.jar"
  fi
}

generate_api() {
  RAW_SPEC="$1"
  PACKAGE_NAME="$2"
  PACKAGE_NAME_SLASHY="${PACKAGE_NAME//.//}"

  TARGET_PATH="$ROOT/src/tiledb/cloud"

  TEMP_PATH="$(mktemp -d /tmp/api_gen.XXXXXX)"

  SPEC="$("$ROOT/generator/rewrite_urls.py" "$RAW_SPEC")"

  ################################################################################
  # minimize output to what we want
  echo "$OPENAPI_GENERATOR_IGNORE" > ${TEMP_PATH}/.openapi-generator-ignore

  ################################################################################
  # openapi-generator config
  echo "$OPENAPI_GENERATOR_CONFIG" > ${TEMP_PATH}/openapi_config-api

  ################################################################################
  java -jar "$GENERATOR" \
    generate \
    -c "$TEMP_PATH/openapi_config-api" \
    -o "$TEMP_PATH" \
    -i "$SPEC" \
    -g python \
    --skip-validate-spec  # The generator doesn't like the v2 spec.

  # Rewrite imports and links in docs,
  # and work around https://github.com/OpenAPITools/openapi-generator/issues/10236
  find "${TEMP_PATH}" \
    -type f \
    -execdir \
      sed --in-place \
        -e "s/${TEMP_PACKAGE_NAME}\./tiledb.cloud.${PACKAGE_NAME}./g" \
        -e "s/\\(from\\|import\\) ${TEMP_PACKAGE_NAME}/\\1 tiledb.cloud.${PACKAGE_NAME}/g" \
        -e "s/${TEMP_PACKAGE_NAME}/${PACKAGE_NAME}/g" \
        -e "s/ del =/ _del =/g" \
        '{}' \
    '+'

  # Fix up links in README.
  sed --in-place -e "s/](${PACKAGE_NAME}\\//](/g" "${TEMP_PATH}/${TEMP_PACKAGE_NAME}_README.md"

  # Get TARGET_PATH out of the way (if present).
  if [ -e "$TARGET_PATH/$PACKAGE_NAME_SLASHY" ]; then
    rm -r -- "$TARGET_PATH/$PACKAGE_NAME_SLASHY"
  fi

  # move generated files to TARGET_PATH
  cp -r "${TEMP_PATH}/${TEMP_PACKAGE_NAME}" "${TARGET_PATH}/${PACKAGE_NAME_SLASHY}"

  cp ${TEMP_PATH}/${TEMP_PACKAGE_NAME}_README.md ${TARGET_PATH}/${PACKAGE_NAME_SLASHY}/README.md
  cp ${TEMP_PATH}/.openapi-generator-ignore ${TARGET_PATH}/${PACKAGE_NAME_SLASHY}/
  cp ${TEMP_PATH}/openapi_config-api ${TARGET_PATH}/${PACKAGE_NAME_SLASHY}/
  cp -r ${TEMP_PATH}/.openapi-generator/ ${TARGET_PATH}/${PACKAGE_NAME_SLASHY}/

  echo
  echo "Output copied from '${TEMP_PATH}' to '${TARGET_PATH}/${PACKAGE_NAME_SLASHY}'"
}

run_format() {
  for command in isort black; do
    if ! [[ -x "$(command -v "${command}")" ]]; then
      echo "${command} is not installed." >&2
      echo 'Before sending a review request, run:' >&2
      echo "  $ pip install ${command}" >&2
      echo "  $ ${command} ${ROOT}" >&2
      echo 'to ensure your files are correctly formatted.' >&2
    else
      "${command}" "${ROOT}"
    fi
  done
}

# Apply an api_client patch to avoid descending into known–JSON-safe values.
apply_json_safe_patch() {
  git apply - <<EOF
diff --git a/src/tiledb/cloud/rest_api/api_client.py b/src/tiledb/cloud/rest_api/api_client.py
index 267385d..6d244a0 100644
--- a/src/tiledb/cloud/rest_api/api_client.py
+++ b/src/tiledb/cloud/rest_api/api_client.py
@@ -25,6 +25,7 @@ from dateutil.parser import parse
 from six.moves.urllib.parse import quote

 import tiledb.cloud.rest_api.models
+from tiledb.cloud._common import json_safe
 from tiledb.cloud.rest_api import rest
 from tiledb.cloud.rest_api.configuration import Configuration
 from tiledb.cloud.rest_api.exceptions import ApiException
@@ -251,6 +252,8 @@ class ApiClient(object):
         """
         if obj is None:
             return None
+        elif isinstance(obj, json_safe.Value):
+            return obj.value
         elif isinstance(obj, self.PRIMITIVE_TYPES):
             return obj
         elif isinstance(obj, list):
EOF
}

ABSPATH="$(realpath "$1")"

download_generator
generate_api "${ABSPATH%/}/openapi-v1.yaml" rest_api
generate_api "${ABSPATH%/}/openapi-v2.yaml" _common.api_v2
run_format
apply_json_safe_patch
cp "$ROOT/generator/openapi_overrides"/* "$TARGET_PATH/_common/api_v2"
