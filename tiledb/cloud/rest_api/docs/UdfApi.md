# rest_api.UdfApi

All URIs are relative to *http://localhost/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_ud_fs**](UdfApi.md#get_ud_fs) | **GET** /udfs | 
[**get_udf**](UdfApi.md#get_udf) | **GET** /udf/{namespace}/{name} | 
[**get_udf_sharing_policies**](UdfApi.md#get_udf_sharing_policies) | **GET** /udf/{namespace}/{name}/share | 
[**register_udf**](UdfApi.md#register_udf) | **POST** /udf/{namespace}/{name} | 
[**share_udf**](UdfApi.md#share_udf) | **PATCH** /udf/{namespace}/{name}/share | 
[**submit_generic_udf**](UdfApi.md#submit_generic_udf) | **POST** /udfs/generic/{namespace} | 
[**submit_udf**](UdfApi.md#submit_udf) | **POST** /arrays/{namespace}/{array}/udf/submit | 
[**updated_registered_udf**](UdfApi.md#updated_registered_udf) | **PATCH** /udf/{namespace}/{name} | 


# **get_ud_fs**
> UDFListingData get_ud_fs(namespace=namespace, created_by=created_by, page=page, per_page=per_page, type=type, search=search, orderby=orderby)



get a all UDFs accessible to the user

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
namespace = 'namespace_example' # str | namespace to filter (optional)
created_by = 'created_by_example' # str | username to filter (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
type = 'type_example' # str | udf type, \"generic\", \"single_array\" (optional)
search = 'search_example' # str | search string that will look at name, namespace or description fields (optional)
orderby = 'orderby_example' # str | sort by which field valid values include created_at, last_used, name (optional)

try:
    api_response = api_instance.get_ud_fs(namespace=namespace, created_by=created_by, page=page, per_page=per_page, type=type, search=search, orderby=orderby)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UdfApi->get_ud_fs: %s\n" % e)
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
namespace = 'namespace_example' # str | namespace to filter (optional)
created_by = 'created_by_example' # str | username to filter (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
type = 'type_example' # str | udf type, \"generic\", \"single_array\" (optional)
search = 'search_example' # str | search string that will look at name, namespace or description fields (optional)
orderby = 'orderby_example' # str | sort by which field valid values include created_at, last_used, name (optional)

try:
    api_response = api_instance.get_ud_fs(namespace=namespace, created_by=created_by, page=page, per_page=per_page, type=type, search=search, orderby=orderby)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UdfApi->get_ud_fs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace to filter | [optional] 
 **created_by** | **str**| username to filter | [optional] 
 **page** | **int**| pagination offset | [optional] 
 **per_page** | **int**| pagination limit | [optional] 
 **type** | **str**| udf type, \&quot;generic\&quot;, \&quot;single_array\&quot; | [optional] 
 **search** | **str**| search string that will look at name, namespace or description fields | [optional] 
 **orderby** | **str**| sort by which field valid values include created_at, last_used, name | [optional] 

### Return type

[**UDFListingData**](UDFListingData.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | registered udfs |  -  |
**404** | udf not found |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_udf**
> UDFRegistration get_udf(namespace, name)



get a specific UDF in the given namespace

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
name = 'name_example' # str | name to register udf under

try:
    api_response = api_instance.get_udf(namespace, name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UdfApi->get_udf: %s\n" % e)
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
name = 'name_example' # str | name to register udf under

try:
    api_response = api_instance.get_udf(namespace, name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UdfApi->get_udf: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **name** | **str**| name to register udf under | 

### Return type

[**UDFRegistration**](UDFRegistration.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | udf registered successfully |  -  |
**404** | udf not found |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_udf_sharing_policies**
> list[UDFSharing] get_udf_sharing_policies(namespace, name)



Get all sharing details of the udf

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
name = 'name_example' # str | name of registered ud

try:
    api_response = api_instance.get_udf_sharing_policies(namespace, name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UdfApi->get_udf_sharing_policies: %s\n" % e)
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
name = 'name_example' # str | name of registered ud

try:
    api_response = api_instance.get_udf_sharing_policies(namespace, name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UdfApi->get_udf_sharing_policies: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **name** | **str**| name of registered ud | 

### Return type

[**list[UDFSharing]**](UDFSharing.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of all specific sharing policies |  -  |
**404** | UDF does not exist or user does not have permissions to view array sharing policies |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **register_udf**
> register_udf(namespace, name, udf)



register a UDF in the given namespace

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
name = 'name_example' # str | name to register udf under
udf = rest_api.UDFRegistration() # UDFRegistration | udf to register

try:
    api_instance.register_udf(namespace, name, udf)
except ApiException as e:
    print("Exception when calling UdfApi->register_udf: %s\n" % e)
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
name = 'name_example' # str | name to register udf under
udf = rest_api.UDFRegistration() # UDFRegistration | udf to register

try:
    api_instance.register_udf(namespace, name, udf)
except ApiException as e:
    print("Exception when calling UdfApi->register_udf: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **name** | **str**| name to register udf under | 
 **udf** | [**UDFRegistration**](UDFRegistration.md)| udf to register | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | udf registered successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **share_udf**
> share_udf(namespace, name, udf_sharing)



Share a UDF with a user

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
name = 'name_example' # str | name of registered ud
udf_sharing = rest_api.UDFSharing() # UDFSharing | Namespace and list of permissions to share with. An empty list of permissions will remove the namespace, if permissions already exist they will be deleted then new ones added. In the event of a failure, the new polcies will be rolled back to prevent partial policies, and its likely the udf will not be shared with the namespace at all

try:
    api_instance.share_udf(namespace, name, udf_sharing)
except ApiException as e:
    print("Exception when calling UdfApi->share_udf: %s\n" % e)
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
name = 'name_example' # str | name of registered ud
udf_sharing = rest_api.UDFSharing() # UDFSharing | Namespace and list of permissions to share with. An empty list of permissions will remove the namespace, if permissions already exist they will be deleted then new ones added. In the event of a failure, the new polcies will be rolled back to prevent partial policies, and its likely the udf will not be shared with the namespace at all

try:
    api_instance.share_udf(namespace, name, udf_sharing)
except ApiException as e:
    print("Exception when calling UdfApi->share_udf: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **name** | **str**| name of registered ud | 
 **udf_sharing** | [**UDFSharing**](UDFSharing.md)| Namespace and list of permissions to share with. An empty list of permissions will remove the namespace, if permissions already exist they will be deleted then new ones added. In the event of a failure, the new polcies will be rolled back to prevent partial policies, and its likely the udf will not be shared with the namespace at all | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | UDF shared successfully |  -  |
**404** | UDF does not exist or user does not have permissions to share udf |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **submit_generic_udf**
> file submit_generic_udf(namespace, udf, accept_encoding=accept_encoding)



send a generic UDF in the given namespace

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
udf = rest_api.GenericUDF() # GenericUDF | udf to run
accept_encoding = 'accept_encoding_example' # str | Encoding to use (optional)

try:
    api_response = api_instance.submit_generic_udf(namespace, udf, accept_encoding=accept_encoding)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UdfApi->submit_generic_udf: %s\n" % e)
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
udf = rest_api.GenericUDF() # GenericUDF | udf to run
accept_encoding = 'accept_encoding_example' # str | Encoding to use (optional)

try:
    api_response = api_instance.submit_generic_udf(namespace, udf, accept_encoding=accept_encoding)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UdfApi->submit_generic_udf: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **udf** | [**GenericUDF**](GenericUDF.md)| udf to run | 
 **accept_encoding** | **str**| Encoding to use | [optional] 

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

# **submit_udf**
> file submit_udf(namespace, array, udf, x_payer=x_payer, accept_encoding=accept_encoding)



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
accept_encoding = 'accept_encoding_example' # str | Encoding to use (optional)

try:
    api_response = api_instance.submit_udf(namespace, array, udf, x_payer=x_payer, accept_encoding=accept_encoding)
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
accept_encoding = 'accept_encoding_example' # str | Encoding to use (optional)

try:
    api_response = api_instance.submit_udf(namespace, array, udf, x_payer=x_payer, accept_encoding=accept_encoding)
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
 **accept_encoding** | **str**| Encoding to use | [optional] 

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

# **updated_registered_udf**
> updated_registered_udf(namespace, name, udf)



updated an existing registerd UDF in the given namespace

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
name = 'name_example' # str | name to register udf under
udf = rest_api.UDFRegistration() # UDFRegistration | udf to update

try:
    api_instance.updated_registered_udf(namespace, name, udf)
except ApiException as e:
    print("Exception when calling UdfApi->updated_registered_udf: %s\n" % e)
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
name = 'name_example' # str | name to register udf under
udf = rest_api.UDFRegistration() # UDFRegistration | udf to update

try:
    api_instance.updated_registered_udf(namespace, name, udf)
except ApiException as e:
    print("Exception when calling UdfApi->updated_registered_udf: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **name** | **str**| name to register udf under | 
 **udf** | [**UDFRegistration**](UDFRegistration.md)| udf to update | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | udf updated successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

