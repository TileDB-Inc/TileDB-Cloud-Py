#!/bin/bash

set -euo pipefail

USAGE='
Usage:

    update_generated.sh /path/to/TileDB-Cloud-API-Spec/openapi-v1.yaml

This will create generated API documents in [repo root]/tiledb/cloud/rest_api.
'

if [[ "$#" -ne 1 ]]; then
  echo "$USAGE"
  exit 1
fi

ROOT="$(git rev-parse --show-toplevel)"

GENERATOR="$ROOT/.cache/openapi-generator-cli-4.3.1.jar"

if [[ ! -f "$GENERATOR" ]]; then
  mkdir -p "$ROOT/.cache"
  wget -O "$GENERATOR" "https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/4.3.1/openapi-generator-cli-4.3.1.jar"
fi

SPEC="$1"
TEMP_PACKAGE_NAME="zzz_replace_me_zzz"
PACKAGE_NAME="rest_api"

TARGET_PATH="$ROOT/tiledb/cloud"

TEMP_PATH="$(mktemp -d /tmp/api_gen.XXXXXX)"

################################################################################
# minimize output to what we want
cat <<EOF > ${TEMP_PATH}/.openapi-generator-ignore
docs/*
test/
test/*
git_push.sh
tox.ini
test-requirements.txt
setup.py
.gitignore
.travis.yml
EOF

################################################################################
# openapi-generator config
cat <<EOF > ${TEMP_PATH}/openapi_config-api
  {
  "projectName": "tiledb-cloud",
  "packageName": "${TEMP_PACKAGE_NAME}",
  "documentationPage": false,
  "generateSourceCodeOnly": true
  }
EOF

################################################################################
java -jar "$GENERATOR" \
  generate \
  -c "$TEMP_PATH/openapi_config-api" \
  -o "$TEMP_PATH" \
  -i "$SPEC" \
  -g python

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
sed --in-place -e "s/](rest_api\\//](/g" "${TEMP_PATH}/${TEMP_PACKAGE_NAME}_README.md"

# Get TARGET_PATH out of the way (if present).
if [ -e "$TARGET_PATH/$PACKAGE_NAME" ]; then
  rm -r -- "$TARGET_PATH/$PACKAGE_NAME"
fi

# move generated files to TARGET_PATH
cp -r "${TEMP_PATH}/${TEMP_PACKAGE_NAME}" "${TARGET_PATH}/${PACKAGE_NAME}"

cp ${TEMP_PATH}/${TEMP_PACKAGE_NAME}_README.md ${TARGET_PATH}/${PACKAGE_NAME}/README.md
cp ${TEMP_PATH}/.openapi-generator-ignore ${TARGET_PATH}/${PACKAGE_NAME}/
cp ${TEMP_PATH}/openapi_config-api ${TARGET_PATH}/${PACKAGE_NAME}/
cp -r ${TEMP_PATH}/.openapi-generator/ ${TARGET_PATH}/${PACKAGE_NAME}/

echo
echo "Output copied from '${TEMP_PATH}' to '${TARGET_PATH}/${PACKAGE_NAME}'"

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

# Apply an api_client patch to avoid descending into known–JSON-safe values.
git apply - <<EOF
diff --git a/tiledb/cloud/rest_api/api_client.py b/tiledb/cloud/rest_api/api_client.py
index 267385d..6d244a0 100644
--- a/tiledb/cloud/rest_api/api_client.py
+++ b/tiledb/cloud/rest_api/api_client.py
@@ -25,6 +25,7 @@ from dateutil.parser import parse
 from six.moves.urllib.parse import quote
 
 import tiledb.cloud.rest_api.models
+from tiledb.cloud._results import json_safe
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

