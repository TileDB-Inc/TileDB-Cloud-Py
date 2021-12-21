# tiledb.cloud.rest_api.TasksApi

All URIs are relative to *http://localhost/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**run_sql**](TasksApi.md#run_sql) | **POST** /sql/{namespace} | 
[**task_id_get**](TasksApi.md#task_id_get) | **GET** /task/{id} | 
[**task_id_result_get**](TasksApi.md#task_id_result_get) | **GET** /task/{id}/result | 
[**tasks_get**](TasksApi.md#tasks_get) | **GET** /tasks | 


# **run_sql**
> list[object] run_sql(namespace, sql, accept_encoding=accept_encoding)



Run a sql query

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
    api_instance = tiledb.cloud.rest_api.TasksApi(api_client)
    namespace = 'namespace_example' # str | namespace to run task under is in (an organization name or user's username)
sql = tiledb.cloud.rest_api.SQLParameters() # SQLParameters | sql being submitted
accept_encoding = 'accept_encoding_example' # str | Encoding to use (optional)

    try:
        api_response = api_instance.run_sql(namespace, sql, accept_encoding=accept_encoding)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TasksApi->run_sql: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.TasksApi(api_client)
    namespace = 'namespace_example' # str | namespace to run task under is in (an organization name or user's username)
sql = tiledb.cloud.rest_api.SQLParameters() # SQLParameters | sql being submitted
accept_encoding = 'accept_encoding_example' # str | Encoding to use (optional)

    try:
        api_response = api_instance.run_sql(namespace, sql, accept_encoding=accept_encoding)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TasksApi->run_sql: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace to run task under is in (an organization name or user&#39;s username) | 
 **sql** | [**SQLParameters**](SQLParameters.md)| sql being submitted | 
 **accept_encoding** | **str**| Encoding to use | [optional] 

### Return type

**list[object]**

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | JSON results in array of objects form, if the query returns results |  * X-TILEDB-CLOUD-TASK-ID - Task ID for just completed query <br>  |
**204** | SQL executed successfully |  * X-TILEDB-CLOUD-TASK-ID - Task ID for just completed query <br>  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **task_id_get**
> ArrayTask task_id_get(id)



Fetch an array task

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
    api_instance = tiledb.cloud.rest_api.TasksApi(api_client)
    id = 'id_example' # str | task ID to fetch

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
    api_instance = tiledb.cloud.rest_api.TasksApi(api_client)
    id = 'id_example' # str | task ID to fetch

    try:
        api_response = api_instance.task_id_get(id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TasksApi->task_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| task ID to fetch | 

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

# **task_id_result_get**
> str task_id_result_get(id, accept_encoding=accept_encoding)



Retrieve results of an array task

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
    api_instance = tiledb.cloud.rest_api.TasksApi(api_client)
    id = 'id_example' # str | task ID to retrieve stored results
accept_encoding = 'accept_encoding_example' # str | Encoding to use (optional)

    try:
        api_response = api_instance.task_id_result_get(id, accept_encoding=accept_encoding)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TasksApi->task_id_result_get: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.TasksApi(api_client)
    id = 'id_example' # str | task ID to retrieve stored results
accept_encoding = 'accept_encoding_example' # str | Encoding to use (optional)

    try:
        api_response = api_instance.task_id_result_get(id, accept_encoding=accept_encoding)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TasksApi->task_id_result_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| task ID to retrieve stored results | 
 **accept_encoding** | **str**| Encoding to use | [optional] 

### Return type

**str**

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | output and format of originating request |  * Content-Type - format results are delivered in <br>  |
**202** | task is still executing |  -  |
**404** | results were not saved, or results have expored |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tasks_get**
> ArrayTaskData tasks_get(namespace=namespace, created_by=created_by, array=array, start=start, end=end, page=page, per_page=per_page, type=type, exclude_type=exclude_type, file_type=file_type, exclude_file_type=exclude_file_type, status=status, search=search, orderby=orderby)



Fetch a list of all array tasks a user has access to

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
    api_instance = tiledb.cloud.rest_api.TasksApi(api_client)
    namespace = 'namespace_example' # str | namespace to filter (optional)
created_by = 'created_by_example' # str | username to filter (optional)
array = 'array_example' # str | name/uri of array that is url-encoded to filter (optional)
start = 56 # int | start time for tasks to filter by (optional)
end = 56 # int | end time for tasks to filter by (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
type = 'type_example' # str | task type, \"QUERY\", \"SQL\", \"UDF\", \"GENERIC_UDF\" (optional)
exclude_type = ['exclude_type_example'] # list[str] | task_type to exclude matching array in results, more than one can be included (optional)
file_type = ['file_type_example'] # list[str] | match file_type of task array, more than one can be included (optional)
exclude_file_type = ['exclude_file_type_example'] # list[str] | exclude file_type of task arrays, more than one can be included (optional)
status = 'status_example' # str | Filter to only return these statuses (optional)
search = 'search_example' # str | search string that will look at name, namespace or description fields (optional)
orderby = 'orderby_example' # str | sort by which field valid values include start_time, name (optional)

    try:
        api_response = api_instance.tasks_get(namespace=namespace, created_by=created_by, array=array, start=start, end=end, page=page, per_page=per_page, type=type, exclude_type=exclude_type, file_type=file_type, exclude_file_type=exclude_file_type, status=status, search=search, orderby=orderby)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TasksApi->tasks_get: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.TasksApi(api_client)
    namespace = 'namespace_example' # str | namespace to filter (optional)
created_by = 'created_by_example' # str | username to filter (optional)
array = 'array_example' # str | name/uri of array that is url-encoded to filter (optional)
start = 56 # int | start time for tasks to filter by (optional)
end = 56 # int | end time for tasks to filter by (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
type = 'type_example' # str | task type, \"QUERY\", \"SQL\", \"UDF\", \"GENERIC_UDF\" (optional)
exclude_type = ['exclude_type_example'] # list[str] | task_type to exclude matching array in results, more than one can be included (optional)
file_type = ['file_type_example'] # list[str] | match file_type of task array, more than one can be included (optional)
exclude_file_type = ['exclude_file_type_example'] # list[str] | exclude file_type of task arrays, more than one can be included (optional)
status = 'status_example' # str | Filter to only return these statuses (optional)
search = 'search_example' # str | search string that will look at name, namespace or description fields (optional)
orderby = 'orderby_example' # str | sort by which field valid values include start_time, name (optional)

    try:
        api_response = api_instance.tasks_get(namespace=namespace, created_by=created_by, array=array, start=start, end=end, page=page, per_page=per_page, type=type, exclude_type=exclude_type, file_type=file_type, exclude_file_type=exclude_file_type, status=status, search=search, orderby=orderby)
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
 **page** | **int**| pagination offset | [optional] 
 **per_page** | **int**| pagination limit | [optional] 
 **type** | **str**| task type, \&quot;QUERY\&quot;, \&quot;SQL\&quot;, \&quot;UDF\&quot;, \&quot;GENERIC_UDF\&quot; | [optional] 
 **exclude_type** | [**list[str]**](str.md)| task_type to exclude matching array in results, more than one can be included | [optional] 
 **file_type** | [**list[str]**](str.md)| match file_type of task array, more than one can be included | [optional] 
 **exclude_file_type** | [**list[str]**](str.md)| exclude file_type of task arrays, more than one can be included | [optional] 
 **status** | **str**| Filter to only return these statuses | [optional] 
 **search** | **str**| search string that will look at name, namespace or description fields | [optional] 
 **orderby** | **str**| sort by which field valid values include start_time, name | [optional] 

### Return type

[**ArrayTaskData**](ArrayTaskData.md)

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

