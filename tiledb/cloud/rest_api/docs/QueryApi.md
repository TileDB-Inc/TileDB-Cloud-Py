# rest_api.QueryApi

All URIs are relative to *http://localhost/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**finalize_query**](QueryApi.md#finalize_query) | **POST** /arrays/{namespace}/{array}/query/finalize | 
[**submit_query**](QueryApi.md#submit_query) | **POST** /arrays/{namespace}/{array}/query/submit | 


# **finalize_query**
> Query finalize_query(namespace, array, type, content_type, query, x_payer=x_payer, open_at=open_at)



send a query to run against a specified array/URI registered to a group/project

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
api_instance = rest_api.QueryApi(rest_api.ApiClient(configuration))
namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
type = 'type_example' # str | type of query
content_type = 'application/json' # str | Content Type of input and return mime (default to 'application/json')
query = rest_api.Query() # Query | query to run
x_payer = 'x_payer_example' # str | Name of organization or user who should be charged for this request (optional)
open_at = 56 # int | open_at for array in unix epoch (optional)

try:
    api_response = api_instance.finalize_query(namespace, array, type, content_type, query, x_payer=x_payer, open_at=open_at)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueryApi->finalize_query: %s\n" % e)
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
api_instance = rest_api.QueryApi(rest_api.ApiClient(configuration))
namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
type = 'type_example' # str | type of query
content_type = 'application/json' # str | Content Type of input and return mime (default to 'application/json')
query = rest_api.Query() # Query | query to run
x_payer = 'x_payer_example' # str | Name of organization or user who should be charged for this request (optional)
open_at = 56 # int | open_at for array in unix epoch (optional)

try:
    api_response = api_instance.finalize_query(namespace, array, type, content_type, query, x_payer=x_payer, open_at=open_at)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueryApi->finalize_query: %s\n" % e)
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

### Return type

[**Query**](Query.md)

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

# **submit_query**
> Query submit_query(namespace, array, type, content_type, query, x_payer=x_payer, open_at=open_at)



send a query to run against a specified array/URI registered to a group/project

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
api_instance = rest_api.QueryApi(rest_api.ApiClient(configuration))
namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
type = 'type_example' # str | type of query
content_type = 'application/json' # str | Content Type of input and return mime (default to 'application/json')
query = rest_api.Query() # Query | query to run
x_payer = 'x_payer_example' # str | Name of organization or user who should be charged for this request (optional)
open_at = 56 # int | open_at for array in unix epoch (optional)

try:
    api_response = api_instance.submit_query(namespace, array, type, content_type, query, x_payer=x_payer, open_at=open_at)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueryApi->submit_query: %s\n" % e)
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
api_instance = rest_api.QueryApi(rest_api.ApiClient(configuration))
namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
type = 'type_example' # str | type of query
content_type = 'application/json' # str | Content Type of input and return mime (default to 'application/json')
query = rest_api.Query() # Query | query to run
x_payer = 'x_payer_example' # str | Name of organization or user who should be charged for this request (optional)
open_at = 56 # int | open_at for array in unix epoch (optional)

try:
    api_response = api_instance.submit_query(namespace, array, type, content_type, query, x_payer=x_payer, open_at=open_at)
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

### Return type

[**Query**](Query.md)

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

