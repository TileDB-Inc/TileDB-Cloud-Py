# tiledb.cloud.rest_api.ArrayTasksApi

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
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
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
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost/v1",
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
    api_instance = tiledb.cloud.rest_api.ArrayTasksApi(api_client)
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
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
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
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost/v1",
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
    api_instance = tiledb.cloud.rest_api.ArrayTasksApi(api_client)
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

