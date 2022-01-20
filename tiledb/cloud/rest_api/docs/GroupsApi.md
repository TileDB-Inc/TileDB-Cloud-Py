# tiledb.cloud.rest_api.GroupsApi

All URIs are relative to *http://localhost/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_asset**](GroupsApi.md#add_asset) | **POST** /groups/{namespace}/{name}/{asset_namespace}/{asset_name} | 
[**create_group**](GroupsApi.md#create_group) | **POST** /groups/{namespace}/{name} | 
[**delete_group**](GroupsApi.md#delete_group) | **DELETE** /groups/{namespace}/{name} | 
[**list_group**](GroupsApi.md#list_group) | **GET** /groups/{namespace}/{name} | 
[**list_top_level_groups**](GroupsApi.md#list_top_level_groups) | **GET** /groups/{namespace} | 
[**remove_asset**](GroupsApi.md#remove_asset) | **DELETE** /groups/{namespace}/{name}/{asset_namespace}/{asset_name} | 
[**update_group**](GroupsApi.md#update_group) | **PATCH** /groups/{namespace}/{name} | 


# **add_asset**
> add_asset(namespace, name, asset_namespace, asset_name)



Adds an asset(array, notebook, udf etc) to a group

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
    api_instance = tiledb.cloud.rest_api.GroupsApi(api_client)
    namespace = 'namespace_example' # str | The namespace of the group
name = 'name_example' # str | The name of the group
asset_namespace = 'asset_namespace_example' # str | The namespace of the asset
asset_name = 'asset_name_example' # str | The name of the asset

    try:
        api_instance.add_asset(namespace, name, asset_namespace, asset_name)
    except ApiException as e:
        print("Exception when calling GroupsApi->add_asset: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.GroupsApi(api_client)
    namespace = 'namespace_example' # str | The namespace of the group
name = 'name_example' # str | The name of the group
asset_namespace = 'asset_namespace_example' # str | The namespace of the asset
asset_name = 'asset_name_example' # str | The name of the asset

    try:
        api_instance.add_asset(namespace, name, asset_namespace, asset_name)
    except ApiException as e:
        print("Exception when calling GroupsApi->add_asset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| The namespace of the group | 
 **name** | **str**| The name of the group | 
 **asset_namespace** | **str**| The namespace of the asset | 
 **asset_name** | **str**| The name of the asset | 

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
**204** | asset added successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_group**
> create_group(namespace, name, group_create=group_create)



Creates a new, empty group in the namespace.

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
    api_instance = tiledb.cloud.rest_api.GroupsApi(api_client)
    namespace = 'namespace_example' # str | The namespace of the group
name = 'name_example' # str | The name of the group
group_create = tiledb.cloud.rest_api.GroupCreate() # GroupCreate |  (optional)

    try:
        api_instance.create_group(namespace, name, group_create=group_create)
    except ApiException as e:
        print("Exception when calling GroupsApi->create_group: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.GroupsApi(api_client)
    namespace = 'namespace_example' # str | The namespace of the group
name = 'name_example' # str | The name of the group
group_create = tiledb.cloud.rest_api.GroupCreate() # GroupCreate |  (optional)

    try:
        api_instance.create_group(namespace, name, group_create=group_create)
    except ApiException as e:
        print("Exception when calling GroupsApi->create_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| The namespace of the group | 
 **name** | **str**| The name of the group | 
 **group_create** | [**GroupCreate**](GroupCreate.md)|  | [optional] 

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
**204** | group created successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_group**
> delete_group(namespace, name)



Deletes the group and all the subgroups recursively. The assets are not deleted nor are not relocated to any other group

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
    api_instance = tiledb.cloud.rest_api.GroupsApi(api_client)
    namespace = 'namespace_example' # str | The namespace of the group
name = 'name_example' # str | The name of the group

    try:
        api_instance.delete_group(namespace, name)
    except ApiException as e:
        print("Exception when calling GroupsApi->delete_group: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.GroupsApi(api_client)
    namespace = 'namespace_example' # str | The namespace of the group
name = 'name_example' # str | The name of the group

    try:
        api_instance.delete_group(namespace, name)
    except ApiException as e:
        print("Exception when calling GroupsApi->delete_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| The namespace of the group | 
 **name** | **str**| The name of the group | 

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
**204** | group deleted successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_group**
> GroupListing list_group(namespace, name, output=output, page=page, per_page=per_page)



Returns the contents, assets and subgroups, of the group

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
    api_instance = tiledb.cloud.rest_api.GroupsApi(api_client)
    namespace = 'namespace_example' # str | The namespace of the group
name = 'name_example' # str | The name of the group
output = 'output_example' # str |  (optional)
page = 56 # int | pagination offset for assets (optional)
per_page = 56 # int | pagination limit for assets (optional)

    try:
        api_response = api_instance.list_group(namespace, name, output=output, page=page, per_page=per_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->list_group: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.GroupsApi(api_client)
    namespace = 'namespace_example' # str | The namespace of the group
name = 'name_example' # str | The name of the group
output = 'output_example' # str |  (optional)
page = 56 # int | pagination offset for assets (optional)
per_page = 56 # int | pagination limit for assets (optional)

    try:
        api_response = api_instance.list_group(namespace, name, output=output, page=page, per_page=per_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->list_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| The namespace of the group | 
 **name** | **str**| The name of the group | 
 **output** | **str**|  | [optional] 
 **page** | **int**| pagination offset for assets | [optional] 
 **per_page** | **int**| pagination limit for assets | [optional] 

### Return type

[**GroupListing**](GroupListing.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | the group contents |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_top_level_groups**
> GroupListing list_top_level_groups(namespace, page=page, per_page=per_page)



Returns one page of top level groups in namespace.

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
    api_instance = tiledb.cloud.rest_api.GroupsApi(api_client)
    namespace = 'namespace_example' # str | The namespace to operate on
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        api_response = api_instance.list_top_level_groups(namespace, page=page, per_page=per_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->list_top_level_groups: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.GroupsApi(api_client)
    namespace = 'namespace_example' # str | The namespace to operate on
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        api_response = api_instance.list_top_level_groups(namespace, page=page, per_page=per_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->list_top_level_groups: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| The namespace to operate on | 
 **page** | **int**| pagination offset | [optional] 
 **per_page** | **int**| pagination limit | [optional] 

### Return type

[**GroupListing**](GroupListing.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | the group contents |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_asset**
> remove_asset(namespace, name, asset_namespace, asset_name)



Removes an asset from a group

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
    api_instance = tiledb.cloud.rest_api.GroupsApi(api_client)
    namespace = 'namespace_example' # str | The namespace of the group
name = 'name_example' # str | The name of the group
asset_namespace = 'asset_namespace_example' # str | The namespace of the asset
asset_name = 'asset_name_example' # str | The name of the asset

    try:
        api_instance.remove_asset(namespace, name, asset_namespace, asset_name)
    except ApiException as e:
        print("Exception when calling GroupsApi->remove_asset: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.GroupsApi(api_client)
    namespace = 'namespace_example' # str | The namespace of the group
name = 'name_example' # str | The name of the group
asset_namespace = 'asset_namespace_example' # str | The namespace of the asset
asset_name = 'asset_name_example' # str | The name of the asset

    try:
        api_instance.remove_asset(namespace, name, asset_namespace, asset_name)
    except ApiException as e:
        print("Exception when calling GroupsApi->remove_asset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| The namespace of the group | 
 **name** | **str**| The name of the group | 
 **asset_namespace** | **str**| The namespace of the asset | 
 **asset_name** | **str**| The name of the asset | 

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
**204** | asset removed successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_group**
> update_group(namespace, name, group_update=group_update)



Changes attributes of the group

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
    api_instance = tiledb.cloud.rest_api.GroupsApi(api_client)
    namespace = 'namespace_example' # str | The namespace of the group
name = 'name_example' # str | The name of the group
group_update = tiledb.cloud.rest_api.GroupUpdate() # GroupUpdate |  (optional)

    try:
        api_instance.update_group(namespace, name, group_update=group_update)
    except ApiException as e:
        print("Exception when calling GroupsApi->update_group: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.GroupsApi(api_client)
    namespace = 'namespace_example' # str | The namespace of the group
name = 'name_example' # str | The name of the group
group_update = tiledb.cloud.rest_api.GroupUpdate() # GroupUpdate |  (optional)

    try:
        api_instance.update_group(namespace, name, group_update=group_update)
    except ApiException as e:
        print("Exception when calling GroupsApi->update_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| The namespace of the group | 
 **name** | **str**| The name of the group | 
 **group_update** | [**GroupUpdate**](GroupUpdate.md)|  | [optional] 

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
**204** | attributes changed successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

