# rest_api.UdfApi

All URIs are relative to *http://localhost/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**submit_udf**](UdfApi.md#submit_udf) | **POST** /arrays/{namespace}/{array}/udf/submit | 


# **submit_udf**
> file submit_udf(namespace, array, udf, x_payer=x_payer)



send a UDF to run against a specified array/URI registered to a group/project

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
api_instance = rest_api.UdfApi(rest_api.ApiClient(configuration))
namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
udf = rest_api.UDF() # UDF | udf to run
x_payer = 'x_payer_example' # str | Name of organization or user who should be charged for this request (optional)

try:
    api_response = api_instance.submit_udf(namespace, array, udf, x_payer=x_payer)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UdfApi->submit_udf: %s\n" % e)
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
api_instance = rest_api.UdfApi(rest_api.ApiClient(configuration))
namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
udf = rest_api.UDF() # UDF | udf to run
x_payer = 'x_payer_example' # str | Name of organization or user who should be charged for this request (optional)

try:
    api_response = api_instance.submit_udf(namespace, array, udf, x_payer=x_payer)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UdfApi->submit_udf: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **array** | **str**| name/uri of array that is url-encoded | 
 **udf** | [**UDF**](UDF.md)| udf to run | 
 **x_payer** | **str**| Name of organization or user who should be charged for this request | [optional] 

### Return type

**file**

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/octet-stream

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | udf completed and the udf-type specific result is returned |  * X-TILEDB-CLOUD-TASK-ID - Task ID for just completed request <br>  |
**0** | error response |  * X-TILEDB-CLOUD-TASK-ID - Task ID for just request if task was started <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

