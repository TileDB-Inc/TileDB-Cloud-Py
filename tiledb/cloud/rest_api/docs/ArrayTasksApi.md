# rest_api.ArrayTasksApi

All URIs are relative to *http://localhost/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_array_tasks_sidebar**](ArrayTasksApi.md#get_array_tasks_sidebar) | **GET** /tasks/sidebar | 


# **get_array_tasks_sidebar**
> ArrayTaskBrowserSidebar get_array_tasks_sidebar(start=start, end=end)



### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
configuration = rest_api.Configuration()
# Configure API key authorization: ApiKeyAuth
configuration.api_key['X-TILEDB-REST-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'
configuration = rest_api.Configuration()
# Configure HTTP basic authorization: BasicAuth
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# Defining host is optional and default to http://localhost/v1
configuration.host = "http://localhost/v1"
# Create an instance of the API class
api_instance = rest_api.ArrayTasksApi(rest_api.ApiClient(configuration))
start = 56 # int | Fetch tasks created after this time, unix epoch in seconds, default 7 days ago (optional)
end = 56 # int | Fetch tasks created before this time, unix epoch in seconds, default now (optional)

try:
    api_response = api_instance.get_array_tasks_sidebar(start=start, end=end)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ArrayTasksApi->get_array_tasks_sidebar: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
configuration = rest_api.Configuration()
# Configure API key authorization: ApiKeyAuth
configuration.api_key['X-TILEDB-REST-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'
configuration = rest_api.Configuration()
# Configure HTTP basic authorization: BasicAuth
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# Defining host is optional and default to http://localhost/v1
configuration.host = "http://localhost/v1"
# Create an instance of the API class
api_instance = rest_api.ArrayTasksApi(rest_api.ApiClient(configuration))
start = 56 # int | Fetch tasks created after this time, unix epoch in seconds, default 7 days ago (optional)
end = 56 # int | Fetch tasks created before this time, unix epoch in seconds, default now (optional)

try:
    api_response = api_instance.get_array_tasks_sidebar(start=start, end=end)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ArrayTasksApi->get_array_tasks_sidebar: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start** | **int**| Fetch tasks created after this time, unix epoch in seconds, default 7 days ago | [optional] 
 **end** | **int**| Fetch tasks created before this time, unix epoch in seconds, default now | [optional] 

### Return type

[**ArrayTaskBrowserSidebar**](ArrayTaskBrowserSidebar.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | sidebar metadata for task definitions for all arrays user has access to |  -  |
**404** | array tasks not found |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

