# tiledb.cloud.rest_api.TasksApi

All URIs are relative to *http://localhost/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**run_sql**](TasksApi.md#run_sql) | **POST** /sql/{namespace} | 
[**task_id_get**](TasksApi.md#task_id_get) | **GET** /task/{id} | 
[**task_id_result_get**](TasksApi.md#task_id_result_get) | **GET** /task/{id}/result | 
[**tasks_get**](TasksApi.md#tasks_get) | **GET** /tasks | 


# **run_sql**
> [bool, date, datetime, dict, float, int, list, str, none_type] run_sql(namespace, sql)



Run a sql query

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import tasks_api
from tiledb.cloud.rest_api.model.sql_parameters import SQLParameters
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
    api_instance = tasks_api.TasksApi(api_client)
    namespace = "namespace_example" # str | namespace to run task under is in (an organization name or user's username)
    sql = SQLParameters(
        name="name_example",
        query="query_example",
        output_uri="s3://my_bucket/my_output_array",
        store_results=True,
        dont_download_results=True,
        result_format=ResultFormat("python_pickle"),
        init_commands=[
            "init_commands_example",
        ],
        parameters=[
            {},
        ],
        task_graph_uuid="task_graph_uuid_example",
        client_node_uuid="client_node_uuid_example",
    ) # SQLParameters | sql being submitted
    accept_encoding = "Accept-Encoding_example" # str | Encoding to use (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.run_sql(namespace, sql)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling TasksApi->run_sql: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.run_sql(namespace, sql, accept_encoding=accept_encoding)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling TasksApi->run_sql: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace to run task under is in (an organization name or user&#39;s username) |
 **sql** | [**SQLParameters**](SQLParameters.md)| sql being submitted |
 **accept_encoding** | **str**| Encoding to use | [optional]

### Return type

**[bool, date, datetime, dict, float, int, list, str, none_type]**

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | JSON results in array of objects form, if the query returns results |  * X-TILEDB-CLOUD-TASK-ID - Task ID for just completed request <br>  |
**204** | SQL executed successfully |  * X-TILEDB-CLOUD-TASK-ID - Task ID for just completed request <br>  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **task_id_get**
> ArrayTask task_id_get(id)



Fetch an array task

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import tasks_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.array_task import ArrayTask
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
    api_instance = tasks_api.TasksApi(api_client)
    id = "id_example" # str | task ID to fetch

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.task_id_get(id)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
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
> str task_id_result_get(id)



Retrieve results of an array task

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import tasks_api
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
    api_instance = tasks_api.TasksApi(api_client)
    id = "id_example" # str | task ID to retrieve stored results
    accept_encoding = "Accept-Encoding_example" # str | Encoding to use (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.task_id_result_get(id)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling TasksApi->task_id_result_get: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.task_id_result_get(id, accept_encoding=accept_encoding)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
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
> ArrayTaskData tasks_get()



Fetch a list of all array tasks a user has access to

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import tasks_api
from tiledb.cloud.rest_api.model.array_task_data import ArrayTaskData
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
    api_instance = tasks_api.TasksApi(api_client)
    namespace = "namespace_example" # str | namespace to filter (optional)
    created_by = "created_by_example" # str | username to filter (optional)
    array = "array_example" # str | name/uri of array that is url-encoded to filter (optional)
    start = 1 # int | start time for tasks to filter by (optional)
    end = 1 # int | end time for tasks to filter by (optional)
    page = 1 # int | pagination offset (optional)
    per_page = 1 # int | pagination limit (optional)
    type = "type_example" # str | task type, \"QUERY\", \"SQL\", \"UDF\", \"GENERIC_UDF\" (optional)
    exclude_type = [
        "exclude_type_example",
    ] # [str] | task_type to exclude matching array in results, more than one can be included (optional)
    file_type = [
        "file_type_example",
    ] # [str] | match file_type of task array, more than one can be included (optional)
    exclude_file_type = [
        "exclude_file_type_example",
    ] # [str] | exclude file_type of task arrays, more than one can be included (optional)
    status = "status_example" # str | Filter to only return these statuses (optional)
    search = "search_example" # str | search string that will look at name, namespace or description fields (optional)
    orderby = "orderby_example" # str | sort by which field valid values include start_time, name (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.tasks_get(namespace=namespace, created_by=created_by, array=array, start=start, end=end, page=page, per_page=per_page, type=type, exclude_type=exclude_type, file_type=file_type, exclude_file_type=exclude_file_type, status=status, search=search, orderby=orderby)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
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
 **exclude_type** | **[str]**| task_type to exclude matching array in results, more than one can be included | [optional]
 **file_type** | **[str]**| match file_type of task array, more than one can be included | [optional]
 **exclude_file_type** | **[str]**| exclude file_type of task arrays, more than one can be included | [optional]
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

