# rest_api.ArrayApi

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
[**consolidate_array**](ArrayApi.md#consolidate_array) | **POST** /arrays/{namespace}/{array}/consolidate | 
[**create_array**](ArrayApi.md#create_array) | **POST** /arrays/{namespace}/{array} | 
[**delete_array**](ArrayApi.md#delete_array) | **DELETE** /arrays/{namespace}/{array} | 
[**deregister_array**](ArrayApi.md#deregister_array) | **DELETE** /arrays/{namespace}/{array}/deregister | 
[**get_all_array_metadata**](ArrayApi.md#get_all_array_metadata) | **GET** /arrays | 
[**get_array**](ArrayApi.md#get_array) | **GET** /arrays/{namespace}/{array} | 
[**get_array_max_buffer_sizes**](ArrayApi.md#get_array_max_buffer_sizes) | **GET** /arrays/{namespace}/{array}/max_buffer_sizes | 
[**get_array_meta_data_json**](ArrayApi.md#get_array_meta_data_json) | **GET** /arrays/{namespace}/{array}/metadata_json | 
[**get_array_metadata**](ArrayApi.md#get_array_metadata) | **GET** /arrays/{namespace}/{array}/metadata | 
[**get_array_non_empty_domain**](ArrayApi.md#get_array_non_empty_domain) | **GET** /arrays/{namespace}/{array}/non_empty_domain | 
[**get_array_sample_data**](ArrayApi.md#get_array_sample_data) | **GET** /arrays/{namespace}/{array}/sample | 
[**get_array_sharing_policies**](ArrayApi.md#get_array_sharing_policies) | **GET** /arrays/{namespace}/{array}/share | 
[**get_arrays_in_namespace**](ArrayApi.md#get_arrays_in_namespace) | **GET** /arrays/{namespace} | 
[**get_last_accessed_arrays**](ArrayApi.md#get_last_accessed_arrays) | **GET** /arrays/last_accessed | 
[**register_array**](ArrayApi.md#register_array) | **POST** /arrays/{namespace}/{array}/register | 
[**share_array**](ArrayApi.md#share_array) | **PATCH** /arrays/{namespace}/{array}/share | 
[**update_array_metadata**](ArrayApi.md#update_array_metadata) | **PATCH** /arrays/{namespace}/{array}/metadata | 
[**vacuum_array**](ArrayApi.md#vacuum_array) | **POST** /arrays/{namespace}/{array}/vacuum | 


# **array_activity_log**
> list[ArrayActivityLog] array_activity_log(namespace, array, start=start, end=end, event_types=event_types, task_id=task_id)



get array activity logs

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
start = 56 # int | Start time of window of fetch logs, unix epoch in seconds (default: seven days ago) (optional)
end = 56 # int | End time of window of fetch logs, unix epoch in seconds (default: current utc timestamp) (optional)
event_types = 'event_types_example' # str | Event values can be one or more of the following read, write, create, delete, register, deregister, comma separated (optional)
task_id = 'task_id_example' # str | Array task id To filter activity to (optional)

    try:
        api_response = api_instance.array_activity_log(namespace, array, start=start, end=end, event_types=event_types, task_id=task_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->array_activity_log: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
start = 56 # int | Start time of window of fetch logs, unix epoch in seconds (default: seven days ago) (optional)
end = 56 # int | End time of window of fetch logs, unix epoch in seconds (default: current utc timestamp) (optional)
event_types = 'event_types_example' # str | Event values can be one or more of the following read, write, create, delete, register, deregister, comma separated (optional)
task_id = 'task_id_example' # str | Array task id To filter activity to (optional)

    try:
        api_response = api_instance.array_activity_log(namespace, array, start=start, end=end, event_types=event_types, task_id=task_id)
        pprint(api_response)
    except ApiException as e:
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
 **task_id** | **str**| Array task id To filter activity to | [optional] 

### Return type

[**list[ArrayActivityLog]**](ArrayActivityLog.md)

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
> ArrayBrowserData arrays_browser_owned_get(page=page, per_page=per_page, search=search, namespace=namespace, orderby=orderby, permissions=permissions, tag=tag, exclude_tag=exclude_tag, file_type=file_type, exclude_file_type=exclude_file_type)



Fetch a list of all arrays that are owned directly by user or user's organizations

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
search = 'search_example' # str | search string that will look at name, namespace or description fields (optional)
namespace = 'namespace_example' # str | namespace (optional)
orderby = 'orderby_example' # str | sort by which field valid values include last_accessed, size, name (optional)
permissions = 'permissions_example' # str | permissions valid values include read, read_write, write, admin (optional)
tag = ['tag_example'] # list[str] | tag to search for, more than one can be included (optional)
exclude_tag = ['exclude_tag_example'] # list[str] | tags to exclude matching array in results, more than one can be included (optional)
file_type = ['file_type_example'] # list[str] | file_type to search for, more than one can be included (optional)
exclude_file_type = ['exclude_file_type_example'] # list[str] | file_type to exclude matching array in results, more than one can be included (optional)

    try:
        api_response = api_instance.arrays_browser_owned_get(page=page, per_page=per_page, search=search, namespace=namespace, orderby=orderby, permissions=permissions, tag=tag, exclude_tag=exclude_tag, file_type=file_type, exclude_file_type=exclude_file_type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->arrays_browser_owned_get: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
search = 'search_example' # str | search string that will look at name, namespace or description fields (optional)
namespace = 'namespace_example' # str | namespace (optional)
orderby = 'orderby_example' # str | sort by which field valid values include last_accessed, size, name (optional)
permissions = 'permissions_example' # str | permissions valid values include read, read_write, write, admin (optional)
tag = ['tag_example'] # list[str] | tag to search for, more than one can be included (optional)
exclude_tag = ['exclude_tag_example'] # list[str] | tags to exclude matching array in results, more than one can be included (optional)
file_type = ['file_type_example'] # list[str] | file_type to search for, more than one can be included (optional)
exclude_file_type = ['exclude_file_type_example'] # list[str] | file_type to exclude matching array in results, more than one can be included (optional)

    try:
        api_response = api_instance.arrays_browser_owned_get(page=page, per_page=per_page, search=search, namespace=namespace, orderby=orderby, permissions=permissions, tag=tag, exclude_tag=exclude_tag, file_type=file_type, exclude_file_type=exclude_file_type)
        pprint(api_response)
    except ApiException as e:
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
 **tag** | [**list[str]**](str.md)| tag to search for, more than one can be included | [optional] 
 **exclude_tag** | [**list[str]**](str.md)| tags to exclude matching array in results, more than one can be included | [optional] 
 **file_type** | [**list[str]**](str.md)| file_type to search for, more than one can be included | [optional] 
 **exclude_file_type** | [**list[str]**](str.md)| file_type to exclude matching array in results, more than one can be included | [optional] 

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
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    
    try:
        api_response = api_instance.arrays_browser_owned_sidebar_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->arrays_browser_owned_sidebar_get: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    
    try:
        api_response = api_instance.arrays_browser_owned_sidebar_get()
        pprint(api_response)
    except ApiException as e:
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
> ArrayBrowserData arrays_browser_public_get(page=page, per_page=per_page, search=search, namespace=namespace, orderby=orderby, permissions=permissions, tag=tag, exclude_tag=exclude_tag, file_type=file_type, exclude_file_type=exclude_file_type)



Fetch a list of all arrays that have been shared publically

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
search = 'search_example' # str | search string that will look at name, namespace or description fields (optional)
namespace = 'namespace_example' # str | namespace (optional)
orderby = 'orderby_example' # str | sort by which field valid values include last_accessed, size, name (optional)
permissions = 'permissions_example' # str | permissions valid values include read, read_write, write, admin (optional)
tag = ['tag_example'] # list[str] | tag to search for, more than one can be included (optional)
exclude_tag = ['exclude_tag_example'] # list[str] | tags to exclude matching array in results, more than one can be included (optional)
file_type = ['file_type_example'] # list[str] | file_type to search for, more than one can be included (optional)
exclude_file_type = ['exclude_file_type_example'] # list[str] | file_type to exclude matching array in results, more than one can be included (optional)

    try:
        api_response = api_instance.arrays_browser_public_get(page=page, per_page=per_page, search=search, namespace=namespace, orderby=orderby, permissions=permissions, tag=tag, exclude_tag=exclude_tag, file_type=file_type, exclude_file_type=exclude_file_type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->arrays_browser_public_get: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
search = 'search_example' # str | search string that will look at name, namespace or description fields (optional)
namespace = 'namespace_example' # str | namespace (optional)
orderby = 'orderby_example' # str | sort by which field valid values include last_accessed, size, name (optional)
permissions = 'permissions_example' # str | permissions valid values include read, read_write, write, admin (optional)
tag = ['tag_example'] # list[str] | tag to search for, more than one can be included (optional)
exclude_tag = ['exclude_tag_example'] # list[str] | tags to exclude matching array in results, more than one can be included (optional)
file_type = ['file_type_example'] # list[str] | file_type to search for, more than one can be included (optional)
exclude_file_type = ['exclude_file_type_example'] # list[str] | file_type to exclude matching array in results, more than one can be included (optional)

    try:
        api_response = api_instance.arrays_browser_public_get(page=page, per_page=per_page, search=search, namespace=namespace, orderby=orderby, permissions=permissions, tag=tag, exclude_tag=exclude_tag, file_type=file_type, exclude_file_type=exclude_file_type)
        pprint(api_response)
    except ApiException as e:
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
 **tag** | [**list[str]**](str.md)| tag to search for, more than one can be included | [optional] 
 **exclude_tag** | [**list[str]**](str.md)| tags to exclude matching array in results, more than one can be included | [optional] 
 **file_type** | [**list[str]**](str.md)| file_type to search for, more than one can be included | [optional] 
 **exclude_file_type** | [**list[str]**](str.md)| file_type to exclude matching array in results, more than one can be included | [optional] 

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
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    
    try:
        api_response = api_instance.arrays_browser_public_sidebar_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->arrays_browser_public_sidebar_get: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    
    try:
        api_response = api_instance.arrays_browser_public_sidebar_get()
        pprint(api_response)
    except ApiException as e:
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
> ArrayBrowserData arrays_browser_shared_get(page=page, per_page=per_page, search=search, namespace=namespace, orderby=orderby, permissions=permissions, tag=tag, exclude_tag=exclude_tag, file_type=file_type, exclude_file_type=exclude_file_type)



Fetch a list of all arrays that have been shared with the user

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
search = 'search_example' # str | search string that will look at name, namespace or description fields (optional)
namespace = 'namespace_example' # str | namespace (optional)
orderby = 'orderby_example' # str | sort by which field valid values include last_accessed, size, name (optional)
permissions = 'permissions_example' # str | permissions valid values include read, read_write, write, admin (optional)
tag = ['tag_example'] # list[str] | tag to search for, more than one can be included (optional)
exclude_tag = ['exclude_tag_example'] # list[str] | tags to exclude matching array in results, more than one can be included (optional)
file_type = ['file_type_example'] # list[str] | file_type to search for, more than one can be included (optional)
exclude_file_type = ['exclude_file_type_example'] # list[str] | file_type to exclude matching array in results, more than one can be included (optional)

    try:
        api_response = api_instance.arrays_browser_shared_get(page=page, per_page=per_page, search=search, namespace=namespace, orderby=orderby, permissions=permissions, tag=tag, exclude_tag=exclude_tag, file_type=file_type, exclude_file_type=exclude_file_type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->arrays_browser_shared_get: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
search = 'search_example' # str | search string that will look at name, namespace or description fields (optional)
namespace = 'namespace_example' # str | namespace (optional)
orderby = 'orderby_example' # str | sort by which field valid values include last_accessed, size, name (optional)
permissions = 'permissions_example' # str | permissions valid values include read, read_write, write, admin (optional)
tag = ['tag_example'] # list[str] | tag to search for, more than one can be included (optional)
exclude_tag = ['exclude_tag_example'] # list[str] | tags to exclude matching array in results, more than one can be included (optional)
file_type = ['file_type_example'] # list[str] | file_type to search for, more than one can be included (optional)
exclude_file_type = ['exclude_file_type_example'] # list[str] | file_type to exclude matching array in results, more than one can be included (optional)

    try:
        api_response = api_instance.arrays_browser_shared_get(page=page, per_page=per_page, search=search, namespace=namespace, orderby=orderby, permissions=permissions, tag=tag, exclude_tag=exclude_tag, file_type=file_type, exclude_file_type=exclude_file_type)
        pprint(api_response)
    except ApiException as e:
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
 **tag** | [**list[str]**](str.md)| tag to search for, more than one can be included | [optional] 
 **exclude_tag** | [**list[str]**](str.md)| tags to exclude matching array in results, more than one can be included | [optional] 
 **file_type** | [**list[str]**](str.md)| file_type to search for, more than one can be included | [optional] 
 **exclude_file_type** | [**list[str]**](str.md)| file_type to exclude matching array in results, more than one can be included | [optional] 

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
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    
    try:
        api_response = api_instance.arrays_browser_shared_sidebar_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->arrays_browser_shared_sidebar_get: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    
    try:
        api_response = api_instance.arrays_browser_shared_sidebar_get()
        pprint(api_response)
    except ApiException as e:
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

# **consolidate_array**
> consolidate_array(namespace, array, tiledb_config)



consolidate an array at a specified URI

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
tiledb_config = rest_api.TileDBConfig() # TileDBConfig | tiledb configuration

    try:
        api_instance.consolidate_array(namespace, array, tiledb_config)
    except ApiException as e:
        print("Exception when calling ArrayApi->consolidate_array: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
tiledb_config = rest_api.TileDBConfig() # TileDBConfig | tiledb configuration

    try:
        api_instance.consolidate_array(namespace, array, tiledb_config)
    except ApiException as e:
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
> create_array(namespace, array, content_type, array_schema)



create a array schema at a specified URI registered to a group/project

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
content_type = 'application/json' # str | Content Type of input and return mime (default to 'application/json')
array_schema = rest_api.ArraySchema() # ArraySchema | ArraySchema being created

    try:
        api_instance.create_array(namespace, array, content_type, array_schema)
    except ApiException as e:
        print("Exception when calling ArrayApi->create_array: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
content_type = 'application/json' # str | Content Type of input and return mime (default to 'application/json')
array_schema = rest_api.ArraySchema() # ArraySchema | ArraySchema being created

    try:
        api_instance.create_array(namespace, array, content_type, array_schema)
    except ApiException as e:
        print("Exception when calling ArrayApi->create_array: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **array** | **str**| name/uri of array that is url-encoded | 
 **content_type** | **str**| Content Type of input and return mime | [default to &#39;application/json&#39;]
 **array_schema** | [**ArraySchema**](ArraySchema.md)| ArraySchema being created | 

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
> delete_array(namespace, array, content_type)



delete a array

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
content_type = 'application/json' # str | Content Type of input and return mime (default to 'application/json')

    try:
        api_instance.delete_array(namespace, array, content_type)
    except ApiException as e:
        print("Exception when calling ArrayApi->delete_array: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
content_type = 'application/json' # str | Content Type of input and return mime (default to 'application/json')

    try:
        api_instance.delete_array(namespace, array, content_type)
    except ApiException as e:
        print("Exception when calling ArrayApi->delete_array: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **array** | **str**| name/uri of array that is url-encoded | 
 **content_type** | **str**| Content Type of input and return mime | [default to &#39;application/json&#39;]

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
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded

    try:
        api_instance.deregister_array(namespace, array)
    except ApiException as e:
        print("Exception when calling ArrayApi->deregister_array: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded

    try:
        api_instance.deregister_array(namespace, array)
    except ApiException as e:
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

# **get_all_array_metadata**
> list[ArrayInfo] get_all_array_metadata(public_share=public_share)



get all array metadata user has access to

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    public_share = 'public_share_example' # str | Public share values can be one of exclude, only (optional)

    try:
        api_response = api_instance.get_all_array_metadata(public_share=public_share)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->get_all_array_metadata: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    public_share = 'public_share_example' # str | Public share values can be one of exclude, only (optional)

    try:
        api_response = api_instance.get_all_array_metadata(public_share=public_share)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->get_all_array_metadata: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **public_share** | **str**| Public share values can be one of exclude, only | [optional] 

### Return type

[**list[ArrayInfo]**](ArrayInfo.md)

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
> ArraySchema get_array(namespace, array, content_type)



get an ArraySchema using a url encoded uri

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
content_type = 'application/json' # str | Content Type of input and return mime (default to 'application/json')

    try:
        api_response = api_instance.get_array(namespace, array, content_type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->get_array: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
content_type = 'application/json' # str | Content Type of input and return mime (default to 'application/json')

    try:
        api_response = api_instance.get_array(namespace, array, content_type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->get_array: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **array** | **str**| name/uri of array that is url-encoded | 
 **content_type** | **str**| Content Type of input and return mime | [default to &#39;application/json&#39;]

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
> MaxBufferSizes get_array_max_buffer_sizes(namespace, array, subarray, content_type, x_payer=x_payer)



get the max buffer sizes of an array for a subarray

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
subarray = 'subarray_example' # str | CSV string of subarray to get max buffer sizes for
content_type = 'application/json' # str | Content Type of input and return mime (default to 'application/json')
x_payer = 'x_payer_example' # str | Name of organization or user who should be charged for this request (optional)

    try:
        api_response = api_instance.get_array_max_buffer_sizes(namespace, array, subarray, content_type, x_payer=x_payer)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->get_array_max_buffer_sizes: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
subarray = 'subarray_example' # str | CSV string of subarray to get max buffer sizes for
content_type = 'application/json' # str | Content Type of input and return mime (default to 'application/json')
x_payer = 'x_payer_example' # str | Name of organization or user who should be charged for this request (optional)

    try:
        api_response = api_instance.get_array_max_buffer_sizes(namespace, array, subarray, content_type, x_payer=x_payer)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->get_array_max_buffer_sizes: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **array** | **str**| name/uri of array that is url-encoded | 
 **subarray** | **str**| CSV string of subarray to get max buffer sizes for | 
 **content_type** | **str**| Content Type of input and return mime | [default to &#39;application/json&#39;]
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
> object get_array_meta_data_json(namespace, array, length=length)



get metadata from the array in json format

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
length = 56 # int | (optional) limit character length of returned values (optional)

    try:
        api_response = api_instance.get_array_meta_data_json(namespace, array, length=length)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->get_array_meta_data_json: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
length = 56 # int | (optional) limit character length of returned values (optional)

    try:
        api_response = api_instance.get_array_meta_data_json(namespace, array, length=length)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->get_array_meta_data_json: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **array** | **str**| name/uri of array that is url-encoded | 
 **length** | **int**| (optional) limit character length of returned values | [optional] 

### Return type

**object**

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
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded

    try:
        api_response = api_instance.get_array_metadata(namespace, array)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->get_array_metadata: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded

    try:
        api_response = api_instance.get_array_metadata(namespace, array)
        pprint(api_response)
    except ApiException as e:
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

# **get_array_non_empty_domain**
> NonEmptyDomain get_array_non_empty_domain(namespace, array, content_type, x_payer=x_payer)



get the non empty domain of an array

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
content_type = 'application/json' # str | Content Type of input and return mime (default to 'application/json')
x_payer = 'x_payer_example' # str | Name of organization or user who should be charged for this request (optional)

    try:
        api_response = api_instance.get_array_non_empty_domain(namespace, array, content_type, x_payer=x_payer)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->get_array_non_empty_domain: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
content_type = 'application/json' # str | Content Type of input and return mime (default to 'application/json')
x_payer = 'x_payer_example' # str | Name of organization or user who should be charged for this request (optional)

    try:
        api_response = api_instance.get_array_non_empty_domain(namespace, array, content_type, x_payer=x_payer)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->get_array_non_empty_domain: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **array** | **str**| name/uri of array that is url-encoded | 
 **content_type** | **str**| Content Type of input and return mime | [default to &#39;application/json&#39;]
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

# **get_array_sample_data**
> ArraySample get_array_sample_data(namespace, array, samples=samples)



get an sample set of data from the array

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
samples = 5.0 # float | Number of sample results to return (optional) (default to 5.0)

    try:
        api_response = api_instance.get_array_sample_data(namespace, array, samples=samples)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->get_array_sample_data: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
samples = 5.0 # float | Number of sample results to return (optional) (default to 5.0)

    try:
        api_response = api_instance.get_array_sample_data(namespace, array, samples=samples)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->get_array_sample_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **array** | **str**| name/uri of array that is url-encoded | 
 **samples** | **float**| Number of sample results to return | [optional] [default to 5.0]

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
> list[ArraySharing] get_array_sharing_policies(namespace, array)



Get all sharing details of the array

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded

    try:
        api_response = api_instance.get_array_sharing_policies(namespace, array)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->get_array_sharing_policies: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded

    try:
        api_response = api_instance.get_array_sharing_policies(namespace, array)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->get_array_sharing_policies: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **array** | **str**| name/uri of array that is url-encoded | 

### Return type

[**list[ArraySharing]**](ArraySharing.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of all specific sharing policies |  -  |
**404** | Array does not exist or user does not have permissions to view array sharing policies |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_arrays_in_namespace**
> list[ArrayInfo] get_arrays_in_namespace(namespace)



get metadata on all arrays in a namespace

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)

    try:
        api_response = api_instance.get_arrays_in_namespace(namespace)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->get_arrays_in_namespace: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)

    try:
        api_response = api_instance.get_arrays_in_namespace(namespace)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->get_arrays_in_namespace: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 

### Return type

[**list[ArrayInfo]**](ArrayInfo.md)

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

# **get_last_accessed_arrays**
> list[LastAccessedArray] get_last_accessed_arrays()



### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    
    try:
        api_response = api_instance.get_last_accessed_arrays()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->get_last_accessed_arrays: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    
    try:
        api_response = api_instance.get_last_accessed_arrays()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->get_last_accessed_arrays: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[LastAccessedArray]**](LastAccessedArray.md)

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
> register_array(namespace, array, array_metadata)



register an array at a specified URI registered to the given namespace

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
array_metadata = rest_api.ArrayInfoUpdate() # ArrayInfoUpdate | metadata associated with array

    try:
        api_instance.register_array(namespace, array, array_metadata)
    except ApiException as e:
        print("Exception when calling ArrayApi->register_array: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
array_metadata = rest_api.ArrayInfoUpdate() # ArrayInfoUpdate | metadata associated with array

    try:
        api_instance.register_array(namespace, array, array_metadata)
    except ApiException as e:
        print("Exception when calling ArrayApi->register_array: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **array** | **str**| name/uri of array that is url-encoded | 
 **array_metadata** | [**ArrayInfoUpdate**](ArrayInfoUpdate.md)| metadata associated with array | 

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
**204** | schema registered successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **share_array**
> share_array(namespace, array, array_sharing)



Share an array with a user

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
array_sharing = rest_api.ArraySharing() # ArraySharing | Namespace and list of permissions to share with. An empty list of permissions will remove the namespace, if permissions already exist they will be deleted then new ones added. In the event of a failure, the new polcies will be rolled back to prevent partial policies, and its likely the array will not be shared with the namespace at all

    try:
        api_instance.share_array(namespace, array, array_sharing)
    except ApiException as e:
        print("Exception when calling ArrayApi->share_array: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
array_sharing = rest_api.ArraySharing() # ArraySharing | Namespace and list of permissions to share with. An empty list of permissions will remove the namespace, if permissions already exist they will be deleted then new ones added. In the event of a failure, the new polcies will be rolled back to prevent partial policies, and its likely the array will not be shared with the namespace at all

    try:
        api_instance.share_array(namespace, array, array_sharing)
    except ApiException as e:
        print("Exception when calling ArrayApi->share_array: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **array** | **str**| name/uri of array that is url-encoded | 
 **array_sharing** | [**ArraySharing**](ArraySharing.md)| Namespace and list of permissions to share with. An empty list of permissions will remove the namespace, if permissions already exist they will be deleted then new ones added. In the event of a failure, the new polcies will be rolled back to prevent partial policies, and its likely the array will not be shared with the namespace at all | 

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
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
array_metadata = rest_api.ArrayInfoUpdate() # ArrayInfoUpdate | array metadata to update

    try:
        api_instance.update_array_metadata(namespace, array, array_metadata)
    except ApiException as e:
        print("Exception when calling ArrayApi->update_array_metadata: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
array_metadata = rest_api.ArrayInfoUpdate() # ArrayInfoUpdate | array metadata to update

    try:
        api_instance.update_array_metadata(namespace, array, array_metadata)
    except ApiException as e:
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

# **vacuum_array**
> vacuum_array(namespace, array, tiledb_config)



vacuum an array at a specified URI

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
tiledb_config = rest_api.TileDBConfig() # TileDBConfig | tiledb configuration

    try:
        api_instance.vacuum_array(namespace, array, tiledb_config)
    except ApiException as e:
        print("Exception when calling ArrayApi->vacuum_array: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
tiledb_config = rest_api.TileDBConfig() # TileDBConfig | tiledb configuration

    try:
        api_instance.vacuum_array(namespace, array, tiledb_config)
    except ApiException as e:
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

