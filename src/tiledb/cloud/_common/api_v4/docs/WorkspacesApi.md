# tiledb.cloud.\_common.api_v4.WorkspacesApi

All URIs are relative to *https://api.tiledb.com/v4*

| Method                                                                | HTTP request                                   | Description                                     |
| --------------------------------------------------------------------- | ---------------------------------------------- | ----------------------------------------------- |
| [**create_workspace**](WorkspacesApi.md#create_workspace)             | **POST** /workspaces                           | Create a workspace                              |
| [**create_workspace_users**](WorkspacesApi.md#create_workspace_users) | **POST** /workspaceusers                       | Create one or more workspace users              |
| [**delete_workspace**](WorkspacesApi.md#delete_workspace)             | **DELETE** /workspaces/{workspace_id}          | Delete a workspace                              |
| [**delete_workspace_user**](WorkspacesApi.md#delete_workspace_user)   | **DELETE** /workspaceusers/{user_id}           | Delete a workspace user                         |
| [**delete_workspace_users**](WorkspacesApi.md#delete_workspace_users) | **POST** /actions/workspaces/users/bulk_delete | Delete the given workspace users in a workspace |
| [**get_workspace**](WorkspacesApi.md#get_workspace)                   | **GET** /workspaces/{workspace_id}             | Retrieves metadata for the given workspace      |
| [**get_workspace_user**](WorkspacesApi.md#get_workspace_user)         | **GET** /workspaceusers/{user_id}              | Retrieve a workspace user                       |
| [**list_workspace_users**](WorkspacesApi.md#list_workspace_users)     | **GET** /workspaceusers                        | Retrieve multiple workspace users               |
| [**update_workspace**](WorkspacesApi.md#update_workspace)             | **PATCH** /workspaces/{workspace_id}           | Update a workspace                              |
| [**update_workspace_user**](WorkspacesApi.md#update_workspace_user)   | **PATCH** /workspaceusers/{user_id}            | Update a workspace user                         |
| [**update_workspace_users**](WorkspacesApi.md#update_workspace_users) | **POST** /actions/workspaces/users/bulk_update | Update multiple workspace users in a workspace  |

# **create_workspace**

> WorkspaceCreateResponse create_workspace(workspace_create_request)

Create a workspace

create a workspace, the user creating will be listed as owner

### Example

- Api Key Authentication (ApiKeyAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    workspace_create_request = tiledb.cloud._common.api_v4.WorkspaceCreateRequest() # WorkspaceCreateRequest | workspace to create

    try:
        # Create a workspace
        api_response = api_instance.create_workspace(workspace_create_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->create_workspace: %s\n" % e)
```

- Basic Authentication (BasicAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    workspace_create_request = tiledb.cloud._common.api_v4.WorkspaceCreateRequest() # WorkspaceCreateRequest | workspace to create

    try:
        # Create a workspace
        api_response = api_instance.create_workspace(workspace_create_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->create_workspace: %s\n" % e)
```

- OAuth Authentication (OAuth2):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    workspace_create_request = tiledb.cloud._common.api_v4.WorkspaceCreateRequest() # WorkspaceCreateRequest | workspace to create

    try:
        # Create a workspace
        api_response = api_instance.create_workspace(workspace_create_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->create_workspace: %s\n" % e)
```

### Parameters

| Name                         | Type                                                    | Description         | Notes |
| ---------------------------- | ------------------------------------------------------- | ------------------- | ----- |
| **workspace_create_request** | [**WorkspaceCreateRequest**](WorkspaceCreateRequest.md) | workspace to create |

### Return type

[**WorkspaceCreateResponse**](WorkspaceCreateResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description                   | Response headers |
| ----------- | ----------------------------- | ---------------- |
| **201**     | Successful workspace response | -                |
| **0**       | error response                | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_workspace_users**

> WorkspaceUsersCreateResponse create_workspace_users(request_body)

Create one or more workspace users

Create one or more workspace users

### Example

- Api Key Authentication (ApiKeyAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    request_body = None # list[object] | The request body containing the workspace users to create

    try:
        # Create one or more workspace users
        api_response = api_instance.create_workspace_users(request_body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->create_workspace_users: %s\n" % e)
```

- Basic Authentication (BasicAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    request_body = None # list[object] | The request body containing the workspace users to create

    try:
        # Create one or more workspace users
        api_response = api_instance.create_workspace_users(request_body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->create_workspace_users: %s\n" % e)
```

- OAuth Authentication (OAuth2):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    request_body = None # list[object] | The request body containing the workspace users to create

    try:
        # Create one or more workspace users
        api_response = api_instance.create_workspace_users(request_body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->create_workspace_users: %s\n" % e)
```

### Parameters

| Name             | Type                          | Description                                               | Notes |
| ---------------- | ----------------------------- | --------------------------------------------------------- | ----- |
| **request_body** | [**list[object]**](object.md) | The request body containing the workspace users to create |

### Return type

[**WorkspaceUsersCreateResponse**](WorkspaceUsersCreateResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description               | Response headers |
| ----------- | ------------------------- | ---------------- |
| **201**     | Workspace user(s) created | -                |
| **0**       | An error occurred         | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_workspace**

> delete_workspace(workspace_id)

Delete a workspace

delete a workspace

### Example

- Api Key Authentication (ApiKeyAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    workspace_id = 'workspace_id_example' # str | The workspace id in the form ws_9m4e2mr0ui3e8a215n4g

    try:
        # Delete a workspace
        api_instance.delete_workspace(workspace_id)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->delete_workspace: %s\n" % e)
```

- Basic Authentication (BasicAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    workspace_id = 'workspace_id_example' # str | The workspace id in the form ws_9m4e2mr0ui3e8a215n4g

    try:
        # Delete a workspace
        api_instance.delete_workspace(workspace_id)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->delete_workspace: %s\n" % e)
```

- OAuth Authentication (OAuth2):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    workspace_id = 'workspace_id_example' # str | The workspace id in the form ws_9m4e2mr0ui3e8a215n4g

    try:
        # Delete a workspace
        api_instance.delete_workspace(workspace_id)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->delete_workspace: %s\n" % e)
```

### Parameters

| Name             | Type    | Description                                          | Notes |
| ---------------- | ------- | ---------------------------------------------------- | ----- |
| **workspace_id** | **str** | The workspace id in the form ws_9m4e2mr0ui3e8a215n4g |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description       | Response headers |
| ----------- | ----------------- | ---------------- |
| **204**     | workspace deleted | -                |
| **0**       | error response    | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_workspace_user**

> delete_workspace_user(user_id)

Delete a workspace user

Delete the given workspace user

### Example

- Api Key Authentication (ApiKeyAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    user_id = 'user_id_example' # str | The user id in the form usr_9m4e2mr0ui3e8a215n4g

    try:
        # Delete a workspace user
        api_instance.delete_workspace_user(user_id)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->delete_workspace_user: %s\n" % e)
```

- Basic Authentication (BasicAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    user_id = 'user_id_example' # str | The user id in the form usr_9m4e2mr0ui3e8a215n4g

    try:
        # Delete a workspace user
        api_instance.delete_workspace_user(user_id)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->delete_workspace_user: %s\n" % e)
```

- OAuth Authentication (OAuth2):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    user_id = 'user_id_example' # str | The user id in the form usr_9m4e2mr0ui3e8a215n4g

    try:
        # Delete a workspace user
        api_instance.delete_workspace_user(user_id)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->delete_workspace_user: %s\n" % e)
```

### Parameters

| Name        | Type    | Description                                      | Notes |
| ----------- | ------- | ------------------------------------------------ | ----- |
| **user_id** | **str** | The user id in the form usr_9m4e2mr0ui3e8a215n4g |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description                      | Response headers |
| ----------- | -------------------------------- | ---------------- |
| **204**     | Workspace user deleted           | -                |
| **404**     | Workspace user ID does not exist | -                |
| **0**       | An error occurred                | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_workspace_users**

> delete_workspace_users(request_body)

Delete the given workspace users in a workspace

Delete the given workspace users in a workspace

### Example

- Api Key Authentication (ApiKeyAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    request_body = ['request_body_example'] # list[str] | The request body containing the workspace users to delete

    try:
        # Delete the given workspace users in a workspace
        api_instance.delete_workspace_users(request_body)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->delete_workspace_users: %s\n" % e)
```

- Basic Authentication (BasicAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    request_body = ['request_body_example'] # list[str] | The request body containing the workspace users to delete

    try:
        # Delete the given workspace users in a workspace
        api_instance.delete_workspace_users(request_body)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->delete_workspace_users: %s\n" % e)
```

- OAuth Authentication (OAuth2):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    request_body = ['request_body_example'] # list[str] | The request body containing the workspace users to delete

    try:
        # Delete the given workspace users in a workspace
        api_instance.delete_workspace_users(request_body)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->delete_workspace_users: %s\n" % e)
```

### Parameters

| Name             | Type                    | Description                                               | Notes |
| ---------------- | ----------------------- | --------------------------------------------------------- | ----- |
| **request_body** | [**list[str]**](str.md) | The request body containing the workspace users to delete |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description                                           | Response headers |
| ----------- | ----------------------------------------------------- | ---------------- |
| **204**     | Workspace users deleted                               | -                |
| **404**     | One or more of the given workspace users do not exist | -                |
| **0**       | An error occurred                                     | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workspace**

> WorkspaceGetResponse get_workspace(workspace_id)

Retrieves metadata for the given workspace

End point to retrieve metadata for the passed workspace

### Example

- Api Key Authentication (ApiKeyAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    workspace_id = 'workspace_id_example' # str | The workspace id in the form ws_9m4e2mr0ui3e8a215n4g

    try:
        # Retrieves metadata for the given workspace
        api_response = api_instance.get_workspace(workspace_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->get_workspace: %s\n" % e)
```

- Basic Authentication (BasicAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    workspace_id = 'workspace_id_example' # str | The workspace id in the form ws_9m4e2mr0ui3e8a215n4g

    try:
        # Retrieves metadata for the given workspace
        api_response = api_instance.get_workspace(workspace_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->get_workspace: %s\n" % e)
```

- OAuth Authentication (OAuth2):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    workspace_id = 'workspace_id_example' # str | The workspace id in the form ws_9m4e2mr0ui3e8a215n4g

    try:
        # Retrieves metadata for the given workspace
        api_response = api_instance.get_workspace(workspace_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->get_workspace: %s\n" % e)
```

### Parameters

| Name             | Type    | Description                                          | Notes |
| ---------------- | ------- | ---------------------------------------------------- | ----- |
| **workspace_id** | **str** | The workspace id in the form ws_9m4e2mr0ui3e8a215n4g |

### Return type

[**WorkspaceGetResponse**](WorkspaceGetResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description                   | Response headers |
| ----------- | ----------------------------- | ---------------- |
| **200**     | Successful workspace response | -                |
| **404**     | Workspace does not exist      | -                |
| **0**       | error response                | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workspace_user**

> WorkspaceUserGetResponse get_workspace_user(user_id)

Retrieve a workspace user

Retrieve the given workspace user

### Example

- Api Key Authentication (ApiKeyAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    user_id = 'user_id_example' # str | The user id in the form usr_9m4e2mr0ui3e8a215n4g

    try:
        # Retrieve a workspace user
        api_response = api_instance.get_workspace_user(user_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->get_workspace_user: %s\n" % e)
```

- Basic Authentication (BasicAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    user_id = 'user_id_example' # str | The user id in the form usr_9m4e2mr0ui3e8a215n4g

    try:
        # Retrieve a workspace user
        api_response = api_instance.get_workspace_user(user_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->get_workspace_user: %s\n" % e)
```

- OAuth Authentication (OAuth2):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    user_id = 'user_id_example' # str | The user id in the form usr_9m4e2mr0ui3e8a215n4g

    try:
        # Retrieve a workspace user
        api_response = api_instance.get_workspace_user(user_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->get_workspace_user: %s\n" % e)
```

### Parameters

| Name        | Type    | Description                                      | Notes |
| ----------- | ------- | ------------------------------------------------ | ----- |
| **user_id** | **str** | The user id in the form usr_9m4e2mr0ui3e8a215n4g |

### Return type

[**WorkspaceUserGetResponse**](WorkspaceUserGetResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description                      | Response headers |
| ----------- | -------------------------------- | ---------------- |
| **200**     | Workspace user retrieved         | -                |
| **404**     | Workspace user ID does not exist | -                |
| **0**       | An error occurred                | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_workspace_users**

> WorkspaceUsersListResponse list_workspace_users(page=page, per_page=per_page)

Retrieve multiple workspace users

Retrieve a list of workspace users

### Example

- Api Key Authentication (ApiKeyAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        # Retrieve multiple workspace users
        api_response = api_instance.list_workspace_users(page=page, per_page=per_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->list_workspace_users: %s\n" % e)
```

- Basic Authentication (BasicAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        # Retrieve multiple workspace users
        api_response = api_instance.list_workspace_users(page=page, per_page=per_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->list_workspace_users: %s\n" % e)
```

- OAuth Authentication (OAuth2):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        # Retrieve multiple workspace users
        api_response = api_instance.list_workspace_users(page=page, per_page=per_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->list_workspace_users: %s\n" % e)
```

### Parameters

| Name         | Type    | Description       | Notes      |
| ------------ | ------- | ----------------- | ---------- |
| **page**     | **int** | pagination offset | [optional] |
| **per_page** | **int** | pagination limit  | [optional] |

### Return type

[**WorkspaceUsersListResponse**](WorkspaceUsersListResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description                      | Response headers |
| ----------- | -------------------------------- | ---------------- |
| **200**     | Workspace user(s) list retrieved | -                |
| **404**     | Workspace ID does not exist      | -                |
| **0**       | An error occurred                | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_workspace**

> update_workspace(workspace_id, workspace_update_request)

Update a workspace

update a workspace

### Example

- Api Key Authentication (ApiKeyAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    workspace_id = 'workspace_id_example' # str | The workspace id in the form ws_9m4e2mr0ui3e8a215n4g
workspace_update_request = tiledb.cloud._common.api_v4.WorkspaceUpdateRequest() # WorkspaceUpdateRequest | workspaceUpdateDetails

    try:
        # Update a workspace
        api_instance.update_workspace(workspace_id, workspace_update_request)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->update_workspace: %s\n" % e)
```

- Basic Authentication (BasicAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    workspace_id = 'workspace_id_example' # str | The workspace id in the form ws_9m4e2mr0ui3e8a215n4g
workspace_update_request = tiledb.cloud._common.api_v4.WorkspaceUpdateRequest() # WorkspaceUpdateRequest | workspaceUpdateDetails

    try:
        # Update a workspace
        api_instance.update_workspace(workspace_id, workspace_update_request)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->update_workspace: %s\n" % e)
```

- OAuth Authentication (OAuth2):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    workspace_id = 'workspace_id_example' # str | The workspace id in the form ws_9m4e2mr0ui3e8a215n4g
workspace_update_request = tiledb.cloud._common.api_v4.WorkspaceUpdateRequest() # WorkspaceUpdateRequest | workspaceUpdateDetails

    try:
        # Update a workspace
        api_instance.update_workspace(workspace_id, workspace_update_request)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->update_workspace: %s\n" % e)
```

### Parameters

| Name                         | Type                                                    | Description                                          | Notes |
| ---------------------------- | ------------------------------------------------------- | ---------------------------------------------------- | ----- |
| **workspace_id**             | **str**                                                 | The workspace id in the form ws_9m4e2mr0ui3e8a215n4g |
| **workspace_update_request** | [**WorkspaceUpdateRequest**](WorkspaceUpdateRequest.md) | workspaceUpdateDetails                               |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description       | Response headers |
| ----------- | ----------------- | ---------------- |
| **204**     | workspace updated | -                |
| **0**       | error response    | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_workspace_user**

> update_workspace_user(user_id, workspace_user_update_request)

Update a workspace user

Update the given workspace user

### Example

- Api Key Authentication (ApiKeyAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    user_id = 'user_id_example' # str | The user id in the form usr_9m4e2mr0ui3e8a215n4g
workspace_user_update_request = tiledb.cloud._common.api_v4.WorkspaceUserUpdateRequest() # WorkspaceUserUpdateRequest | The request body containing the workspace user to update

    try:
        # Update a workspace user
        api_instance.update_workspace_user(user_id, workspace_user_update_request)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->update_workspace_user: %s\n" % e)
```

- Basic Authentication (BasicAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    user_id = 'user_id_example' # str | The user id in the form usr_9m4e2mr0ui3e8a215n4g
workspace_user_update_request = tiledb.cloud._common.api_v4.WorkspaceUserUpdateRequest() # WorkspaceUserUpdateRequest | The request body containing the workspace user to update

    try:
        # Update a workspace user
        api_instance.update_workspace_user(user_id, workspace_user_update_request)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->update_workspace_user: %s\n" % e)
```

- OAuth Authentication (OAuth2):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    user_id = 'user_id_example' # str | The user id in the form usr_9m4e2mr0ui3e8a215n4g
workspace_user_update_request = tiledb.cloud._common.api_v4.WorkspaceUserUpdateRequest() # WorkspaceUserUpdateRequest | The request body containing the workspace user to update

    try:
        # Update a workspace user
        api_instance.update_workspace_user(user_id, workspace_user_update_request)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->update_workspace_user: %s\n" % e)
```

### Parameters

| Name                              | Type                                                            | Description                                              | Notes |
| --------------------------------- | --------------------------------------------------------------- | -------------------------------------------------------- | ----- |
| **user_id**                       | **str**                                                         | The user id in the form usr_9m4e2mr0ui3e8a215n4g         |
| **workspace_user_update_request** | [**WorkspaceUserUpdateRequest**](WorkspaceUserUpdateRequest.md) | The request body containing the workspace user to update |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description                      | Response headers |
| ----------- | -------------------------------- | ---------------- |
| **204**     | Workspace user updated           | -                |
| **404**     | Workspace user ID does not exist | -                |
| **0**       | An error occurred                | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_workspace_users**

> update_workspace_users(request_body)

Update multiple workspace users in a workspace

Update multiple workspace users in a workspace

### Example

- Api Key Authentication (ApiKeyAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    request_body = None # list[object] | The request body containing the workspace users to update

    try:
        # Update multiple workspace users in a workspace
        api_instance.update_workspace_users(request_body)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->update_workspace_users: %s\n" % e)
```

- Basic Authentication (BasicAuth):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    request_body = None # list[object] | The request body containing the workspace users to update

    try:
        # Update multiple workspace users in a workspace
        api_instance.update_workspace_users(request_body)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->update_workspace_users: %s\n" % e)
```

- OAuth Authentication (OAuth2):

```python
from __future__ import print_function
import time
import tiledb.cloud._common.api_v4
from tiledb.cloud._common.api_v4.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.tiledb.com/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud._common.api_v4.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Configure OAuth2 access token for authorization: OAuth2
configuration = tiledb.cloud._common.api_v4.Configuration(
    host = "https://api.tiledb.com/v4"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tiledb.cloud._common.api_v4.WorkspacesApi(api_client)
    request_body = None # list[object] | The request body containing the workspace users to update

    try:
        # Update multiple workspace users in a workspace
        api_instance.update_workspace_users(request_body)
    except ApiException as e:
        print("Exception when calling WorkspacesApi->update_workspace_users: %s\n" % e)
```

### Parameters

| Name             | Type                          | Description                                               | Notes |
| ---------------- | ----------------------------- | --------------------------------------------------------- | ----- |
| **request_body** | [**list[object]**](object.md) | The request body containing the workspace users to update |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description                          | Response headers |
| ----------- | ------------------------------------ | ---------------- |
| **204**     | Workspace users updated successfully | -                |
| **0**       | An error occurred                    | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
