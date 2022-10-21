# tiledb.cloud.rest_api.QueryApi

All URIs are relative to *http://localhost/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**submit_query**](QueryApi.md#submit_query) | **POST** /arrays/{namespace}/{array}/query/submit | 


# **submit_query**
> file submit_query(namespace, array, type, content_type, query, x_payer=x_payer, open_at=open_at, read_all=read_all)



send a query to run against a specified array/URI registered to a group/project

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
    api_instance = tiledb.cloud.rest_api.QueryApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
type = 'type_example' # str | type of query
content_type = 'application/json' # str | Content Type of input and return mime (default to 'application/json')
query = tiledb.cloud.rest_api.Query() # Query | query to run
x_payer = 'x_payer_example' # str | Name of organization or user who should be charged for this request (optional)
open_at = 56 # int | open_at for array in unix epoch (optional)
read_all = 'read_all_example' # str | If \"true\", resubmits incomplete queries until the query has completed. Defaults to \"false\". (optional)

    try:
        api_response = api_instance.submit_query(namespace, array, type, content_type, query, x_payer=x_payer, open_at=open_at, read_all=read_all)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling QueryApi->submit_query: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.QueryApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
type = 'type_example' # str | type of query
content_type = 'application/json' # str | Content Type of input and return mime (default to 'application/json')
query = tiledb.cloud.rest_api.Query() # Query | query to run
x_payer = 'x_payer_example' # str | Name of organization or user who should be charged for this request (optional)
open_at = 56 # int | open_at for array in unix epoch (optional)
read_all = 'read_all_example' # str | If \"true\", resubmits incomplete queries until the query has completed. Defaults to \"false\". (optional)

    try:
        api_response = api_instance.submit_query(namespace, array, type, content_type, query, x_payer=x_payer, open_at=open_at, read_all=read_all)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling QueryApi->submit_query: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **array** | **str**| name/uri of array that is url-encoded | 
 **type** | **str**| type of query | 
 **content_type** | **str**| Content Type of input and return mime | [default to &#39;application/json&#39;]
 **query** | [**Query**](Query.md)| query to run | 
 **x_payer** | **str**| Name of organization or user who should be charged for this request | [optional] 
 **open_at** | **int**| open_at for array in unix epoch | [optional] 
 **read_all** | **str**| If \&quot;true\&quot;, resubmits incomplete queries until the query has completed. Defaults to \&quot;false\&quot;. | [optional] 

### Return type

**file**

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/capnp
 - **Accept**: application/json, application/capnp

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | query completed and results are returned in query object |  * X-TILEDB-CLOUD-TASK-ID - Task ID for just completed query <br>  |
**204** | query completed successfully with no return |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

