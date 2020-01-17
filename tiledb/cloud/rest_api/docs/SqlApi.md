# rest_api.SqlApi

All URIs are relative to *http://localhost/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**run_sql**](SqlApi.md#run_sql) | **POST** /sql/{namespace} | 


# **run_sql**
> list[object] run_sql(namespace, sql, accept_encoding=accept_encoding)



Run a sql query

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
api_instance = rest_api.SqlApi(rest_api.ApiClient(configuration))
namespace = 'namespace_example' # str | namespace to run task under is in (an organization name or user's username)
sql = rest_api.SQLParameters() # SQLParameters | sql being submitted
accept_encoding = 'accept_encoding_example' # str | Encoding to use (optional)

try:
    api_response = api_instance.run_sql(namespace, sql, accept_encoding=accept_encoding)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SqlApi->run_sql: %s\n" % e)
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
api_instance = rest_api.SqlApi(rest_api.ApiClient(configuration))
namespace = 'namespace_example' # str | namespace to run task under is in (an organization name or user's username)
sql = rest_api.SQLParameters() # SQLParameters | sql being submitted
accept_encoding = 'accept_encoding_example' # str | Encoding to use (optional)

try:
    api_response = api_instance.run_sql(namespace, sql, accept_encoding=accept_encoding)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SqlApi->run_sql: %s\n" % e)
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

