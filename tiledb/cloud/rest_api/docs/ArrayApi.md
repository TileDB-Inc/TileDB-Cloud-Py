# tiledb.cloud.rest_api.ArrayApi

All URIs are relative to *http://localhost/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**array_activity_log**](ArrayApi.md#array_activity_log) | **GET** /arrays/{namespace}/{array}/activity | 
[**arrays_browser_owned_get**](ArrayApi.md#arrays_browser_owned_get) | **GET** /arrays/browser/owned | 
[**arrays_browser_owned_sidebar_get**](ArrayApi.md#arrays_browser_owned_sidebar_get) | **GET** /arrays/browser/owned/sidebar | 
[**arrays_browser_public_get**](ArrayApi.md#arrays_browser_public_get) | **GET** /arrays/browser/public | 
[**arrays_browser_public_sidebar_get**](ArrayApi.md#arrays_browser_public_sidebar_get) | **GET** /arrays/browser/public/sidebar | 
[**arrays_browser_shared_get**](ArrayApi.md#arrays_browser_shared_get) | **GET** /arrays/browser/shared | 
[**arrays_browser_shared_sidebar_get**](ArrayApi.md#arrays_browser_shared_sidebar_get) | **GET** /arrays/browser/shared/sidebar | 
[**arrays_namespace_array_end_timestamps_get**](ArrayApi.md#arrays_namespace_array_end_timestamps_get) | **GET** /arrays/{namespace}/{array}/end_timestamps | 
[**consolidate_array**](ArrayApi.md#consolidate_array) | **POST** /arrays/{namespace}/{array}/consolidate | 
[**create_array**](ArrayApi.md#create_array) | **POST** /arrays/{namespace}/{array} | 
[**delete_array**](ArrayApi.md#delete_array) | **DELETE** /arrays/{namespace}/{array} | 
[**deregister_array**](ArrayApi.md#deregister_array) | **DELETE** /arrays/{namespace}/{array}/deregister | 
[**get_activity_log_by_id**](ArrayApi.md#get_activity_log_by_id) | **GET** /arrays/{namespace}/{array}/activity/{id} | 
[**get_all_array_metadata**](ArrayApi.md#get_all_array_metadata) | **GET** /arrays | 
[**get_array**](ArrayApi.md#get_array) | **GET** /arrays/{namespace}/{array} | 
[**get_array_max_buffer_sizes**](ArrayApi.md#get_array_max_buffer_sizes) | **GET** /arrays/{namespace}/{array}/max_buffer_sizes | 
[**get_array_meta_data_json**](ArrayApi.md#get_array_meta_data_json) | **GET** /arrays/{namespace}/{array}/metadata_json | 
[**get_array_metadata**](ArrayApi.md#get_array_metadata) | **GET** /arrays/{namespace}/{array}/metadata | 
[**get_array_metadata_capnp**](ArrayApi.md#get_array_metadata_capnp) | **GET** /arrays/{namespace}/{array}/array_metadata | 
[**get_array_non_empty_domain**](ArrayApi.md#get_array_non_empty_domain) | **GET** /arrays/{namespace}/{array}/non_empty_domain | 
[**get_array_non_empty_domain_json**](ArrayApi.md#get_array_non_empty_domain_json) | **GET** /arrays/{namespace}/{array}/non_empty_domain_json | 
[**get_array_sample_data**](ArrayApi.md#get_array_sample_data) | **GET** /arrays/{namespace}/{array}/sample | 
[**get_array_sharing_policies**](ArrayApi.md#get_array_sharing_policies) | **GET** /arrays/{namespace}/{array}/share | 
[**get_arrays_in_namespace**](ArrayApi.md#get_arrays_in_namespace) | **GET** /arrays/{namespace} | 
[**get_fragment_end_timestamp**](ArrayApi.md#get_fragment_end_timestamp) | **GET** /arrays/{namespace}/{array}/fragment_end_timestamp | 
[**get_last_accessed_arrays**](ArrayApi.md#get_last_accessed_arrays) | **GET** /arrays/last_accessed | 
[**register_array**](ArrayApi.md#register_array) | **POST** /arrays/{namespace}/{array}/register | 
[**share_array**](ArrayApi.md#share_array) | **PATCH** /arrays/{namespace}/{array}/share | 
[**update_array_metadata**](ArrayApi.md#update_array_metadata) | **PATCH** /arrays/{namespace}/{array}/metadata | 
[**update_array_metadata_capnp**](ArrayApi.md#update_array_metadata_capnp) | **POST** /arrays/{namespace}/{array}/array_metadata | 
[**vacuum_array**](ArrayApi.md#vacuum_array) | **POST** /arrays/{namespace}/{array}/vacuum | 


# **array_activity_log**
> [ArrayActivityLog] array_activity_log(namespace, array)



get array activity logs

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.array_activity_log import ArrayActivityLog
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded
    start = 1 # int | Start time of window of fetch logs, unix epoch in seconds (default: seven days ago) (optional)
    end = 1 # int | End time of window of fetch logs, unix epoch in seconds (default: current utc timestamp) (optional)
    event_types = "event_types_example" # str | Event values can be one or more of the following read, write, create, delete, register, deregister, comma separated (optional)
    task_id = "task_id_example" # str | Array task ID To filter activity to (optional)
    has_task_id = True # bool | Excludes activity log results that do not contain an array task UUID (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.array_activity_log(namespace, array)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->array_activity_log: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.array_activity_log(namespace, array, start=start, end=end, event_types=event_types, task_id=task_id, has_task_id=has_task_id)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->array_activity_log: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |
 **start** | **int**| Start time of window of fetch logs, unix epoch in seconds (default: seven days ago) | [optional]
 **end** | **int**| End time of window of fetch logs, unix epoch in seconds (default: current utc timestamp) | [optional]
 **event_types** | **str**| Event values can be one or more of the following read, write, create, delete, register, deregister, comma separated | [optional]
 **task_id** | **str**| Array task ID To filter activity to | [optional]
 **has_task_id** | **bool**| Excludes activity log results that do not contain an array task UUID | [optional]

### Return type

[**[ArrayActivityLog]**](ArrayActivityLog.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | log of array activity |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **arrays_browser_owned_get**
> ArrayBrowserData arrays_browser_owned_get()



Fetch a list of all arrays that are owned directly by user or user's organizations

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.array_browser_data import ArrayBrowserData
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
    api_instance = array_api.ArrayApi(api_client)
    page = 1 # int | pagination offset (optional)
    per_page = 1 # int | pagination limit (optional)
    search = "search_example" # str | search string that will look at name, namespace or description fields (optional)
    namespace = "namespace_example" # str | namespace (optional)
    orderby = "orderby_example" # str | sort by which field valid values include last_accessed, size, name (optional)
    permissions = "permissions_example" # str | permissions valid values include read, read_write, write, admin (optional)
    tag = [
        "tag_example",
    ] # [str] | tag to search for, more than one can be included (optional)
    exclude_tag = [
        "exclude_tag_example",
    ] # [str] | tags to exclude matching array in results, more than one can be included (optional)
    file_type = [
        "file_type_example",
    ] # [str] | file_type to search for, more than one can be included (optional)
    exclude_file_type = [
        "exclude_file_type_example",
    ] # [str] | file_type to exclude matching array in results, more than one can be included (optional)
    file_property = [
        "file_property_example",
    ] # [str] | file_property key-value pair (comma separated, i.e. key,value) to search for, more than one can be included (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.arrays_browser_owned_get(page=page, per_page=per_page, search=search, namespace=namespace, orderby=orderby, permissions=permissions, tag=tag, exclude_tag=exclude_tag, file_type=file_type, exclude_file_type=exclude_file_type, file_property=file_property)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->arrays_browser_owned_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| pagination offset | [optional]
 **per_page** | **int**| pagination limit | [optional]
 **search** | **str**| search string that will look at name, namespace or description fields | [optional]
 **namespace** | **str**| namespace | [optional]
 **orderby** | **str**| sort by which field valid values include last_accessed, size, name | [optional]
 **permissions** | **str**| permissions valid values include read, read_write, write, admin | [optional]
 **tag** | **[str]**| tag to search for, more than one can be included | [optional]
 **exclude_tag** | **[str]**| tags to exclude matching array in results, more than one can be included | [optional]
 **file_type** | **[str]**| file_type to search for, more than one can be included | [optional]
 **exclude_file_type** | **[str]**| file_type to exclude matching array in results, more than one can be included | [optional]
 **file_property** | **[str]**| file_property key-value pair (comma separated, i.e. key,value) to search for, more than one can be included | [optional]

### Return type

[**ArrayBrowserData**](ArrayBrowserData.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Array of array info that are owned directly by user or user&#39;s organizations |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **arrays_browser_owned_sidebar_get**
> ArrayBrowserSidebar arrays_browser_owned_sidebar_get()



Fetch a sidebar for arrays that are owned directly by user or user's organizations

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.array_browser_sidebar import ArrayBrowserSidebar
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
    api_instance = array_api.ArrayApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        api_response = api_instance.arrays_browser_owned_sidebar_get()
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->arrays_browser_owned_sidebar_get: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**ArrayBrowserSidebar**](ArrayBrowserSidebar.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Array of array info that are owned directly by user or user&#39;s organizations |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **arrays_browser_public_get**
> ArrayBrowserData arrays_browser_public_get()



Fetch a list of all arrays that have been shared publically

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.array_browser_data import ArrayBrowserData
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
    api_instance = array_api.ArrayApi(api_client)
    page = 1 # int | pagination offset (optional)
    per_page = 1 # int | pagination limit (optional)
    search = "search_example" # str | search string that will look at name, namespace or description fields (optional)
    namespace = "namespace_example" # str | namespace (optional)
    orderby = "orderby_example" # str | sort by which field valid values include last_accessed, size, name (optional)
    permissions = "permissions_example" # str | permissions valid values include read, read_write, write, admin (optional)
    tag = [
        "tag_example",
    ] # [str] | tag to search for, more than one can be included (optional)
    exclude_tag = [
        "exclude_tag_example",
    ] # [str] | tags to exclude matching array in results, more than one can be included (optional)
    file_type = [
        "file_type_example",
    ] # [str] | file_type to search for, more than one can be included (optional)
    exclude_file_type = [
        "exclude_file_type_example",
    ] # [str] | file_type to exclude matching array in results, more than one can be included (optional)
    file_property = [
        "file_property_example",
    ] # [str] | file_property key-value pair (comma separated, i.e. key,value) to search for, more than one can be included (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.arrays_browser_public_get(page=page, per_page=per_page, search=search, namespace=namespace, orderby=orderby, permissions=permissions, tag=tag, exclude_tag=exclude_tag, file_type=file_type, exclude_file_type=exclude_file_type, file_property=file_property)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->arrays_browser_public_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| pagination offset | [optional]
 **per_page** | **int**| pagination limit | [optional]
 **search** | **str**| search string that will look at name, namespace or description fields | [optional]
 **namespace** | **str**| namespace | [optional]
 **orderby** | **str**| sort by which field valid values include last_accessed, size, name | [optional]
 **permissions** | **str**| permissions valid values include read, read_write, write, admin | [optional]
 **tag** | **[str]**| tag to search for, more than one can be included | [optional]
 **exclude_tag** | **[str]**| tags to exclude matching array in results, more than one can be included | [optional]
 **file_type** | **[str]**| file_type to search for, more than one can be included | [optional]
 **exclude_file_type** | **[str]**| file_type to exclude matching array in results, more than one can be included | [optional]
 **file_property** | **[str]**| file_property key-value pair (comma separated, i.e. key,value) to search for, more than one can be included | [optional]

### Return type

[**ArrayBrowserData**](ArrayBrowserData.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Array of array info that has been shared publically |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **arrays_browser_public_sidebar_get**
> ArrayBrowserSidebar arrays_browser_public_sidebar_get()



Fetch a sidebar of all arrays that have been shared publically

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.array_browser_sidebar import ArrayBrowserSidebar
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
    api_instance = array_api.ArrayApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        api_response = api_instance.arrays_browser_public_sidebar_get()
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->arrays_browser_public_sidebar_get: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**ArrayBrowserSidebar**](ArrayBrowserSidebar.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Array of array info that has been shared publically |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **arrays_browser_shared_get**
> ArrayBrowserData arrays_browser_shared_get()



Fetch a list of all arrays that have been shared with the user

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.array_browser_data import ArrayBrowserData
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
    api_instance = array_api.ArrayApi(api_client)
    page = 1 # int | pagination offset (optional)
    per_page = 1 # int | pagination limit (optional)
    search = "search_example" # str | search string that will look at name, namespace or description fields (optional)
    namespace = "namespace_example" # str | namespace (optional)
    orderby = "orderby_example" # str | sort by which field valid values include last_accessed, size, name (optional)
    permissions = "permissions_example" # str | permissions valid values include read, read_write, write, admin (optional)
    tag = [
        "tag_example",
    ] # [str] | tag to search for, more than one can be included (optional)
    exclude_tag = [
        "exclude_tag_example",
    ] # [str] | tags to exclude matching array in results, more than one can be included (optional)
    file_type = [
        "file_type_example",
    ] # [str] | file_type to search for, more than one can be included (optional)
    exclude_file_type = [
        "exclude_file_type_example",
    ] # [str] | file_type to exclude matching array in results, more than one can be included (optional)
    file_property = [
        "file_property_example",
    ] # [str] | file_property key-value pair (comma separated, i.e. key,value) to search for, more than one can be included (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.arrays_browser_shared_get(page=page, per_page=per_page, search=search, namespace=namespace, orderby=orderby, permissions=permissions, tag=tag, exclude_tag=exclude_tag, file_type=file_type, exclude_file_type=exclude_file_type, file_property=file_property)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->arrays_browser_shared_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| pagination offset | [optional]
 **per_page** | **int**| pagination limit | [optional]
 **search** | **str**| search string that will look at name, namespace or description fields | [optional]
 **namespace** | **str**| namespace | [optional]
 **orderby** | **str**| sort by which field valid values include last_accessed, size, name | [optional]
 **permissions** | **str**| permissions valid values include read, read_write, write, admin | [optional]
 **tag** | **[str]**| tag to search for, more than one can be included | [optional]
 **exclude_tag** | **[str]**| tags to exclude matching array in results, more than one can be included | [optional]
 **file_type** | **[str]**| file_type to search for, more than one can be included | [optional]
 **exclude_file_type** | **[str]**| file_type to exclude matching array in results, more than one can be included | [optional]
 **file_property** | **[str]**| file_property key-value pair (comma separated, i.e. key,value) to search for, more than one can be included | [optional]

### Return type

[**ArrayBrowserData**](ArrayBrowserData.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Array of array info that has been shared with the user |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **arrays_browser_shared_sidebar_get**
> ArrayBrowserSidebar arrays_browser_shared_sidebar_get()



Fetch a list of all arrays that have been shared with the user

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.array_browser_sidebar import ArrayBrowserSidebar
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
    api_instance = array_api.ArrayApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        api_response = api_instance.arrays_browser_shared_sidebar_get()
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->arrays_browser_shared_sidebar_get: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**ArrayBrowserSidebar**](ArrayBrowserSidebar.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Array of array info that has been shared with the user |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **arrays_namespace_array_end_timestamps_get**
> ArrayEndTimestampData arrays_namespace_array_end_timestamps_get(namespace, array)



retrieve a list of timestamps from the array fragment info listing in milliseconds, paginated

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.array_end_timestamp_data import ArrayEndTimestampData
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded
    page = 1 # int | pagination offset (optional)
    per_page = 1 # int | pagination limit (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.arrays_namespace_array_end_timestamps_get(namespace, array)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->arrays_namespace_array_end_timestamps_get: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.arrays_namespace_array_end_timestamps_get(namespace, array, page=page, per_page=per_page)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->arrays_namespace_array_end_timestamps_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |
 **page** | **int**| pagination offset | [optional]
 **per_page** | **int**| pagination limit | [optional]

### Return type

[**ArrayEndTimestampData**](ArrayEndTimestampData.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | list of timestamps in milliseconds, paginated |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **consolidate_array**
> consolidate_array(namespace, array, tiledb_config)



consolidate an array at a specified URI

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.tile_db_config import TileDBConfig
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded
    tiledb_config = TileDBConfig(
        configs={
            "key": "key_example",
        },
    ) # TileDBConfig | tiledb configuration

    # example passing only required values which don't have defaults set
    try:
        api_instance.consolidate_array(namespace, array, tiledb_config)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->consolidate_array: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |
 **tiledb_config** | [**TileDBConfig**](TileDBConfig.md)| tiledb configuration |

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
**204** | array consolidated successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_array**
> create_array(namespace, array, array_schema)



create a array schema at a specified URI registered to a group/project

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.array_schema import ArraySchema
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded
    array_schema = ArraySchema(
        uri="s3://<bucket>/test_array",
        version=[1, 3, 0],
        array_type=ArrayType("dense"),
        tile_order=Layout("row-major"),
        cell_order=Layout("row-major"),
        capacity=100000,
        coords_filter_pipeline=FilterPipeline(
            filters=[
                Filter(
                    type=FilterType("FILTER_NONE"),
                    data=FilterData(
                        int8=1,
                        uint8=1,
                        int16=1,
                        uint16=1,
                        int32=1,
                        uint32=1,
                        int64=1,
                        uint64=1,
                        float32=1,
                        float64=1,
                    ),
                ),
            ],
        ),
        offset_filter_pipeline=FilterPipeline(
            filters=[
                Filter(
                    type=FilterType("FILTER_NONE"),
                    data=FilterData(
                        int8=1,
                        uint8=1,
                        int16=1,
                        uint16=1,
                        int32=1,
                        uint32=1,
                        int64=1,
                        uint64=1,
                        float32=1,
                        float64=1,
                    ),
                ),
            ],
        ),
        domain=Domain(
            type=Datatype("INT32"),
            tile_order=Layout("row-major"),
            cell_order=Layout("row-major"),
            dimensions=[
                Dimension(
                    name="row",
                    type=Datatype("INT32"),
                    domain=DomainArray(
                        int8=[
                            1,
                        ],
                        uint8=[
                            1,
                        ],
                        int16=[
                            1,
                        ],
                        uint16=[
                            1,
                        ],
                        int32=[
                            1,
                        ],
                        uint32=[
                            1,
                        ],
                        int64=[
                            1,
                        ],
                        uint64=[
                            1,
                        ],
                        float32=[
                            3.14,
                        ],
                        float64=[
                            3.14,
                        ],
                    ),
                    null_tile_extent=True,
                    tile_extent=DimensionTileExtent(
                        int8=1,
                        uint8=1,
                        int16=1,
                        uint16=1,
                        int32=1,
                        uint32=1,
                        int64=1,
                        uint64=1,
                        float32=1,
                        float64=1,
                    ),
                    filter_pipeline=FilterPipeline(
                        filters=[
                            Filter(
                                type=FilterType("FILTER_NONE"),
                                data=FilterData(
                                    int8=1,
                                    uint8=1,
                                    int16=1,
                                    uint16=1,
                                    int32=1,
                                    uint32=1,
                                    int64=1,
                                    uint64=1,
                                    float32=1,
                                    float64=1,
                                ),
                            ),
                        ],
                    ),
                ),
            ],
        ),
        attributes=[
            Attribute(
                name="attribute1",
                type=Datatype("INT32"),
                filter_pipeline=FilterPipeline(
                    filters=[
                        Filter(
                            type=FilterType("FILTER_NONE"),
                            data=FilterData(
                                int8=1,
                                uint8=1,
                                int16=1,
                                uint16=1,
                                int32=1,
                                uint32=1,
                                int64=1,
                                uint64=1,
                                float32=1,
                                float64=1,
                            ),
                        ),
                    ],
                ),
                cell_val_num=1,
                nullable=True,
                fill_value=[
                    1,
                ],
            ),
        ],
        allows_duplicates=True,
    ) # ArraySchema | ArraySchema being created
    x_tiledb_cloud_access_credentials_name = "X-TILEDB-CLOUD-ACCESS-CREDENTIALS-NAME_example" # str | Optional registered access credentials to use for creation (optional)

    # example passing only required values which don't have defaults set
    try:
        api_instance.create_array(namespace, array, array_schema)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->create_array: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_instance.create_array(namespace, array, array_schema, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->create_array: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |
 **array_schema** | [**ArraySchema**](ArraySchema.md)| ArraySchema being created |
 **content_type** | **str**| Content Type of input and return mime | defaults to "application/json"
 **x_tiledb_cloud_access_credentials_name** | **str**| Optional registered access credentials to use for creation | [optional]

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
**204** | schema created successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_array**
> delete_array(namespace, array, )



delete a array

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_array(namespace, array, )
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->delete_array: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |
 **content_type** | **str**| Content Type of input and return mime | defaults to "application/json"

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
**204** | delete array successful |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deregister_array**
> deregister_array(namespace, array)



deregister a array

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded

    # example passing only required values which don't have defaults set
    try:
        api_instance.deregister_array(namespace, array)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->deregister_array: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |

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
**204** | deregistered array successful |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_activity_log_by_id**
> ArrayActivityLog get_activity_log_by_id(namespace, array, id)



get activity log by ID

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.array_activity_log import ArrayActivityLog
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded
    id = "id_example" # str | ID of the activity

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_activity_log_by_id(namespace, array, id)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->get_activity_log_by_id: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |
 **id** | **str**| ID of the activity |

### Return type

[**ArrayActivityLog**](ArrayActivityLog.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | array activity |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_array_metadata**
> [ArrayInfo] get_all_array_metadata()



get all array metadata user has access to

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.array_info import ArrayInfo
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
    api_instance = array_api.ArrayApi(api_client)
    public_share = "public_share_example" # str | Public share values can be one of exclude, only (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_all_array_metadata(public_share=public_share)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->get_all_array_metadata: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **public_share** | **str**| Public share values can be one of exclude, only | [optional]

### Return type

[**[ArrayInfo]**](ArrayInfo.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | array metadata for all arrays user has access to |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_array**
> ArraySchema get_array(namespace, array, )



get an ArraySchema using a url encoded uri

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.array_schema import ArraySchema
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_array(namespace, array, )
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->get_array: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |
 **content_type** | **str**| Content Type of input and return mime | defaults to "application/json"

### Return type

[**ArraySchema**](ArraySchema.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/capnp


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | get ArraySchema |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_array_max_buffer_sizes**
> MaxBufferSizes get_array_max_buffer_sizes(namespace, array, subarray, )



get the max buffer sizes of an array for a subarray

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.max_buffer_sizes import MaxBufferSizes
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded
    subarray = "subarray_example" # str | CSV string of subarray to get max buffer sizes for
    x_payer = "X-Payer_example" # str | Name of organization or user who should be charged for this request (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_array_max_buffer_sizes(namespace, array, subarray, )
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->get_array_max_buffer_sizes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_array_max_buffer_sizes(namespace, array, subarray, x_payer=x_payer)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->get_array_max_buffer_sizes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |
 **subarray** | **str**| CSV string of subarray to get max buffer sizes for |
 **content_type** | **str**| Content Type of input and return mime | defaults to "application/json"
 **x_payer** | **str**| Name of organization or user who should be charged for this request | [optional]

### Return type

[**MaxBufferSizes**](MaxBufferSizes.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | get the max buffer sizes of an array for a subarray |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_array_meta_data_json**
> bool, date, datetime, dict, float, int, list, str, none_type get_array_meta_data_json(namespace, array)



get metadata from the array in JSON format

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded
    length = 1 # int | (optional) limit character length of returned values (optional)
    end_timestamp = 1 # int | Milliseconds since Unix epoch, metadata will use open_at functionality to open array at the specific timestamp (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_array_meta_data_json(namespace, array)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->get_array_meta_data_json: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_array_meta_data_json(namespace, array, length=length, end_timestamp=end_timestamp)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->get_array_meta_data_json: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |
 **length** | **int**| (optional) limit character length of returned values | [optional]
 **end_timestamp** | **int**| Milliseconds since Unix epoch, metadata will use open_at functionality to open array at the specific timestamp | [optional]

### Return type

**bool, date, datetime, dict, float, int, list, str, none_type**

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | get array metadata |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_array_metadata**
> ArrayInfo get_array_metadata(namespace, array)



get metadata on an array

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.array_info import ArrayInfo
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_array_metadata(namespace, array)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->get_array_metadata: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |

### Return type

[**ArrayInfo**](ArrayInfo.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | array metadata for an array |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_array_metadata_capnp**
> ArrayMetadata get_array_metadata_capnp(namespace, array)



get metadata on an array

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.array_metadata import ArrayMetadata
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_array_metadata_capnp(namespace, array)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->get_array_metadata_capnp: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |

### Return type

[**ArrayMetadata**](ArrayMetadata.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/capnp


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | array metadata for an array |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_array_non_empty_domain**
> NonEmptyDomain get_array_non_empty_domain(namespace, array, )



get the non empty domain of an array

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.non_empty_domain import NonEmptyDomain
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded
    x_payer = "X-Payer_example" # str | Name of organization or user who should be charged for this request (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_array_non_empty_domain(namespace, array, )
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->get_array_non_empty_domain: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_array_non_empty_domain(namespace, array, x_payer=x_payer)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->get_array_non_empty_domain: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |
 **content_type** | **str**| Content Type of input and return mime | defaults to "application/json"
 **x_payer** | **str**| Name of organization or user who should be charged for this request | [optional]

### Return type

[**NonEmptyDomain**](NonEmptyDomain.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | get the non empty domain of an array |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_array_non_empty_domain_json**
> bool, date, datetime, dict, float, int, list, str, none_type get_array_non_empty_domain_json(namespace, array)



get non-empty domain from the array in json format

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_array_non_empty_domain_json(namespace, array)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->get_array_non_empty_domain_json: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |

### Return type

**bool, date, datetime, dict, float, int, list, str, none_type**

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | get array non-empty domaim |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_array_sample_data**
> ArraySample get_array_sample_data(namespace, array)



get an sample set of data from the array

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.array_sample import ArraySample
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded
    samples = 5.0 # float | Number of sample results to return (optional) if omitted the server will use the default value of 5.0

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_array_sample_data(namespace, array)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->get_array_sample_data: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_array_sample_data(namespace, array, samples=samples)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->get_array_sample_data: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |
 **samples** | **float**| Number of sample results to return | [optional] if omitted the server will use the default value of 5.0

### Return type

[**ArraySample**](ArraySample.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | get array sample data |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_array_sharing_policies**
> [ArraySharing] get_array_sharing_policies(namespace, array)



Get all sharing details of the array

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.array_sharing import ArraySharing
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_array_sharing_policies(namespace, array)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->get_array_sharing_policies: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |

### Return type

[**[ArraySharing]**](ArraySharing.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of all specific sharing policies |  -  |
**404** | Array does not exist or user does not have permissions to view array-sharing policies |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_arrays_in_namespace**
> [ArrayInfo] get_arrays_in_namespace(namespace)



get metadata on all arrays in a namespace

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.array_info import ArrayInfo
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_arrays_in_namespace(namespace)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->get_arrays_in_namespace: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |

### Return type

[**[ArrayInfo]**](ArrayInfo.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | array metadata for all arrays in a namespace |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_fragment_end_timestamp**
> int get_fragment_end_timestamp(namespace, array)



Get fragment end_timestamp on an array, will search for the closest end_timestamp to the timestamp asked

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded
    end_timestamp = 1 # int | Milliseconds since Unix epoch (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_fragment_end_timestamp(namespace, array)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->get_fragment_end_timestamp: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_fragment_end_timestamp(namespace, array, end_timestamp=end_timestamp)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->get_fragment_end_timestamp: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |
 **end_timestamp** | **int**| Milliseconds since Unix epoch | [optional]

### Return type

**int**

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | fragment end_timestamp on an array |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_last_accessed_arrays**
> [LastAccessedArray] get_last_accessed_arrays()



### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.last_accessed_array import LastAccessedArray
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
    api_instance = array_api.ArrayApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        api_response = api_instance.get_last_accessed_arrays()
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->get_last_accessed_arrays: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[LastAccessedArray]**](LastAccessedArray.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | gets last accessed arrays |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **register_array**
> ArrayInfo register_array(namespace, array, array_metadata)



register an array at a specified URI registered to the given namespace

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.array_info_update import ArrayInfoUpdate
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.array_info import ArrayInfo
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded
    array_metadata = ArrayInfoUpdate(
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
    ) # ArrayInfoUpdate | metadata associated with array

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.register_array(namespace, array, array_metadata)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->register_array: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |
 **array_metadata** | [**ArrayInfoUpdate**](ArrayInfoUpdate.md)| metadata associated with array |

### Return type

[**ArrayInfo**](ArrayInfo.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | array registered successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **share_array**
> share_array(namespace, array, array_sharing)



Share an array with a user

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.array_sharing import ArraySharing
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded
    array_sharing = ArraySharing(
        actions=[
            ArrayActions("[read, write]"),
        ],
        namespace="MyOrganization",
        namespace_type="organization",
    ) # ArraySharing | Namespace and list of permissions to share with. An empty list of permissions will remove the namespace; if permissions already exist they will be deleted then new ones added. In the event of a failure, the new policies will be rolled back to prevent partial policies, and it's likely the array will not be shared with the namespace at all.

    # example passing only required values which don't have defaults set
    try:
        api_instance.share_array(namespace, array, array_sharing)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->share_array: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |
 **array_sharing** | [**ArraySharing**](ArraySharing.md)| Namespace and list of permissions to share with. An empty list of permissions will remove the namespace; if permissions already exist they will be deleted then new ones added. In the event of a failure, the new policies will be rolled back to prevent partial policies, and it&#39;s likely the array will not be shared with the namespace at all. |

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
**204** | Array shared successfully |  -  |
**404** | Array does not exist or user does not have permissions to share array |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_array_metadata**
> update_array_metadata(namespace, array, array_metadata)



update metadata on an array

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded
    array_metadata = ArrayInfoUpdate(
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
    ) # ArrayInfoUpdate | array metadata to update

    # example passing only required values which don't have defaults set
    try:
        api_instance.update_array_metadata(namespace, array, array_metadata)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->update_array_metadata: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |
 **array_metadata** | [**ArrayInfoUpdate**](ArrayInfoUpdate.md)| array metadata to update |

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
**204** | array metadata updated successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_array_metadata_capnp**
> update_array_metadata_capnp(namespace, array, array_metadata_entries)



update metadata on an array

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.array_metadata import ArrayMetadata
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded
    array_metadata_entries = ArrayMetadata(
        entries=[
            ArrayMetadataEntry(
                key="key_example",
                type="type_example",
                value_num=1,
                value=[
                    1,
                ],
                _del=True,
            ),
        ],
    ) # ArrayMetadata | List of metadata entries

    # example passing only required values which don't have defaults set
    try:
        api_instance.update_array_metadata_capnp(namespace, array, array_metadata_entries)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->update_array_metadata_capnp: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |
 **array_metadata_entries** | [**ArrayMetadata**](ArrayMetadata.md)| List of metadata entries |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/capnp
 - **Accept**: application/json, application/capnp


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | array metadata updated successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **vacuum_array**
> vacuum_array(namespace, array, tiledb_config)



vacuum an array at a specified URI

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import array_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.tile_db_config import TileDBConfig
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
    api_instance = array_api.ArrayApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded
    tiledb_config = TileDBConfig(
        configs={
            "key": "key_example",
        },
    ) # TileDBConfig | tiledb configuration

    # example passing only required values which don't have defaults set
    try:
        api_instance.vacuum_array(namespace, array, tiledb_config)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling ArrayApi->vacuum_array: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |
 **tiledb_config** | [**TileDBConfig**](TileDBConfig.md)| tiledb configuration |

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
**204** | array vacuumed successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

