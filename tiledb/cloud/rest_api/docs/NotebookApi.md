# tiledb.cloud.rest_api.NotebookApi

All URIs are relative to *http://localhost/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_notebook_server_status**](NotebookApi.md#get_notebook_server_status) | **GET** /notebooks/server/{namespace}/status | 
[**handle_copy_notebook**](NotebookApi.md#handle_copy_notebook) | **POST** /notebooks/{namespace}/{array}/copy | 
[**handle_upload_notebook**](NotebookApi.md#handle_upload_notebook) | **POST** /notebooks/{namespace}/upload | 
[**shutdown_notebook_server**](NotebookApi.md#shutdown_notebook_server) | **DELETE** /notebooks/server/{namespace} | 
[**update_notebook_name**](NotebookApi.md#update_notebook_name) | **PATCH** /notebooks/{namespace}/{array}/rename | 


# **get_notebook_server_status**
> NotebookStatus get_notebook_server_status(namespace)



Get status of the notebook server

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import notebook_api
from tiledb.cloud.rest_api.model.notebook_status import NotebookStatus
from tiledb.cloud.rest_api.model.error import Error
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
    api_instance = notebook_api.NotebookApi(api_client)
    namespace = "namespace_example" # str | namespace notebook is in (an organization name or user's username)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_notebook_server_status(namespace)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling NotebookApi->get_notebook_server_status: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace notebook is in (an organization name or user&#39;s username) |

### Return type

[**NotebookStatus**](NotebookStatus.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | status of running notebook |  -  |
**202** | Notebook server is pending |  -  |
**402** | Payment required |  -  |
**404** | Notebook is not running |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **handle_copy_notebook**
> NotebookCopied handle_copy_notebook(namespace, array, notebook_copy)



Copy a tiledb notebook at the specified location

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import notebook_api
from tiledb.cloud.rest_api.model.notebook_copied import NotebookCopied
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.notebook_copy import NotebookCopy
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
    api_instance = notebook_api.NotebookApi(api_client)
    namespace = "namespace_example" # str | The namespace of the notebook
    array = "array_example" # str | The name of the notebook
    notebook_copy = NotebookCopy(
        output_uri="output_uri_example",
        name="name_example",
        namespace="namespace_example",
    ) # NotebookCopy | Input/Output information to create a new TileDB file
    x_tiledb_cloud_access_credentials_name = "X-TILEDB-CLOUD-ACCESS-CREDENTIALS-NAME_example" # str | Optional registered access credentials to use for creation (optional)
    end_timestamp = 1 # int | Milliseconds since Unix epoch, copy will use open_at functionality to copy notebook created at the specific timestamp (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.handle_copy_notebook(namespace, array, notebook_copy)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling NotebookApi->handle_copy_notebook: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.handle_copy_notebook(namespace, array, notebook_copy, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, end_timestamp=end_timestamp)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling NotebookApi->handle_copy_notebook: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| The namespace of the notebook |
 **array** | **str**| The name of the notebook |
 **notebook_copy** | [**NotebookCopy**](NotebookCopy.md)| Input/Output information to create a new TileDB file |
 **x_tiledb_cloud_access_credentials_name** | **str**| Optional registered access credentials to use for creation | [optional]
 **end_timestamp** | **int**| Milliseconds since Unix epoch, copy will use open_at functionality to copy notebook created at the specific timestamp | [optional]

### Return type

[**NotebookCopied**](NotebookCopied.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Notebook copied |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **handle_upload_notebook**
> FileUploaded handle_upload_notebook(namespace, input_file)



Upload a notebook at the specified location

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import notebook_api
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
    api_instance = notebook_api.NotebookApi(api_client)
    namespace = "namespace_example" # str | The namespace of the notebook
    input_file = open('/path/to/file', 'rb') # file_type | the notebook to upload
    x_tiledb_cloud_access_credentials_name = "X-TILEDB-CLOUD-ACCESS-CREDENTIALS-NAME_example" # str | Optional registered access credentials to use for creation (optional)
    output_uri = "output_uri_example" # str | output location of the TileDB File (optional)
    name = "name_example" # str | name to set for registered file (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.handle_upload_notebook(namespace, input_file)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling NotebookApi->handle_upload_notebook: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.handle_upload_notebook(namespace, input_file, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, output_uri=output_uri, name=name)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling NotebookApi->handle_upload_notebook: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| The namespace of the notebook |
 **input_file** | **file_type**| the notebook to upload |
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

# **shutdown_notebook_server**
> shutdown_notebook_server(namespace)



Shutdown a notebook server

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import notebook_api
from tiledb.cloud.rest_api.model.error import Error
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
    api_instance = notebook_api.NotebookApi(api_client)
    namespace = "namespace_example" # str | namespace notebook is in (an organization name or user's username)

    # example passing only required values which don't have defaults set
    try:
        api_instance.shutdown_notebook_server(namespace)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling NotebookApi->shutdown_notebook_server: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace notebook is in (an organization name or user&#39;s username) |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Notebook shutdown successfully |  -  |
**404** | Notebook is not running |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_notebook_name**
> update_notebook_name(namespace, array, notebook_metadata)



update name on a notebok, moving related S3 object to new location

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import notebook_api
from tiledb.cloud.rest_api.model.array_info_update import ArrayInfoUpdate
from tiledb.cloud.rest_api.model.error import Error
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
    api_instance = notebook_api.NotebookApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of notebook (array) that is url-encoded
    notebook_metadata = ArrayInfoUpdate(
        description="description_example",
        name="myarray1",
        uri="s3://bucket/array",
        file_type=FileType("notebook"),
        file_properties={
            "key": "key_example",
        },
        access_credentials_name="access_credentials_name_example",
        logo="logo_example",
        tags=[
            "tags_example",
        ],
        license_id="license_id_example",
        license_text="license_text_example",
        read_only=True,
    ) # ArrayInfoUpdate | notebook (array) metadata to update

    # example passing only required values which don't have defaults set
    try:
        api_instance.update_notebook_name(namespace, array, notebook_metadata)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling NotebookApi->update_notebook_name: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of notebook (array) that is url-encoded |
 **notebook_metadata** | [**ArrayInfoUpdate**](ArrayInfoUpdate.md)| notebook (array) metadata to update |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | notebook name updated successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

