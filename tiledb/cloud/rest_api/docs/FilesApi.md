# tiledb.cloud.rest_api.FilesApi

All URIs are relative to *http://localhost/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**handle_create_file**](FilesApi.md#handle_create_file) | **POST** /files/{namespace} | 
[**handle_export_file**](FilesApi.md#handle_export_file) | **POST** /files/{namespace}/{file}/export | 
[**handle_upload_file**](FilesApi.md#handle_upload_file) | **POST** /files/{namespace}/upload | 


# **handle_create_file**
> FileCreated handle_create_file(namespace, file_create)



Create a tiledb file at the specified location

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import files_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.file_created import FileCreated
from tiledb.cloud.rest_api.model.file_create import FileCreate
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = files_api.FilesApi(api_client)
    namespace = "namespace_example" # str | The namespace of the file
    file_create = FileCreate(
        input_uri="input_uri_example",
        output_uri="output_uri_example",
        name="name_example",
    ) # FileCreate | Input/Output information to create a new TileDB file
    x_tiledb_cloud_access_credentials_name = "X-TILEDB-CLOUD-ACCESS-CREDENTIALS-NAME_example" # str | Optional registered access credentials to use for creation (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.handle_create_file(namespace, file_create)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling FilesApi->handle_create_file: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.handle_create_file(namespace, file_create, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling FilesApi->handle_create_file: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| The namespace of the file |
 **file_create** | [**FileCreate**](FileCreate.md)| Input/Output information to create a new TileDB file |
 **x_tiledb_cloud_access_credentials_name** | **str**| Optional registered access credentials to use for creation | [optional]

### Return type

[**FileCreated**](FileCreated.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | File created |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **handle_export_file**
> FileExported handle_export_file(namespace, file, file_export)



Export a TileDB File back to its original file format

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import files_api
from tiledb.cloud.rest_api.model.file_export import FileExport
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.file_exported import FileExported
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = files_api.FilesApi(api_client)
    namespace = "namespace_example" # str | The namespace of the file
    file = "file_example" # str | The file identifier
    file_export = FileExport(
        output_uri="output_uri_example",
    ) # FileExport | Export configuration information

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.handle_export_file(namespace, file, file_export)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling FilesApi->handle_export_file: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| The namespace of the file |
 **file** | **str**| The file identifier |
 **file_export** | [**FileExport**](FileExport.md)| Export configuration information |

### Return type

[**FileExported**](FileExported.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | File exported |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **handle_upload_file**
> FileUploaded handle_upload_file(namespace, input_file)



Upload a tiledb file at the specified location

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import files_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.file_uploaded import FileUploaded
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = files_api.FilesApi(api_client)
    namespace = "namespace_example" # str | The namespace of the file
    input_file = open('/path/to/file', 'rb') # file_type | the file to upload
    x_tiledb_cloud_access_credentials_name = "X-TILEDB-CLOUD-ACCESS-CREDENTIALS-NAME_example" # str | Optional registered access credentials to use for creation (optional)
    output_uri = "output_uri_example" # str | output location of the TileDB File (optional)
    name = "name_example" # str | name to set for registered file (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.handle_upload_file(namespace, input_file)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling FilesApi->handle_upload_file: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.handle_upload_file(namespace, input_file, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, output_uri=output_uri, name=name)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling FilesApi->handle_upload_file: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| The namespace of the file |
 **input_file** | **file_type**| the file to upload |
 **x_tiledb_cloud_access_credentials_name** | **str**| Optional registered access credentials to use for creation | [optional]
 **output_uri** | **str**| output location of the TileDB File | [optional]
 **name** | **str**| name to set for registered file | [optional]

### Return type

[**FileUploaded**](FileUploaded.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | File uploaded |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

