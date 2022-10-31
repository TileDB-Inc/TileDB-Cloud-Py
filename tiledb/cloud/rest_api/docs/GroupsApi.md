# tiledb.cloud.rest_api.GroupsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**change_group_contents**](GroupsApi.md#change_group_contents) | **POST** /v1/groups/{group_namespace}/{group_name}/contents | 
[**create_group**](GroupsApi.md#create_group) | **POST** /v1/groups/{namespace}/create | 
[**delete_group**](GroupsApi.md#delete_group) | **DELETE** /v1/groups/{group_namespace}/{group_name} | 
[**get_group**](GroupsApi.md#get_group) | **GET** /v1/groups/{group_namespace}/{group_name} | 
[**get_group_contents**](GroupsApi.md#get_group_contents) | **GET** /v1/groups/{group_namespace}/{group_name}/contents | 
[**get_group_sharing_policies**](GroupsApi.md#get_group_sharing_policies) | **GET** /v1/groups/{group_namespace}/{group_name}/share | 
[**groups_browser_owned_filters_get**](GroupsApi.md#groups_browser_owned_filters_get) | **GET** /v1/groups/browser/owned/filters | 
[**groups_browser_public_filters_get**](GroupsApi.md#groups_browser_public_filters_get) | **GET** /v1/groups/browser/public/filters | 
[**groups_browser_shared_filters_get**](GroupsApi.md#groups_browser_shared_filters_get) | **GET** /v1/groups/browser/shared/filters | 
[**groups_group_namespace_group_name_contents_filters_get**](GroupsApi.md#groups_group_namespace_group_name_contents_filters_get) | **GET** /v1/groups/{group_namespace}/{group_name}/contents/filters | 
[**list_owned_groups**](GroupsApi.md#list_owned_groups) | **GET** /v1/groups/browser/owned | 
[**list_public_groups**](GroupsApi.md#list_public_groups) | **GET** /v1/groups/browser/public | 
[**list_shared_groups**](GroupsApi.md#list_shared_groups) | **GET** /v1/groups/browser/shared | 
[**register_group**](GroupsApi.md#register_group) | **POST** /v1/groups/{namespace}/{array}/register | 
[**share_group**](GroupsApi.md#share_group) | **PATCH** /v1/groups/{group_namespace}/{group_name}/share | 
[**update_group**](GroupsApi.md#update_group) | **PATCH** /v1/groups/{group_namespace}/{group_name} | 


# **change_group_contents**
> change_group_contents(group_namespace, group_name, group_changes=group_changes)



Changes the contents of the group by adding/removing members.

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
group_changes = tiledb.cloud.rest_api.GroupChanges() # GroupChanges |  (optional)

    try:
        api_instance.change_group_contents(group_namespace, group_name, group_changes=group_changes)
    except ApiException as e:
        print("Exception when calling GroupsApi->change_group_contents: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
group_changes = tiledb.cloud.rest_api.GroupChanges() # GroupChanges |  (optional)

    try:
        api_instance.change_group_contents(group_namespace, group_name, group_changes=group_changes)
    except ApiException as e:
        print("Exception when calling GroupsApi->change_group_contents: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_namespace** | **str**| The namespace of the group | 
 **group_name** | **str**| The unique name or id of the group | 
 **group_changes** | [**GroupChanges**](GroupChanges.md)|  | [optional] 

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
**204** | all changes applied successfully |  -  |
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_group**
> create_group(namespace, group_create=group_create)



Creates a new group in the namespace.

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
group_create = tiledb.cloud.rest_api.GroupCreate() # GroupCreate |  (optional)

    try:
        api_instance.create_group(namespace, group_create=group_create)
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
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
group_create = tiledb.cloud.rest_api.GroupCreate() # GroupCreate |  (optional)

    try:
        api_instance.create_group(namespace, group_create=group_create)
    except ApiException as e:
        print("Exception when calling GroupsApi->create_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| The namespace of the group | 
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
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_group**
> delete_group(group_namespace, group_name)



Deletes the group. The assets are not deleted nor are not relocated to any other group

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group

    try:
        api_instance.delete_group(group_namespace, group_name)
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
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group

    try:
        api_instance.delete_group(group_namespace, group_name)
    except ApiException as e:
        print("Exception when calling GroupsApi->delete_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_namespace** | **str**| The namespace of the group | 
 **group_name** | **str**| The unique name or id of the group | 

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
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_group**
> GroupInfo get_group(group_namespace, group_name)



Returns the the group

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group

    try:
        api_response = api_instance.get_group(group_namespace, group_name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->get_group: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group

    try:
        api_response = api_instance.get_group(group_namespace, group_name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->get_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_namespace** | **str**| The namespace of the group | 
 **group_name** | **str**| The unique name or id of the group | 

### Return type

[**GroupInfo**](GroupInfo.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | the group metadata |  -  |
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_group_contents**
> GroupContents get_group_contents(group_namespace, group_name, page=page, per_page=per_page, namespace=namespace, search=search, orderby=orderby, tag=tag, exclude_tag=exclude_tag, member_type=member_type, exclude_member_type=exclude_member_type)



Returns the contents of the group

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
page = 56 # int | pagination offset for assets (optional)
per_page = 56 # int | pagination limit for assets (optional)
namespace = 'namespace_example' # str | namespace to search for (optional)
search = 'search_example' # str | search string that will look at name, namespace or description fields (optional)
orderby = 'orderby_example' # str | sort by which field valid values include last_accessed, size, name (optional)
tag = ['tag_example'] # list[str] | tag to search for, more than one can be included (optional)
exclude_tag = ['exclude_tag_example'] # list[str] | tags to exclude matching array in results, more than one can be included (optional)
member_type = ['member_type_example'] # list[str] | member type to search for, more than one can be included (optional)
exclude_member_type = ['exclude_member_type_example'] # list[str] | member type to exclude matching groups in results, more than one can be included (optional)

    try:
        api_response = api_instance.get_group_contents(group_namespace, group_name, page=page, per_page=per_page, namespace=namespace, search=search, orderby=orderby, tag=tag, exclude_tag=exclude_tag, member_type=member_type, exclude_member_type=exclude_member_type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->get_group_contents: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
page = 56 # int | pagination offset for assets (optional)
per_page = 56 # int | pagination limit for assets (optional)
namespace = 'namespace_example' # str | namespace to search for (optional)
search = 'search_example' # str | search string that will look at name, namespace or description fields (optional)
orderby = 'orderby_example' # str | sort by which field valid values include last_accessed, size, name (optional)
tag = ['tag_example'] # list[str] | tag to search for, more than one can be included (optional)
exclude_tag = ['exclude_tag_example'] # list[str] | tags to exclude matching array in results, more than one can be included (optional)
member_type = ['member_type_example'] # list[str] | member type to search for, more than one can be included (optional)
exclude_member_type = ['exclude_member_type_example'] # list[str] | member type to exclude matching groups in results, more than one can be included (optional)

    try:
        api_response = api_instance.get_group_contents(group_namespace, group_name, page=page, per_page=per_page, namespace=namespace, search=search, orderby=orderby, tag=tag, exclude_tag=exclude_tag, member_type=member_type, exclude_member_type=exclude_member_type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->get_group_contents: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_namespace** | **str**| The namespace of the group | 
 **group_name** | **str**| The unique name or id of the group | 
 **page** | **int**| pagination offset for assets | [optional] 
 **per_page** | **int**| pagination limit for assets | [optional] 
 **namespace** | **str**| namespace to search for | [optional] 
 **search** | **str**| search string that will look at name, namespace or description fields | [optional] 
 **orderby** | **str**| sort by which field valid values include last_accessed, size, name | [optional] 
 **tag** | [**list[str]**](str.md)| tag to search for, more than one can be included | [optional] 
 **exclude_tag** | [**list[str]**](str.md)| tags to exclude matching array in results, more than one can be included | [optional] 
 **member_type** | [**list[str]**](str.md)| member type to search for, more than one can be included | [optional] 
 **exclude_member_type** | [**list[str]**](str.md)| member type to exclude matching groups in results, more than one can be included | [optional] 

### Return type

[**GroupContents**](GroupContents.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | the group contents |  -  |
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_group_sharing_policies**
> list[GroupSharing] get_group_sharing_policies(group_namespace, group_name)



Get all sharing details of the group

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group

    try:
        api_response = api_instance.get_group_sharing_policies(group_namespace, group_name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->get_group_sharing_policies: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group

    try:
        api_response = api_instance.get_group_sharing_policies(group_namespace, group_name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->get_group_sharing_policies: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_namespace** | **str**| The namespace of the group | 
 **group_name** | **str**| The unique name or id of the group | 

### Return type

[**list[GroupSharing]**](GroupSharing.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of all specific sharing policies |  -  |
**404** | Group does not exist or user does not have permissions to view group-sharing policies |  -  |
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **groups_browser_owned_filters_get**
> GroupBrowserFilterData groups_browser_owned_filters_get()



Fetch data to initialize filters for the groups browser

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    
    try:
        api_response = api_instance.groups_browser_owned_filters_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->groups_browser_owned_filters_get: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    
    try:
        api_response = api_instance.groups_browser_owned_filters_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->groups_browser_owned_filters_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**GroupBrowserFilterData**](GroupBrowserFilterData.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Filter data |  -  |
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **groups_browser_public_filters_get**
> GroupBrowserFilterData groups_browser_public_filters_get()



Fetch data to initialize filters for the groups browser

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    
    try:
        api_response = api_instance.groups_browser_public_filters_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->groups_browser_public_filters_get: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    
    try:
        api_response = api_instance.groups_browser_public_filters_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->groups_browser_public_filters_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**GroupBrowserFilterData**](GroupBrowserFilterData.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Filter data |  -  |
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **groups_browser_shared_filters_get**
> GroupBrowserFilterData groups_browser_shared_filters_get()



Fetch data to initialize filters for the groups browser

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    
    try:
        api_response = api_instance.groups_browser_shared_filters_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->groups_browser_shared_filters_get: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    
    try:
        api_response = api_instance.groups_browser_shared_filters_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->groups_browser_shared_filters_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**GroupBrowserFilterData**](GroupBrowserFilterData.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Filter data |  -  |
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **groups_group_namespace_group_name_contents_filters_get**
> GroupContentsFilterData groups_group_namespace_group_name_contents_filters_get(group_namespace, group_name)



Fetch data to initialize filters for the group contents

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group

    try:
        api_response = api_instance.groups_group_namespace_group_name_contents_filters_get(group_namespace, group_name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->groups_group_namespace_group_name_contents_filters_get: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group

    try:
        api_response = api_instance.groups_group_namespace_group_name_contents_filters_get(group_namespace, group_name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->groups_group_namespace_group_name_contents_filters_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_namespace** | **str**| The namespace of the group | 
 **group_name** | **str**| The unique name or id of the group | 

### Return type

[**GroupContentsFilterData**](GroupContentsFilterData.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Filter data |  -  |
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_owned_groups**
> GroupBrowserData list_owned_groups(page=page, per_page=per_page, search=search, namespace=namespace, orderby=orderby, permissions=permissions, tag=tag, exclude_tag=exclude_tag, flat=flat, parent=parent)



Returns one page of owned groups.

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
search = 'search_example' # str | search string that will look at name, namespace or description fields (optional)
namespace = 'namespace_example' # str | namespace (optional)
orderby = 'orderby_example' # str | sort by which field valid values include last_accessed, size, name (optional)
permissions = 'permissions_example' # str | permissions valid values include read, read_write, write, admin (optional)
tag = ['tag_example'] # list[str] | tag to search for, more than one can be included (optional)
exclude_tag = ['exclude_tag_example'] # list[str] | tags to exclude matching array in results, more than one can be included (optional)
flat = True # bool | if true, ignores the nesting of groups and searches all of them (optional)
parent = 'parent_example' # str | search only the children of the groups with this uuid (optional)

    try:
        api_response = api_instance.list_owned_groups(page=page, per_page=per_page, search=search, namespace=namespace, orderby=orderby, permissions=permissions, tag=tag, exclude_tag=exclude_tag, flat=flat, parent=parent)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->list_owned_groups: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
search = 'search_example' # str | search string that will look at name, namespace or description fields (optional)
namespace = 'namespace_example' # str | namespace (optional)
orderby = 'orderby_example' # str | sort by which field valid values include last_accessed, size, name (optional)
permissions = 'permissions_example' # str | permissions valid values include read, read_write, write, admin (optional)
tag = ['tag_example'] # list[str] | tag to search for, more than one can be included (optional)
exclude_tag = ['exclude_tag_example'] # list[str] | tags to exclude matching array in results, more than one can be included (optional)
flat = True # bool | if true, ignores the nesting of groups and searches all of them (optional)
parent = 'parent_example' # str | search only the children of the groups with this uuid (optional)

    try:
        api_response = api_instance.list_owned_groups(page=page, per_page=per_page, search=search, namespace=namespace, orderby=orderby, permissions=permissions, tag=tag, exclude_tag=exclude_tag, flat=flat, parent=parent)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->list_owned_groups: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| pagination offset | [optional] 
 **per_page** | **int**| pagination limit | [optional] 
 **search** | **str**| search string that will look at name, namespace or description fields | [optional] 
 **namespace** | **str**| namespace | [optional] 
 **orderby** | **str**| sort by which field valid values include last_accessed, size, name | [optional] 
 **permissions** | **str**| permissions valid values include read, read_write, write, admin | [optional] 
 **tag** | [**list[str]**](str.md)| tag to search for, more than one can be included | [optional] 
 **exclude_tag** | [**list[str]**](str.md)| tags to exclude matching array in results, more than one can be included | [optional] 
 **flat** | **bool**| if true, ignores the nesting of groups and searches all of them | [optional] 
 **parent** | **str**| search only the children of the groups with this uuid | [optional] 

### Return type

[**GroupBrowserData**](GroupBrowserData.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | the group contents |  -  |
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_public_groups**
> GroupBrowserData list_public_groups(page=page, per_page=per_page, search=search, namespace=namespace, orderby=orderby, permissions=permissions, tag=tag, exclude_tag=exclude_tag, flat=flat, parent=parent)



Returns one page of public groups.

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
search = 'search_example' # str | search string that will look at name, namespace or description fields (optional)
namespace = 'namespace_example' # str | namespace (optional)
orderby = 'orderby_example' # str | sort by which field valid values include last_accessed, size, name (optional)
permissions = 'permissions_example' # str | permissions valid values include read, read_write, write, admin (optional)
tag = ['tag_example'] # list[str] | tag to search for, more than one can be included (optional)
exclude_tag = ['exclude_tag_example'] # list[str] | tags to exclude matching array in results, more than one can be included (optional)
flat = True # bool | if true, ignores the nesting of groups and searches all of them (optional)
parent = 'parent_example' # str | search only the children of the groups with this uuid (optional)

    try:
        api_response = api_instance.list_public_groups(page=page, per_page=per_page, search=search, namespace=namespace, orderby=orderby, permissions=permissions, tag=tag, exclude_tag=exclude_tag, flat=flat, parent=parent)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->list_public_groups: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
search = 'search_example' # str | search string that will look at name, namespace or description fields (optional)
namespace = 'namespace_example' # str | namespace (optional)
orderby = 'orderby_example' # str | sort by which field valid values include last_accessed, size, name (optional)
permissions = 'permissions_example' # str | permissions valid values include read, read_write, write, admin (optional)
tag = ['tag_example'] # list[str] | tag to search for, more than one can be included (optional)
exclude_tag = ['exclude_tag_example'] # list[str] | tags to exclude matching array in results, more than one can be included (optional)
flat = True # bool | if true, ignores the nesting of groups and searches all of them (optional)
parent = 'parent_example' # str | search only the children of the groups with this uuid (optional)

    try:
        api_response = api_instance.list_public_groups(page=page, per_page=per_page, search=search, namespace=namespace, orderby=orderby, permissions=permissions, tag=tag, exclude_tag=exclude_tag, flat=flat, parent=parent)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->list_public_groups: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| pagination offset | [optional] 
 **per_page** | **int**| pagination limit | [optional] 
 **search** | **str**| search string that will look at name, namespace or description fields | [optional] 
 **namespace** | **str**| namespace | [optional] 
 **orderby** | **str**| sort by which field valid values include last_accessed, size, name | [optional] 
 **permissions** | **str**| permissions valid values include read, read_write, write, admin | [optional] 
 **tag** | [**list[str]**](str.md)| tag to search for, more than one can be included | [optional] 
 **exclude_tag** | [**list[str]**](str.md)| tags to exclude matching array in results, more than one can be included | [optional] 
 **flat** | **bool**| if true, ignores the nesting of groups and searches all of them | [optional] 
 **parent** | **str**| search only the children of the groups with this uuid | [optional] 

### Return type

[**GroupBrowserData**](GroupBrowserData.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | the group contents |  -  |
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_shared_groups**
> GroupBrowserData list_shared_groups(page=page, per_page=per_page, search=search, namespace=namespace, orderby=orderby, permissions=permissions, tag=tag, exclude_tag=exclude_tag, flat=flat, parent=parent, shared_to=shared_to)



Returns one page of shared groups.

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
search = 'search_example' # str | search string that will look at name, namespace or description fields (optional)
namespace = 'namespace_example' # str | namespace (optional)
orderby = 'orderby_example' # str | sort by which field valid values include last_accessed, size, name (optional)
permissions = 'permissions_example' # str | permissions valid values include read, read_write, write, admin (optional)
tag = ['tag_example'] # list[str] | tag to search for, more than one can be included (optional)
exclude_tag = ['exclude_tag_example'] # list[str] | tags to exclude matching array in results, more than one can be included (optional)
flat = True # bool | if true, ignores the nesting of groups and searches all of them (optional)
parent = 'parent_example' # str | search only the children of the groups with this uuid (optional)
shared_to = ['shared_to_example'] # list[str] | namespaces to filter results of where there groups were shared to (optional)

    try:
        api_response = api_instance.list_shared_groups(page=page, per_page=per_page, search=search, namespace=namespace, orderby=orderby, permissions=permissions, tag=tag, exclude_tag=exclude_tag, flat=flat, parent=parent, shared_to=shared_to)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->list_shared_groups: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
search = 'search_example' # str | search string that will look at name, namespace or description fields (optional)
namespace = 'namespace_example' # str | namespace (optional)
orderby = 'orderby_example' # str | sort by which field valid values include last_accessed, size, name (optional)
permissions = 'permissions_example' # str | permissions valid values include read, read_write, write, admin (optional)
tag = ['tag_example'] # list[str] | tag to search for, more than one can be included (optional)
exclude_tag = ['exclude_tag_example'] # list[str] | tags to exclude matching array in results, more than one can be included (optional)
flat = True # bool | if true, ignores the nesting of groups and searches all of them (optional)
parent = 'parent_example' # str | search only the children of the groups with this uuid (optional)
shared_to = ['shared_to_example'] # list[str] | namespaces to filter results of where there groups were shared to (optional)

    try:
        api_response = api_instance.list_shared_groups(page=page, per_page=per_page, search=search, namespace=namespace, orderby=orderby, permissions=permissions, tag=tag, exclude_tag=exclude_tag, flat=flat, parent=parent, shared_to=shared_to)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->list_shared_groups: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| pagination offset | [optional] 
 **per_page** | **int**| pagination limit | [optional] 
 **search** | **str**| search string that will look at name, namespace or description fields | [optional] 
 **namespace** | **str**| namespace | [optional] 
 **orderby** | **str**| sort by which field valid values include last_accessed, size, name | [optional] 
 **permissions** | **str**| permissions valid values include read, read_write, write, admin | [optional] 
 **tag** | [**list[str]**](str.md)| tag to search for, more than one can be included | [optional] 
 **exclude_tag** | [**list[str]**](str.md)| tags to exclude matching array in results, more than one can be included | [optional] 
 **flat** | **bool**| if true, ignores the nesting of groups and searches all of them | [optional] 
 **parent** | **str**| search only the children of the groups with this uuid | [optional] 
 **shared_to** | [**list[str]**](str.md)| namespaces to filter results of where there groups were shared to | [optional] 

### Return type

[**GroupBrowserData**](GroupBrowserData.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | the group contents |  -  |
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **register_group**
> register_group(namespace, array, group_register=group_register)



Registers an existing group in the namespace.

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
array = 'array_example' # str | The unique name or id of the group
group_register = tiledb.cloud.rest_api.GroupRegister() # GroupRegister |  (optional)

    try:
        api_instance.register_group(namespace, array, group_register=group_register)
    except ApiException as e:
        print("Exception when calling GroupsApi->register_group: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
array = 'array_example' # str | The unique name or id of the group
group_register = tiledb.cloud.rest_api.GroupRegister() # GroupRegister |  (optional)

    try:
        api_instance.register_group(namespace, array, group_register=group_register)
    except ApiException as e:
        print("Exception when calling GroupsApi->register_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| The namespace of the group | 
 **array** | **str**| The unique name or id of the group | 
 **group_register** | [**GroupRegister**](GroupRegister.md)|  | [optional] 

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
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **share_group**
> share_group(group_namespace, group_name, group_sharing_request)



Share a group with a namespace

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
group_sharing_request = tiledb.cloud.rest_api.GroupSharingRequest() # GroupSharingRequest | Namespace and list of permissions to share with. Sharing is recursive, it is applied to all reachable subgroups and arrays of the group. An empty list of permissions will remove the namespace; if permissions already exist they will be deleted then new ones added. In the event of a failure, the new policies will be rolled back to prevent partial policies, and it's likely the group will not be shared with the namespace at all.

    try:
        api_instance.share_group(group_namespace, group_name, group_sharing_request)
    except ApiException as e:
        print("Exception when calling GroupsApi->share_group: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
group_sharing_request = tiledb.cloud.rest_api.GroupSharingRequest() # GroupSharingRequest | Namespace and list of permissions to share with. Sharing is recursive, it is applied to all reachable subgroups and arrays of the group. An empty list of permissions will remove the namespace; if permissions already exist they will be deleted then new ones added. In the event of a failure, the new policies will be rolled back to prevent partial policies, and it's likely the group will not be shared with the namespace at all.

    try:
        api_instance.share_group(group_namespace, group_name, group_sharing_request)
    except ApiException as e:
        print("Exception when calling GroupsApi->share_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_namespace** | **str**| The namespace of the group | 
 **group_name** | **str**| The unique name or id of the group | 
 **group_sharing_request** | [**GroupSharingRequest**](GroupSharingRequest.md)| Namespace and list of permissions to share with. Sharing is recursive, it is applied to all reachable subgroups and arrays of the group. An empty list of permissions will remove the namespace; if permissions already exist they will be deleted then new ones added. In the event of a failure, the new policies will be rolled back to prevent partial policies, and it&#39;s likely the group will not be shared with the namespace at all. | 

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
**204** | Group shared successfully |  -  |
**404** | Group does not exist or user does not have permissions to share group |  -  |
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_group**
> update_group(group_namespace, group_name, group_update=group_update)



Changes attributes of the group

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
group_update = tiledb.cloud.rest_api.GroupUpdate() # GroupUpdate |  (optional)

    try:
        api_instance.update_group(group_namespace, group_name, group_update=group_update)
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
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud.rest_api.Configuration(
    host = "http://localhost",
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
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
group_update = tiledb.cloud.rest_api.GroupUpdate() # GroupUpdate |  (optional)

    try:
        api_instance.update_group(group_namespace, group_name, group_update=group_update)
    except ApiException as e:
        print("Exception when calling GroupsApi->update_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_namespace** | **str**| The namespace of the group | 
 **group_name** | **str**| The unique name or id of the group | 
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
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

