# tiledb.cloud.rest_api.FilesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**handle_create_file**](FilesApi.md#handle_create_file) | **POST** /v1/files/{namespace} | 
[**handle_export_file**](FilesApi.md#handle_export_file) | **POST** /v1/files/{namespace}/{file}/export | 
[**handle_upload_file**](FilesApi.md#handle_upload_file) | **POST** /v1/files/{namespace}/upload | 


# **handle_create_file**
> FileCreated handle_create_file(namespace, file_create, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name)



Create a tiledb file at the specified location

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud.rest_api.FilesApi(api_client)
    namespace = 'namespace_example' # str | The namespace of the file
file_create = tiledb.cloud.rest_api.FileCreate() # FileCreate | Input/Output information to create a new TileDB file
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)

    try:
        api_response = api_instance.handle_create_file(namespace, file_create, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->handle_create_file: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud.rest_api.FilesApi(api_client)
    namespace = 'namespace_example' # str | The namespace of the file
file_create = tiledb.cloud.rest_api.FileCreate() # FileCreate | Input/Output information to create a new TileDB file
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)

    try:
        api_response = api_instance.handle_create_file(namespace, file_create, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name)
        pprint(api_response)
    except ApiException as e:
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
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **handle_export_file**
> FileExported handle_export_file(namespace, file, file_export)



Export a TileDB File back to its original file format

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud.rest_api.FilesApi(api_client)
    namespace = 'namespace_example' # str | The namespace of the file
file = 'file_example' # str | The file identifier
file_export = tiledb.cloud.rest_api.FileExport() # FileExport | Export configuration information

    try:
        api_response = api_instance.handle_export_file(namespace, file, file_export)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->handle_export_file: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud.rest_api.FilesApi(api_client)
    namespace = 'namespace_example' # str | The namespace of the file
file = 'file_example' # str | The file identifier
file_export = tiledb.cloud.rest_api.FileExport() # FileExport | Export configuration information

    try:
        api_response = api_instance.handle_export_file(namespace, file, file_export)
        pprint(api_response)
    except ApiException as e:
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
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **handle_upload_file**
> FileUploaded handle_upload_file(namespace, input_file, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, output_uri=output_uri, name=name)



Upload a tiledb file at the specified location

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud.rest_api.FilesApi(api_client)
    namespace = 'namespace_example' # str | The namespace of the file
input_file = '/path/to/file' # file | the file to upload
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)
output_uri = 'output_uri_example' # str | output location of the TileDB File (optional)
name = 'name_example' # str | name to set for registered file (optional)

    try:
        api_response = api_instance.handle_upload_file(namespace, input_file, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, output_uri=output_uri, name=name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->handle_upload_file: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud.rest_api.FilesApi(api_client)
    namespace = 'namespace_example' # str | The namespace of the file
input_file = '/path/to/file' # file | the file to upload
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)
output_uri = 'output_uri_example' # str | output location of the TileDB File (optional)
name = 'name_example' # str | name to set for registered file (optional)

    try:
        api_response = api_instance.handle_upload_file(namespace, input_file, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, output_uri=output_uri, name=name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->handle_upload_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| The namespace of the file | 
 **input_file** | **file**| the file to upload | 
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
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

