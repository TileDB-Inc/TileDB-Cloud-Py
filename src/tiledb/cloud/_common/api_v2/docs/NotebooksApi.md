# tiledb.cloud._common.api_v2.NotebooksApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**handle_upload_notebook**](NotebooksApi.md#handle_upload_notebook) | **POST** /v2/notebooks/{namespace}/{array}/upload | 


# **handle_upload_notebook**
> NotebookUploaded handle_upload_notebook(namespace, array, filesize, notebook, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, name=name)



Upload a notebook at the specified location and wrap it in TileDB Array

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.NotebooksApi(api_client)
    namespace = 'namespace_example' # str | The namespace of the notebook
array = 'array_example' # str | name/uri of array that is url-encoded
filesize = 56 # int | size of the notebook to upload in bytes
notebook = '/path/to/file' # file | notebook to upload
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)
name = 'name_example' # str | name of the TileDB array to create, if missing {array} is used (optional)

    try:
        api_response = api_instance.handle_upload_notebook(namespace, array, filesize, notebook, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, name=name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling NotebooksApi->handle_upload_notebook: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.NotebooksApi(api_client)
    namespace = 'namespace_example' # str | The namespace of the notebook
array = 'array_example' # str | name/uri of array that is url-encoded
filesize = 56 # int | size of the notebook to upload in bytes
notebook = '/path/to/file' # file | notebook to upload
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)
name = 'name_example' # str | name of the TileDB array to create, if missing {array} is used (optional)

    try:
        api_response = api_instance.handle_upload_notebook(namespace, array, filesize, notebook, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, name=name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling NotebooksApi->handle_upload_notebook: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| The namespace of the notebook | 
 **array** | **str**| name/uri of array that is url-encoded | 
 **filesize** | **int**| size of the notebook to upload in bytes | 
 **notebook** | **file**| notebook to upload | 
 **x_tiledb_cloud_access_credentials_name** | **str**| Optional registered access credentials to use for creation | [optional] 
 **name** | **str**| name of the TileDB array to create, if missing {array} is used | [optional] 

### Return type

[**NotebookUploaded**](NotebookUploaded.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: application/octet-stream
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Notebook uploaded |  -  |
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

