# tiledb.cloud.rest_api.ArrayApi

All URIs are relative to *http://localhost/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**array_activity_log**](ArrayApi.md#array_activity_log) | **GET** /arrays/{namespace}/{array}/activity | 


# **array_activity_log**
> ArrayActivityLogData array_activity_log(namespace, array, start=start, end=end, event_types=event_types, task_id=task_id, has_task_id=has_task_id, page=page, per_page=per_page)



get array activity logs

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v2
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost/v2"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost/v2",
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
    api_instance = tiledb.cloud.rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
start = 56 # int | Start time of window of fetch logs, unix epoch in seconds (default: seven days ago) (optional)
end = 56 # int | End time of window of fetch logs, unix epoch in seconds (default: current utc timestamp) (optional)
event_types = ['event_types_example'] # list[str] | Event values can be one or more of the following read, write, create, delete, register, deregister, comma separated (optional)
task_id = 'task_id_example' # str | Array task id To filter activity to (optional)
has_task_id = True # bool | Excludes activity log results that does not contain an array task uuid (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        api_response = api_instance.array_activity_log(namespace, array, start=start, end=end, event_types=event_types, task_id=task_id, has_task_id=has_task_id, page=page, per_page=per_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->array_activity_log: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v2
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost/v2"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost/v2",
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
    api_instance = tiledb.cloud.rest_api.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
start = 56 # int | Start time of window of fetch logs, unix epoch in seconds (default: seven days ago) (optional)
end = 56 # int | End time of window of fetch logs, unix epoch in seconds (default: current utc timestamp) (optional)
event_types = ['event_types_example'] # list[str] | Event values can be one or more of the following read, write, create, delete, register, deregister, comma separated (optional)
task_id = 'task_id_example' # str | Array task id To filter activity to (optional)
has_task_id = True # bool | Excludes activity log results that does not contain an array task uuid (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        api_response = api_instance.array_activity_log(namespace, array, start=start, end=end, event_types=event_types, task_id=task_id, has_task_id=has_task_id, page=page, per_page=per_page)
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
 **event_types** | [**list[str]**](str.md)| Event values can be one or more of the following read, write, create, delete, register, deregister, comma separated | [optional] 
 **task_id** | **str**| Array task id To filter activity to | [optional] 
 **has_task_id** | **bool**| Excludes activity log results that does not contain an array task uuid | [optional] 
 **page** | **int**| pagination offset | [optional] 
 **per_page** | **int**| pagination limit | [optional] 

### Return type

[**ArrayActivityLogData**](ArrayActivityLogData.md)

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

