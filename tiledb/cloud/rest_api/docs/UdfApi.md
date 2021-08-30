# tiledb.cloud.rest_api.UdfApi

All URIs are relative to *http://localhost/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_udf_info**](UdfApi.md#delete_udf_info) | **DELETE** /udf/{namespace}/{name} | 
[**get_udf_info**](UdfApi.md#get_udf_info) | **GET** /udf/{namespace}/{name} | 
[**get_udf_info_sharing_policies**](UdfApi.md#get_udf_info_sharing_policies) | **GET** /udf/{namespace}/{name}/share | 
[**register_udf_info**](UdfApi.md#register_udf_info) | **POST** /udf/{namespace}/{name} | 
[**share_udf_info**](UdfApi.md#share_udf_info) | **PATCH** /udf/{namespace}/{name}/share | 
[**submit_generic_udf**](UdfApi.md#submit_generic_udf) | **POST** /udfs/generic/{namespace} | 
[**submit_multi_array_udf**](UdfApi.md#submit_multi_array_udf) | **POST** /udfs/arrays/{namespace} | 
[**submit_udf**](UdfApi.md#submit_udf) | **POST** /arrays/{namespace}/{array}/udf/submit | 
[**udf_namespace_array_versions_get**](UdfApi.md#udf_namespace_array_versions_get) | **GET** /udf/{namespace}/{array}/versions | 
[**update_udf_info**](UdfApi.md#update_udf_info) | **PATCH** /udf/{namespace}/{name} | 


# **delete_udf_info**
> delete_udf_info(namespace, name)



delete a registerd UDF, this will remove all sharing and can not be undone

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
    api_instance = tiledb.cloud.rest_api.UdfApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
name = 'name_example' # str | name to register udf under

    try:
        api_instance.delete_udf_info(namespace, name)
    except ApiException as e:
        print("Exception when calling UdfApi->delete_udf_info: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.UdfApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
name = 'name_example' # str | name to register udf under

    try:
        api_instance.delete_udf_info(namespace, name)
    except ApiException as e:
        print("Exception when calling UdfApi->delete_udf_info: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **name** | **str**| name to register udf under | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | UDF delete successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_udf_info**
> UDFInfo get_udf_info(namespace, name)



get a specific UDF in the given namespace

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
    api_instance = tiledb.cloud.rest_api.UdfApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
name = 'name_example' # str | name to register udf under

    try:
        api_response = api_instance.get_udf_info(namespace, name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UdfApi->get_udf_info: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.UdfApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
name = 'name_example' # str | name to register udf under

    try:
        api_response = api_instance.get_udf_info(namespace, name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UdfApi->get_udf_info: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **name** | **str**| name to register udf under | 

### Return type

[**UDFInfo**](UDFInfo.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | UDFInfo was retrieved successfully |  -  |
**404** | udf not found |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_udf_info_sharing_policies**
> list[UDFSharing] get_udf_info_sharing_policies(namespace, name)



Get all sharing details of the udf

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
    api_instance = tiledb.cloud.rest_api.UdfApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
name = 'name_example' # str | name of UDFInfo

    try:
        api_response = api_instance.get_udf_info_sharing_policies(namespace, name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UdfApi->get_udf_info_sharing_policies: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.UdfApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
name = 'name_example' # str | name of UDFInfo

    try:
        api_response = api_instance.get_udf_info_sharing_policies(namespace, name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UdfApi->get_udf_info_sharing_policies: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **name** | **str**| name of UDFInfo | 

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

# **register_udf_info**
> register_udf_info(namespace, name, udf)



register a UDF in the given namespace

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
    api_instance = tiledb.cloud.rest_api.UdfApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
name = 'name_example' # str | name to register udf under
udf = tiledb.cloud.rest_api.UDFInfoUpdate() # UDFInfoUpdate | udf to register

    try:
        api_instance.register_udf_info(namespace, name, udf)
    except ApiException as e:
        print("Exception when calling UdfApi->register_udf_info: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.UdfApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
name = 'name_example' # str | name to register udf under
udf = tiledb.cloud.rest_api.UDFInfoUpdate() # UDFInfoUpdate | udf to register

    try:
        api_instance.register_udf_info(namespace, name, udf)
    except ApiException as e:
        print("Exception when calling UdfApi->register_udf_info: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **name** | **str**| name to register udf under | 
 **udf** | [**UDFInfoUpdate**](UDFInfoUpdate.md)| udf to register | 

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

# **share_udf_info**
> share_udf_info(namespace, name, udf_sharing)



Share a UDF with a user

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
    api_instance = tiledb.cloud.rest_api.UdfApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
name = 'name_example' # str | name of UDFInfo
udf_sharing = tiledb.cloud.rest_api.UDFSharing() # UDFSharing | Namespace and list of permissions to share with. An empty list of permissions will remove the namespace, if permissions already exist they will be deleted then new ones added. In the event of a failure, the new polcies will be rolled back to prevent partial policies, and its likely the udf will not be shared with the namespace at all

    try:
        api_instance.share_udf_info(namespace, name, udf_sharing)
    except ApiException as e:
        print("Exception when calling UdfApi->share_udf_info: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.UdfApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
name = 'name_example' # str | name of UDFInfo
udf_sharing = tiledb.cloud.rest_api.UDFSharing() # UDFSharing | Namespace and list of permissions to share with. An empty list of permissions will remove the namespace, if permissions already exist they will be deleted then new ones added. In the event of a failure, the new polcies will be rolled back to prevent partial policies, and its likely the udf will not be shared with the namespace at all

    try:
        api_instance.share_udf_info(namespace, name, udf_sharing)
    except ApiException as e:
        print("Exception when calling UdfApi->share_udf_info: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **name** | **str**| name of UDFInfo | 
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



submit a generic UDF in the given namespace

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
    api_instance = tiledb.cloud.rest_api.UdfApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
udf = tiledb.cloud.rest_api.GenericUDF() # GenericUDF | udf to run
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
    api_instance = tiledb.cloud.rest_api.UdfApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
udf = tiledb.cloud.rest_api.GenericUDF() # GenericUDF | udf to run
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

# **submit_multi_array_udf**
> file submit_multi_array_udf(namespace, udf, accept_encoding=accept_encoding)



submit a multi-array UDF in the given namespace

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
    api_instance = tiledb.cloud.rest_api.UdfApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
udf = tiledb.cloud.rest_api.MultiArrayUDF() # MultiArrayUDF | udf to run
accept_encoding = 'accept_encoding_example' # str | Encoding to use (optional)

    try:
        api_response = api_instance.submit_multi_array_udf(namespace, udf, accept_encoding=accept_encoding)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UdfApi->submit_multi_array_udf: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.UdfApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
udf = tiledb.cloud.rest_api.MultiArrayUDF() # MultiArrayUDF | udf to run
accept_encoding = 'accept_encoding_example' # str | Encoding to use (optional)

    try:
        api_response = api_instance.submit_multi_array_udf(namespace, udf, accept_encoding=accept_encoding)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UdfApi->submit_multi_array_udf: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **udf** | [**MultiArrayUDF**](MultiArrayUDF.md)| udf to run | 
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
> file submit_udf(namespace, array, udf, x_payer=x_payer, accept_encoding=accept_encoding, v2=v2)



send a UDF to run against a specified array/URI registered to a group/project

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
    api_instance = tiledb.cloud.rest_api.UdfApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
udf = tiledb.cloud.rest_api.MultiArrayUDF() # MultiArrayUDF | udf to run
x_payer = 'x_payer_example' # str | Name of organization or user who should be charged for this request (optional)
accept_encoding = 'accept_encoding_example' # str | Encoding to use (optional)
v2 = 'v2_example' # str | flag to indicate if v2 array udfs should be used, currently in beta testing. Setting any value will enable v2 array udfs (optional)

    try:
        api_response = api_instance.submit_udf(namespace, array, udf, x_payer=x_payer, accept_encoding=accept_encoding, v2=v2)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UdfApi->submit_udf: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.UdfApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
udf = tiledb.cloud.rest_api.MultiArrayUDF() # MultiArrayUDF | udf to run
x_payer = 'x_payer_example' # str | Name of organization or user who should be charged for this request (optional)
accept_encoding = 'accept_encoding_example' # str | Encoding to use (optional)
v2 = 'v2_example' # str | flag to indicate if v2 array udfs should be used, currently in beta testing. Setting any value will enable v2 array udfs (optional)

    try:
        api_response = api_instance.submit_udf(namespace, array, udf, x_payer=x_payer, accept_encoding=accept_encoding, v2=v2)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UdfApi->submit_udf: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **array** | **str**| name/uri of array that is url-encoded | 
 **udf** | [**MultiArrayUDF**](MultiArrayUDF.md)| udf to run | 
 **x_payer** | **str**| Name of organization or user who should be charged for this request | [optional] 
 **accept_encoding** | **str**| Encoding to use | [optional] 
 **v2** | **str**| flag to indicate if v2 array udfs should be used, currently in beta testing. Setting any value will enable v2 array udfs | [optional] 

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

# **udf_namespace_array_versions_get**
> list[int] udf_namespace_array_versions_get(namespace, array)



retrieve a list of timestamps from the array fragment info listing in milliseconds

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
    api_instance = tiledb.cloud.rest_api.UdfApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded

    try:
        api_response = api_instance.udf_namespace_array_versions_get(namespace, array)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UdfApi->udf_namespace_array_versions_get: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.UdfApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded

    try:
        api_response = api_instance.udf_namespace_array_versions_get(namespace, array)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UdfApi->udf_namespace_array_versions_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **array** | **str**| name/uri of array that is url-encoded | 

### Return type

**list[int]**

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | list of timestamps in milliseconds |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_udf_info**
> update_udf_info(namespace, name, udf)



updated an existing registerd UDF in the given namespace

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
    api_instance = tiledb.cloud.rest_api.UdfApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
name = 'name_example' # str | name to register udf under
udf = tiledb.cloud.rest_api.UDFInfoUpdate() # UDFInfoUpdate | udf to update

    try:
        api_instance.update_udf_info(namespace, name, udf)
    except ApiException as e:
        print("Exception when calling UdfApi->update_udf_info: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.UdfApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
name = 'name_example' # str | name to register udf under
udf = tiledb.cloud.rest_api.UDFInfoUpdate() # UDFInfoUpdate | udf to update

    try:
        api_instance.update_udf_info(namespace, name, udf)
    except ApiException as e:
        print("Exception when calling UdfApi->update_udf_info: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) | 
 **name** | **str**| name to register udf under | 
 **udf** | [**UDFInfoUpdate**](UDFInfoUpdate.md)| udf to update | 

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

