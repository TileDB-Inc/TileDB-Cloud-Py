# tiledb.cloud.rest_api.SqlApi

All URIs are relative to *http://localhost/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**run_sql**](SqlApi.md#run_sql) | **POST** /sql/{namespace} | 


# **run_sql**
> [bool, date, datetime, dict, float, int, list, str, none_type] run_sql(namespace, sql)



Run a sql query

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import sql_api
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
    api_instance = sql_api.SqlApi(api_client)
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
        print("Exception when calling SqlApi->run_sql: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.run_sql(namespace, sql, accept_encoding=accept_encoding)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling SqlApi->run_sql: %s\n" % e)
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

