# tiledb.cloud.rest_api.GroupsApi

All URIs are relative to *http://localhost/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**deregister_group**](GroupsApi.md#deregister_group) | **DELETE** /groups/{group_namespace}/{group_name} | 
[**groups_group_namespace_group_name_options**](GroupsApi.md#groups_group_namespace_group_name_options) | **OPTIONS** /groups/{group_namespace}/{group_name} | 
[**retrieve_group**](GroupsApi.md#retrieve_group) | **POST** /groups/{group_namespace}/{group_name} | 
[**update_group_contents**](GroupsApi.md#update_group_contents) | **PATCH** /groups/{group_namespace}/{group_name} | 


# **deregister_group**
> deregister_group(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name)



Deregisters a group

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
    api_instance = tiledb.cloud.rest_api.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)

    try:
        api_instance.deregister_group(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name)
    except ApiException as e:
        print("Exception when calling GroupsApi->deregister_group: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)

    try:
        api_instance.deregister_group(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name)
    except ApiException as e:
        print("Exception when calling GroupsApi->deregister_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_namespace** | **str**| The namespace of the group | 
 **group_name** | **str**| The unique name or id of the group | 
 **x_tiledb_cloud_access_credentials_name** | **str**| Optional registered access credentials to use for creation | [optional] 

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
**200** | group deregistered successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **groups_group_namespace_group_name_options**
> groups_group_namespace_group_name_options(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name)



can be used to check if the resource exists

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
    api_instance = tiledb.cloud.rest_api.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)

    try:
        api_instance.groups_group_namespace_group_name_options(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name)
    except ApiException as e:
        print("Exception when calling GroupsApi->groups_group_namespace_group_name_options: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)

    try:
        api_instance.groups_group_namespace_group_name_options(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name)
    except ApiException as e:
        print("Exception when calling GroupsApi->groups_group_namespace_group_name_options: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_namespace** | **str**| The namespace of the group | 
 **group_name** | **str**| The unique name or id of the group | 
 **x_tiledb_cloud_access_credentials_name** | **str**| Optional registered access credentials to use for creation | [optional] 

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
**204** | the resource exists |  -  |
**404** | the resource does not exist |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_group**
> GroupContentsRetrievalResponse retrieve_group(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, group_retrieval=group_retrieval)



Retrieves the contents of a group

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
    api_instance = tiledb.cloud.rest_api.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)
group_retrieval = tiledb.cloud.rest_api.GroupContentsRetrievalRequest() # GroupContentsRetrievalRequest |  (optional)

    try:
        api_response = api_instance.retrieve_group(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, group_retrieval=group_retrieval)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->retrieve_group: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)
group_retrieval = tiledb.cloud.rest_api.GroupContentsRetrievalRequest() # GroupContentsRetrievalRequest |  (optional)

    try:
        api_response = api_instance.retrieve_group(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, group_retrieval=group_retrieval)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->retrieve_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_namespace** | **str**| The namespace of the group | 
 **group_name** | **str**| The unique name or id of the group | 
 **x_tiledb_cloud_access_credentials_name** | **str**| Optional registered access credentials to use for creation | [optional] 
 **group_retrieval** | [**GroupContentsRetrievalRequest**](GroupContentsRetrievalRequest.md)|  | [optional] 

### Return type

[**GroupContentsRetrievalResponse**](GroupContentsRetrievalResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | group created successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_group_contents**
> update_group_contents(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, group_update_contents=group_update_contents)



Change the contents of the group

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
    api_instance = tiledb.cloud.rest_api.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)
group_update_contents = tiledb.cloud.rest_api.GroupContentsChangesRequest() # GroupContentsChangesRequest |  (optional)

    try:
        api_instance.update_group_contents(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, group_update_contents=group_update_contents)
    except ApiException as e:
        print("Exception when calling GroupsApi->update_group_contents: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)
group_update_contents = tiledb.cloud.rest_api.GroupContentsChangesRequest() # GroupContentsChangesRequest |  (optional)

    try:
        api_instance.update_group_contents(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, group_update_contents=group_update_contents)
    except ApiException as e:
        print("Exception when calling GroupsApi->update_group_contents: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_namespace** | **str**| The namespace of the group | 
 **group_name** | **str**| The unique name or id of the group | 
 **x_tiledb_cloud_access_credentials_name** | **str**| Optional registered access credentials to use for creation | [optional] 
 **group_update_contents** | [**GroupContentsChangesRequest**](GroupContentsChangesRequest.md)|  | [optional] 

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

