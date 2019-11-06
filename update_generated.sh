#!/bin/sh

read -r -d '' USAGE <<'EOF'
Usage:

    gen.sh /path/to/TileDB-REST /path/to/output/[api]

Note: api is expected to exist under target path. For accurate file removal,
      the directory should be removed and re-created empty, before running this
      script.
EOF

if [[ -z "$1" || -z "$2" ]]; then
  echo "$USAGE"
  exit 1
fi

REST_SRC=$(realpath $1)
TARGET_PATH=$(realpath $2)

OUTPUT_PATH=$(mktemp -d /tmp/api_gen.XXXXXX)

PACKAGE_NAME="rest_api"

mkdir -p ${OUTPUT_PATH}/

################################################################################
# minimize output to what we want
cat <<EOF > ${OUTPUT_PATH}/.openapi-generator-ignore
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
cat <<EOF > ${OUTPUT_PATH}/openapi_config-api
  {
  "projectName": "tiledb-cloud",
  "packageName": "${PACKAGE_NAME}",
  "documentationPage": false,
  "generateSourceCodeOnly": true
  }
EOF

################################################################################
docker run --rm  \
  -v ${REST_SRC}/:/dc_src \
  -v ${OUTPUT_PATH}:/gen \
  openapitools/openapi-generator-cli:v4.1.3 generate \
    -c /gen/openapi_config-api -o /gen \
    -i /dc_src/openapi-v1.yaml -g python

# Needed because openapi generates everything as root user
sudo chown -R `whoami` ${OUTPUT_PATH}

# fix imports
find "${OUTPUT_PATH}" -iname "*.py" -exec sed -i '' -e "s/${PACKAGE_NAME}\./tiledb.cloud.${PACKAGE_NAME}./g" {} \;
# fix extra import in api_client
find "${OUTPUT_PATH}" -iname "api_client.py" -exec sed -i '' -e "s/from ${PACKAGE_NAME} import rest/from tiledb.cloud.${PACKAGE_NAME} import rest/g" {} \;

# move generated files to TARGET_PATH
cp -r ${OUTPUT_PATH}/${PACKAGE_NAME} ${TARGET_PATH}/

cp ${OUTPUT_PATH}/${PACKAGE_NAME}_README.md ${TARGET_PATH}/${PACKAGE_NAME}/README.md
# The newer openapi-generator-cli doesn't produce a requirements.txt
#cp ${OUTPUT_PATH}/requirements.txt ${TARGET_PATH}/${PACKAGE_NAME}
cp ${OUTPUT_PATH}/.openapi-generator-ignore ${TARGET_PATH}/${PACKAGE_NAME}/
cp ${OUTPUT_PATH}/openapi_config-api ${TARGET_PATH}/${PACKAGE_NAME}/
cp -r ${OUTPUT_PATH}/.openapi-generator/ ${TARGET_PATH}/${PACKAGE_NAME}/

echo
echo "Output copied from '${OUTPUT_PATH}' to '${TARGET_PATH}/${PACKAGE_NAME}'"

if ! [ -x "$(command -v black)" ]; then
  echo 'Warning: black python linter/formater is not installed. You must install black and run black to format generated files' >&2
else
  black .
fi
