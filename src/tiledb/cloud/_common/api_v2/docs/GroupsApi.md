# tiledb.cloud.\_common.api_v2.GroupsApi

All URIs are relative to _http://localhost_

| Method                                                                                                  | HTTP request                                                       | Description |
| ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | ----------- |
| [**create_group**](GroupsApi.md#create_group)                                                           | **POST** /v2/groups/{group_namespace}                              |
| [**delete_group**](GroupsApi.md#delete_group)                                                           | **DELETE** /v2/groups/{group_namespace}/{group_name}/delete        |
| [**deregister_group**](GroupsApi.md#deregister_group)                                                   | **DELETE** /v2/groups/{group_namespace}/{group_name}               |
| [**get_group_activity**](GroupsApi.md#get_group_activity)                                               | **GET** /v2/groups/{group_namespace}/{group_name}/activity         |
| [**get_group_content_activity**](GroupsApi.md#get_group_content_activity)                               | **GET** /v2/groups/{group_namespace}/{group_name}/content_activity |
| [**get_group_metadata**](GroupsApi.md#get_group_metadata)                                               | **POST** /v2/groups/{group_namespace}/{group_name}/metadata        |
| [**groups_group_namespace_group_name_options**](GroupsApi.md#groups_group_namespace_group_name_options) | **OPTIONS** /v2/groups/{group_namespace}/{group_name}              |
| [**register_group**](GroupsApi.md#register_group)                                                       | **PUT** /v2/groups/{group_namespace}                               |
| [**retrieve_group**](GroupsApi.md#retrieve_group)                                                       | **POST** /v2/groups/{group_namespace}/{group_name}                 |
| [**update_group_contents**](GroupsApi.md#update_group_contents)                                         | **PATCH** /v2/groups/{group_namespace}/{group_name}                |
| [**update_group_metadata**](GroupsApi.md#update_group_metadata)                                         | **PUT** /v2/groups/{group_namespace}/{group_name}/metadata         |

# **create_group**

> GroupCreationResponse create_group(group_namespace, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, group_creation=group_creation)

Creates an empty group

### Example

- Api Key Authentication (ApiKeyAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)
group_creation = tiledb.cloud._common.api_v2.GroupCreationRequest() # GroupCreationRequest |  (optional)

    try:
        api_response = api_instance.create_group(group_namespace, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, group_creation=group_creation)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->create_group: %s\n" % e)
```

- Basic Authentication (BasicAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)
group_creation = tiledb.cloud._common.api_v2.GroupCreationRequest() # GroupCreationRequest |  (optional)

    try:
        api_response = api_instance.create_group(group_namespace, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, group_creation=group_creation)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->create_group: %s\n" % e)
```

### Parameters

| Name                                       | Type                                                | Description                                                | Notes      |
| ------------------------------------------ | --------------------------------------------------- | ---------------------------------------------------------- | ---------- |
| **group_namespace**                        | **str**                                             | The namespace of the group                                 |
| **x_tiledb_cloud_access_credentials_name** | **str**                                             | Optional registered access credentials to use for creation | [optional] |
| **group_creation**                         | [**GroupCreationRequest**](GroupCreationRequest.md) |                                                            | [optional] |

### Return type

[**GroupCreationResponse**](GroupCreationResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description                | Response headers |
| ----------- | -------------------------- | ---------------- |
| **201**     | group created successfully | -                |
| **502**     | Bad Gateway                | -                |
| **0**       | error response             | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_group**

> delete_group(group_namespace, group_name, recursive=recursive)

Deregisters and physically deletes a group

### Example

- Api Key Authentication (ApiKeyAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
recursive = 'recursive_example' # str | If true, it descends in the group and deletes every subgroup and subarray (optional)

    try:
        api_instance.delete_group(group_namespace, group_name, recursive=recursive)
    except ApiException as e:
        print("Exception when calling GroupsApi->delete_group: %s\n" % e)
```

- Basic Authentication (BasicAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
recursive = 'recursive_example' # str | If true, it descends in the group and deletes every subgroup and subarray (optional)

    try:
        api_instance.delete_group(group_namespace, group_name, recursive=recursive)
    except ApiException as e:
        print("Exception when calling GroupsApi->delete_group: %s\n" % e)
```

### Parameters

| Name                | Type    | Description                                                               | Notes      |
| ------------------- | ------- | ------------------------------------------------------------------------- | ---------- |
| **group_namespace** | **str** | The namespace of the group                                                |
| **group_name**      | **str** | The unique name or id of the group                                        |
| **recursive**       | **str** | If true, it descends in the group and deletes every subgroup and subarray | [optional] |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description                | Response headers |
| ----------- | -------------------------- | ---------------- |
| **204**     | group deleted successfully | -                |
| **502**     | Bad Gateway                | -                |
| **0**       | error response             | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deregister_group**

> deregister_group(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, recursive=recursive)

Deregisters a group

### Example

- Api Key Authentication (ApiKeyAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)
recursive = 'recursive_example' # str | If true, it descends in the group and deregisters every subgroup and subarray (optional)

    try:
        api_instance.deregister_group(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, recursive=recursive)
    except ApiException as e:
        print("Exception when calling GroupsApi->deregister_group: %s\n" % e)
```

- Basic Authentication (BasicAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)
recursive = 'recursive_example' # str | If true, it descends in the group and deregisters every subgroup and subarray (optional)

    try:
        api_instance.deregister_group(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, recursive=recursive)
    except ApiException as e:
        print("Exception when calling GroupsApi->deregister_group: %s\n" % e)
```

### Parameters

| Name                                       | Type    | Description                                                                   | Notes      |
| ------------------------------------------ | ------- | ----------------------------------------------------------------------------- | ---------- |
| **group_namespace**                        | **str** | The namespace of the group                                                    |
| **group_name**                             | **str** | The unique name or id of the group                                            |
| **x_tiledb_cloud_access_credentials_name** | **str** | Optional registered access credentials to use for creation                    | [optional] |
| **recursive**                              | **str** | If true, it descends in the group and deregisters every subgroup and subarray | [optional] |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description                     | Response headers |
| ----------- | ------------------------------- | ---------------- |
| **200**     | group deregistered successfully | -                |
| **502**     | Bad Gateway                     | -                |
| **0**       | error response                  | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_group_activity**

> GroupActivityResponse get_group_activity(group_namespace, group_name, start=start, end=end, page=page, per_page=per_page)

Retrieves activity logs for all assets contained in a group (arrays and other groups) including the parent group itself.

### Example

- Api Key Authentication (ApiKeyAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | namespace group is in (an organization name or user's username)
group_name = 'group_name_example' # str | name/uri of group that is url-encoded
start = 56 # int | Start time of window of fetch logs, unix epoch in seconds (default: seven days ago) (optional)
end = 56 # int | End time of window of fetch logs, unix epoch in seconds (default: current utc timestamp) (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        api_response = api_instance.get_group_activity(group_namespace, group_name, start=start, end=end, page=page, per_page=per_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->get_group_activity: %s\n" % e)
```

- Basic Authentication (BasicAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | namespace group is in (an organization name or user's username)
group_name = 'group_name_example' # str | name/uri of group that is url-encoded
start = 56 # int | Start time of window of fetch logs, unix epoch in seconds (default: seven days ago) (optional)
end = 56 # int | End time of window of fetch logs, unix epoch in seconds (default: current utc timestamp) (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        api_response = api_instance.get_group_activity(group_namespace, group_name, start=start, end=end, page=page, per_page=per_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->get_group_activity: %s\n" % e)
```

### Parameters

| Name                | Type    | Description                                                                              | Notes      |
| ------------------- | ------- | ---------------------------------------------------------------------------------------- | ---------- |
| **group_namespace** | **str** | namespace group is in (an organization name or user&#39;s username)                      |
| **group_name**      | **str** | name/uri of group that is url-encoded                                                    |
| **start**           | **int** | Start time of window of fetch logs, unix epoch in seconds (default: seven days ago)      | [optional] |
| **end**             | **int** | End time of window of fetch logs, unix epoch in seconds (default: current utc timestamp) | [optional] |
| **page**            | **int** | pagination offset                                                                        | [optional] |
| **per_page**        | **int** | pagination limit                                                                         | [optional] |

### Return type

[**GroupActivityResponse**](GroupActivityResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description                                                                   | Response headers |
| ----------- | ----------------------------------------------------------------------------- | ---------------- |
| **200**     | Activity logs of group and all its content along with the pagination metadata | -                |
| **502**     | Bad Gateway                                                                   | -                |
| **0**       | error response                                                                | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_group_content_activity**

> GroupContentActivityResponse get_group_content_activity(group_namespace, group_name, page=page, per_page=per_page)

Retrieves combined activity logs for all assets contained in a group.

### Example

- Api Key Authentication (ApiKeyAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        api_response = api_instance.get_group_content_activity(group_namespace, group_name, page=page, per_page=per_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->get_group_content_activity: %s\n" % e)
```

- Basic Authentication (BasicAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        api_response = api_instance.get_group_content_activity(group_namespace, group_name, page=page, per_page=per_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->get_group_content_activity: %s\n" % e)
```

### Parameters

| Name                | Type    | Description                        | Notes      |
| ------------------- | ------- | ---------------------------------- | ---------- |
| **group_namespace** | **str** | The namespace of the group         |
| **group_name**      | **str** | The unique name or id of the group |
| **page**            | **int** | pagination offset                  | [optional] |
| **per_page**        | **int** | pagination limit                   | [optional] |

### Return type

[**GroupContentActivityResponse**](GroupContentActivityResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description                                                        | Response headers |
| ----------- | ------------------------------------------------------------------ | ---------------- |
| **200**     | Activity logs of group contents along with the pagination metadata | -                |
| **502**     | Bad Gateway                                                        | -                |
| **0**       | error response                                                     | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_group_metadata**

> Metadata get_group_metadata(group_namespace, group_name, metadata_retrieval=metadata_retrieval)

get metadata on a group using the requested config

### Example

- Api Key Authentication (ApiKeyAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
metadata_retrieval = tiledb.cloud._common.api_v2.GroupMetadataRetrievalRequest() # GroupMetadataRetrievalRequest |  (optional)

    try:
        api_response = api_instance.get_group_metadata(group_namespace, group_name, metadata_retrieval=metadata_retrieval)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->get_group_metadata: %s\n" % e)
```

- Basic Authentication (BasicAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
metadata_retrieval = tiledb.cloud._common.api_v2.GroupMetadataRetrievalRequest() # GroupMetadataRetrievalRequest |  (optional)

    try:
        api_response = api_instance.get_group_metadata(group_namespace, group_name, metadata_retrieval=metadata_retrieval)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->get_group_metadata: %s\n" % e)
```

### Parameters

| Name                   | Type                                                                  | Description                        | Notes      |
| ---------------------- | --------------------------------------------------------------------- | ---------------------------------- | ---------- |
| **group_namespace**    | **str**                                                               | The namespace of the group         |
| **group_name**         | **str**                                                               | The unique name or id of the group |
| **metadata_retrieval** | [**GroupMetadataRetrievalRequest**](GroupMetadataRetrievalRequest.md) |                                    | [optional] |

### Return type

[**Metadata**](Metadata.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description                   | Response headers |
| ----------- | ----------------------------- | ---------------- |
| **200**     | retrieve metadata for a group | -                |
| **502**     | Bad Gateway                   | -                |
| **0**       | error response                | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **groups_group_namespace_group_name_options**

> groups_group_namespace_group_name_options(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name)

can be used to check if the resource exists

### Example

- Api Key Authentication (ApiKeyAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)

    try:
        api_instance.groups_group_namespace_group_name_options(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name)
    except ApiException as e:
        print("Exception when calling GroupsApi->groups_group_namespace_group_name_options: %s\n" % e)
```

- Basic Authentication (BasicAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)

    try:
        api_instance.groups_group_namespace_group_name_options(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name)
    except ApiException as e:
        print("Exception when calling GroupsApi->groups_group_namespace_group_name_options: %s\n" % e)
```

### Parameters

| Name                                       | Type    | Description                                                | Notes      |
| ------------------------------------------ | ------- | ---------------------------------------------------------- | ---------- |
| **group_namespace**                        | **str** | The namespace of the group                                 |
| **group_name**                             | **str** | The unique name or id of the group                         |
| **x_tiledb_cloud_access_credentials_name** | **str** | Optional registered access credentials to use for creation | [optional] |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description                 | Response headers |
| ----------- | --------------------------- | ---------------- |
| **204**     | the resource exists         | -                |
| **404**     | the resource does not exist | -                |
| **502**     | Bad Gateway                 | -                |
| **0**       | error response              | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **register_group**

> register_group(group_namespace, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, group_registration=group_registration)

Registers an already existing group

### Example

- Api Key Authentication (ApiKeyAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)
group_registration = tiledb.cloud._common.api_v2.GroupRegistrationRequest() # GroupRegistrationRequest |  (optional)

    try:
        api_instance.register_group(group_namespace, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, group_registration=group_registration)
    except ApiException as e:
        print("Exception when calling GroupsApi->register_group: %s\n" % e)
```

- Basic Authentication (BasicAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)
group_registration = tiledb.cloud._common.api_v2.GroupRegistrationRequest() # GroupRegistrationRequest |  (optional)

    try:
        api_instance.register_group(group_namespace, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, group_registration=group_registration)
    except ApiException as e:
        print("Exception when calling GroupsApi->register_group: %s\n" % e)
```

### Parameters

| Name                                       | Type                                                        | Description                                                | Notes      |
| ------------------------------------------ | ----------------------------------------------------------- | ---------------------------------------------------------- | ---------- |
| **group_namespace**                        | **str**                                                     | The namespace of the group                                 |
| **x_tiledb_cloud_access_credentials_name** | **str**                                                     | Optional registered access credentials to use for creation | [optional] |
| **group_registration**                     | [**GroupRegistrationRequest**](GroupRegistrationRequest.md) |                                                            | [optional] |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description                | Response headers |
| ----------- | -------------------------- | ---------------- |
| **201**     | group created successfully | -                |
| **502**     | Bad Gateway                | -                |
| **0**       | error response             | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_group**

> GroupContentsRetrievalResponse retrieve_group(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, group_retrieval=group_retrieval)

Retrieves the contents of a group

### Example

- Api Key Authentication (ApiKeyAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)
group_retrieval = tiledb.cloud._common.api_v2.GroupContentsRetrievalRequest() # GroupContentsRetrievalRequest |  (optional)

    try:
        api_response = api_instance.retrieve_group(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, group_retrieval=group_retrieval)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->retrieve_group: %s\n" % e)
```

- Basic Authentication (BasicAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)
group_retrieval = tiledb.cloud._common.api_v2.GroupContentsRetrievalRequest() # GroupContentsRetrievalRequest |  (optional)

    try:
        api_response = api_instance.retrieve_group(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, group_retrieval=group_retrieval)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->retrieve_group: %s\n" % e)
```

### Parameters

| Name                                       | Type                                                                  | Description                                                | Notes      |
| ------------------------------------------ | --------------------------------------------------------------------- | ---------------------------------------------------------- | ---------- |
| **group_namespace**                        | **str**                                                               | The namespace of the group                                 |
| **group_name**                             | **str**                                                               | The unique name or id of the group                         |
| **x_tiledb_cloud_access_credentials_name** | **str**                                                               | Optional registered access credentials to use for creation | [optional] |
| **group_retrieval**                        | [**GroupContentsRetrievalRequest**](GroupContentsRetrievalRequest.md) |                                                            | [optional] |

### Return type

[**GroupContentsRetrievalResponse**](GroupContentsRetrievalResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description                | Response headers |
| ----------- | -------------------------- | ---------------- |
| **200**     | group created successfully | -                |
| **502**     | Bad Gateway                | -                |
| **0**       | error response             | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_group_contents**

> update_group_contents(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, group_update_contents=group_update_contents)

Change the contents of the group

### Example

- Api Key Authentication (ApiKeyAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)
group_update_contents = tiledb.cloud._common.api_v2.GroupContentsChangesRequest() # GroupContentsChangesRequest |  (optional)

    try:
        api_instance.update_group_contents(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, group_update_contents=group_update_contents)
    except ApiException as e:
        print("Exception when calling GroupsApi->update_group_contents: %s\n" % e)
```

- Basic Authentication (BasicAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
x_tiledb_cloud_access_credentials_name = 'x_tiledb_cloud_access_credentials_name_example' # str | Optional registered access credentials to use for creation (optional)
group_update_contents = tiledb.cloud._common.api_v2.GroupContentsChangesRequest() # GroupContentsChangesRequest |  (optional)

    try:
        api_instance.update_group_contents(group_namespace, group_name, x_tiledb_cloud_access_credentials_name=x_tiledb_cloud_access_credentials_name, group_update_contents=group_update_contents)
    except ApiException as e:
        print("Exception when calling GroupsApi->update_group_contents: %s\n" % e)
```

### Parameters

| Name                                       | Type                                                              | Description                                                | Notes      |
| ------------------------------------------ | ----------------------------------------------------------------- | ---------------------------------------------------------- | ---------- |
| **group_namespace**                        | **str**                                                           | The namespace of the group                                 |
| **group_name**                             | **str**                                                           | The unique name or id of the group                         |
| **x_tiledb_cloud_access_credentials_name** | **str**                                                           | Optional registered access credentials to use for creation | [optional] |
| **group_update_contents**                  | [**GroupContentsChangesRequest**](GroupContentsChangesRequest.md) |                                                            | [optional] |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description                     | Response headers |
| ----------- | ------------------------------- | ---------------- |
| **204**     | attributes changed successfully | -                |
| **502**     | Bad Gateway                     | -                |
| **0**       | error response                  | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_group_metadata**

> update_group_metadata(group_namespace, group_name, metadata_updating=metadata_updating)

update metadata on a group

### Example

- Api Key Authentication (ApiKeyAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
metadata_updating = tiledb.cloud._common.api_v2.GroupMetadataUpdateRequest() # GroupMetadataUpdateRequest |  (optional)

    try:
        api_instance.update_group_metadata(group_namespace, group_name, metadata_updating=metadata_updating)
    except ApiException as e:
        print("Exception when calling GroupsApi->update_group_metadata: %s\n" % e)
```

- Basic Authentication (BasicAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    host = "http://localhost",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v2.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v2.GroupsApi(api_client)
    group_namespace = 'group_namespace_example' # str | The namespace of the group
group_name = 'group_name_example' # str | The unique name or id of the group
metadata_updating = tiledb.cloud._common.api_v2.GroupMetadataUpdateRequest() # GroupMetadataUpdateRequest |  (optional)

    try:
        api_instance.update_group_metadata(group_namespace, group_name, metadata_updating=metadata_updating)
    except ApiException as e:
        print("Exception when calling GroupsApi->update_group_metadata: %s\n" % e)
```

### Parameters

| Name                  | Type                                                            | Description                        | Notes      |
| --------------------- | --------------------------------------------------------------- | ---------------------------------- | ---------- |
| **group_namespace**   | **str**                                                         | The namespace of the group         |
| **group_name**        | **str**                                                         | The unique name or id of the group |
| **metadata_updating** | [**GroupMetadataUpdateRequest**](GroupMetadataUpdateRequest.md) |                                    | [optional] |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description                         | Response headers |
| ----------- | ----------------------------------- | ---------------- |
| **200**     | group metadata updated successfully | -                |
| **502**     | Bad Gateway                         | -                |
| **0**       | error response                      | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
