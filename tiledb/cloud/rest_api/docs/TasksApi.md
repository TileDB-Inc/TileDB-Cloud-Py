# rest_api.TasksApi

All URIs are relative to *http://localhost/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**task_id_get**](TasksApi.md#task_id_get) | **GET** /task/{id} | 
[**tasks_get**](TasksApi.md#tasks_get) | **GET** /tasks | 


# **task_id_get**
> ArrayTask task_id_get(id)



Fetch an array task

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
api_instance = rest_api.TasksApi(rest_api.ApiClient(configuration))
id = 'id_example' # str | task id to fetch

try:
    api_response = api_instance.task_id_get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->task_id_get: %s\n" % e)
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
api_instance = rest_api.TasksApi(rest_api.ApiClient(configuration))
id = 'id_example' # str | task id to fetch

try:
    api_response = api_instance.task_id_get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->task_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| task id to fetch | 

### Return type

[**ArrayTask**](ArrayTask.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Array task |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tasks_get**
> list[ArrayTask] tasks_get(namespace=namespace, created_by=created_by, array=array, start=start, end=end, status=status)



Fetch a list of all array tasks a user has access to

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
api_instance = rest_api.TasksApi(rest_api.ApiClient(configuration))
namespace = 'namespace_example' # str | namespace to filter (optional)
created_by = 'created_by_example' # str | username to filter (optional)
array = 'array_example' # str | name/uri of array that is url-encoded to filter (optional)
start = 56 # int | start time for tasks to filter by (optional)
end = 56 # int | end time for tasks to filter by (optional)
status = 'status_example' # str | Filter to only return these statuses (optional)

try:
    api_response = api_instance.tasks_get(namespace=namespace, created_by=created_by, array=array, start=start, end=end, status=status)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->tasks_get: %s\n" % e)
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
api_instance = rest_api.TasksApi(rest_api.ApiClient(configuration))
namespace = 'namespace_example' # str | namespace to filter (optional)
created_by = 'created_by_example' # str | username to filter (optional)
array = 'array_example' # str | name/uri of array that is url-encoded to filter (optional)
start = 56 # int | start time for tasks to filter by (optional)
end = 56 # int | end time for tasks to filter by (optional)
status = 'status_example' # str | Filter to only return these statuses (optional)

try:
    api_response = api_instance.tasks_get(namespace=namespace, created_by=created_by, array=array, start=start, end=end, status=status)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->tasks_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace to filter | [optional] 
 **created_by** | **str**| username to filter | [optional] 
 **array** | **str**| name/uri of array that is url-encoded to filter | [optional] 
 **start** | **int**| start time for tasks to filter by | [optional] 
 **end** | **int**| end time for tasks to filter by | [optional] 
 **status** | **str**| Filter to only return these statuses | [optional] 

### Return type

[**list[ArrayTask]**](ArrayTask.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Array of all tasks user has access too |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

