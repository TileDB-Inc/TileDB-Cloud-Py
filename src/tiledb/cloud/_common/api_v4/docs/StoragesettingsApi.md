# tiledb.cloud.\_common.api_v4.StoragesettingsApi

All URIs are relative to *https://api.tiledb.com/v4*

| Method                                                                                 | HTTP request                           | Description                  |
| -------------------------------------------------------------------------------------- | -------------------------------------- | ---------------------------- |
| [**create_storage_setting**](StoragesettingsApi.md#create_storage_setting)             | **POST** /storagesettings              | Create a new storage setting |
| [**delete_storage_setting_by_id**](StoragesettingsApi.md#delete_storage_setting_by_id) | **DELETE** /storagesettings/{stset_id} | Delete storage setting       |
| [**get_storage_setting_by_id**](StoragesettingsApi.md#get_storage_setting_by_id)       | **GET** /storagesettings/{stset_id}    | Get storage setting          |
| [**list_storage_settings**](StoragesettingsApi.md#list_storage_settings)               | **GET** /storagesettings               | Get storage settings         |
| [**patch_storage_setting_by_id**](StoragesettingsApi.md#patch_storage_setting_by_id)   | **PATCH** /storagesettings/{stset_id}  | Update storage setting       |

# **create_storage_setting**

> StorageSettingsCreateResponse create_storage_setting(storage_settings_create_request, teamspace_id=teamspace_id)

Create a new storage setting

create a storage setting

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
    api_instance = tiledb.cloud._common.api_v4.StoragesettingsApi(api_client)
    storage_settings_create_request = tiledb.cloud._common.api_v4.StorageSettingsCreateRequest() # StorageSettingsCreateRequest | The request body containing the storage setting to create
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Create a new storage setting
        api_response = api_instance.create_storage_setting(storage_settings_create_request, teamspace_id=teamspace_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StoragesettingsApi->create_storage_setting: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.StoragesettingsApi(api_client)
    storage_settings_create_request = tiledb.cloud._common.api_v4.StorageSettingsCreateRequest() # StorageSettingsCreateRequest | The request body containing the storage setting to create
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Create a new storage setting
        api_response = api_instance.create_storage_setting(storage_settings_create_request, teamspace_id=teamspace_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StoragesettingsApi->create_storage_setting: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.StoragesettingsApi(api_client)
    storage_settings_create_request = tiledb.cloud._common.api_v4.StorageSettingsCreateRequest() # StorageSettingsCreateRequest | The request body containing the storage setting to create
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Create a new storage setting
        api_response = api_instance.create_storage_setting(storage_settings_create_request, teamspace_id=teamspace_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StoragesettingsApi->create_storage_setting: %s\n" % e)
```

### Parameters

| Name                                | Type                                                                | Description                                                                        | Notes      |
| ----------------------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ---------- |
| **storage_settings_create_request** | [**StorageSettingsCreateRequest**](StorageSettingsCreateRequest.md) | The request body containing the storage setting to create                          |
| **teamspace_id**                    | **str**                                                             | Teamspace id should be empty, if the request is about an action on workspace level | [optional] |

### Return type

[**StorageSettingsCreateResponse**](StorageSettingsCreateResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description              | Response headers |
| ----------- | ------------------------ | ---------------- |
| **201**     | Storage settings created | -                |
| **0**       | error response           | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_storage_setting_by_id**

> delete_storage_setting_by_id(stset_id, teamspace_id=teamspace_id)

Delete storage setting

Delete the storage setting.

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
    api_instance = tiledb.cloud._common.api_v4.StoragesettingsApi(api_client)
    stset_id = 'stset_id_example' # str | The storage setting id in the form stset_9m4e2mr0ui3e8a215n4g
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Delete storage setting
        api_instance.delete_storage_setting_by_id(stset_id, teamspace_id=teamspace_id)
    except ApiException as e:
        print("Exception when calling StoragesettingsApi->delete_storage_setting_by_id: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.StoragesettingsApi(api_client)
    stset_id = 'stset_id_example' # str | The storage setting id in the form stset_9m4e2mr0ui3e8a215n4g
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Delete storage setting
        api_instance.delete_storage_setting_by_id(stset_id, teamspace_id=teamspace_id)
    except ApiException as e:
        print("Exception when calling StoragesettingsApi->delete_storage_setting_by_id: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.StoragesettingsApi(api_client)
    stset_id = 'stset_id_example' # str | The storage setting id in the form stset_9m4e2mr0ui3e8a215n4g
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Delete storage setting
        api_instance.delete_storage_setting_by_id(stset_id, teamspace_id=teamspace_id)
    except ApiException as e:
        print("Exception when calling StoragesettingsApi->delete_storage_setting_by_id: %s\n" % e)
```

### Parameters

| Name             | Type    | Description                                                                        | Notes      |
| ---------------- | ------- | ---------------------------------------------------------------------------------- | ---------- |
| **stset_id**     | **str** | The storage setting id in the form stset_9m4e2mr0ui3e8a215n4g                      |
| **teamspace_id** | **str** | Teamspace id should be empty, if the request is about an action on workspace level | [optional] |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description             | Response headers |
| ----------- | ----------------------- | ---------------- |
| **204**     | storage setting deleted | -                |
| **0**       | error response          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_storage_setting_by_id**

> StorageSettingGetResponse get_storage_setting_by_id(stset_id, teamspace_id=teamspace_id)

Get storage setting

get information about storage setting by ID

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
    api_instance = tiledb.cloud._common.api_v4.StoragesettingsApi(api_client)
    stset_id = 'stset_id_example' # str | The storage setting id in the form stset_9m4e2mr0ui3e8a215n4g
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Get storage setting
        api_response = api_instance.get_storage_setting_by_id(stset_id, teamspace_id=teamspace_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StoragesettingsApi->get_storage_setting_by_id: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.StoragesettingsApi(api_client)
    stset_id = 'stset_id_example' # str | The storage setting id in the form stset_9m4e2mr0ui3e8a215n4g
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Get storage setting
        api_response = api_instance.get_storage_setting_by_id(stset_id, teamspace_id=teamspace_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StoragesettingsApi->get_storage_setting_by_id: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.StoragesettingsApi(api_client)
    stset_id = 'stset_id_example' # str | The storage setting id in the form stset_9m4e2mr0ui3e8a215n4g
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Get storage setting
        api_response = api_instance.get_storage_setting_by_id(stset_id, teamspace_id=teamspace_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StoragesettingsApi->get_storage_setting_by_id: %s\n" % e)
```

### Parameters

| Name             | Type    | Description                                                                        | Notes      |
| ---------------- | ------- | ---------------------------------------------------------------------------------- | ---------- |
| **stset_id**     | **str** | The storage setting id in the form stset_9m4e2mr0ui3e8a215n4g                      |
| **teamspace_id** | **str** | Teamspace id should be empty, if the request is about an action on workspace level | [optional] |

### Return type

[**StorageSettingGetResponse**](StorageSettingGetResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description                         | Response headers |
| ----------- | ----------------------------------- | ---------------- |
| **200**     | Successful storage setting response | -                |
| **404**     | Storage setting does not exist      | -                |
| **0**       | error response                      | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_storage_settings**

> StorageSettingsListResponse list_storage_settings(teamspace_id=teamspace_id, page=page, per_page=per_page)

Get storage settings

list the storage settings available for the user

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
    api_instance = tiledb.cloud._common.api_v4.StoragesettingsApi(api_client)
    teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        # Get storage settings
        api_response = api_instance.list_storage_settings(teamspace_id=teamspace_id, page=page, per_page=per_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StoragesettingsApi->list_storage_settings: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.StoragesettingsApi(api_client)
    teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        # Get storage settings
        api_response = api_instance.list_storage_settings(teamspace_id=teamspace_id, page=page, per_page=per_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StoragesettingsApi->list_storage_settings: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.StoragesettingsApi(api_client)
    teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        # Get storage settings
        api_response = api_instance.list_storage_settings(teamspace_id=teamspace_id, page=page, per_page=per_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StoragesettingsApi->list_storage_settings: %s\n" % e)
```

### Parameters

| Name             | Type    | Description                                                                        | Notes      |
| ---------------- | ------- | ---------------------------------------------------------------------------------- | ---------- |
| **teamspace_id** | **str** | Teamspace id should be empty, if the request is about an action on workspace level | [optional] |
| **page**         | **int** | pagination offset                                                                  | [optional] |
| **per_page**     | **int** | pagination limit                                                                   | [optional] |

### Return type

[**StorageSettingsListResponse**](StorageSettingsListResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description                               | Response headers |
| ----------- | ----------------------------------------- | ---------------- |
| **200**     | Successful storage settings list response | -                |
| **0**       | error response                            | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_storage_setting_by_id**

> patch_storage_setting_by_id(stset_id, storage_setting_update_request, teamspace_id=teamspace_id)

Update storage setting

update storage setting given by the user

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
    api_instance = tiledb.cloud._common.api_v4.StoragesettingsApi(api_client)
    stset_id = 'stset_id_example' # str | The storage setting id in the form stset_9m4e2mr0ui3e8a215n4g
storage_setting_update_request = tiledb.cloud._common.api_v4.StorageSettingUpdateRequest() # StorageSettingUpdateRequest | storage setting update details
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Update storage setting
        api_instance.patch_storage_setting_by_id(stset_id, storage_setting_update_request, teamspace_id=teamspace_id)
    except ApiException as e:
        print("Exception when calling StoragesettingsApi->patch_storage_setting_by_id: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.StoragesettingsApi(api_client)
    stset_id = 'stset_id_example' # str | The storage setting id in the form stset_9m4e2mr0ui3e8a215n4g
storage_setting_update_request = tiledb.cloud._common.api_v4.StorageSettingUpdateRequest() # StorageSettingUpdateRequest | storage setting update details
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Update storage setting
        api_instance.patch_storage_setting_by_id(stset_id, storage_setting_update_request, teamspace_id=teamspace_id)
    except ApiException as e:
        print("Exception when calling StoragesettingsApi->patch_storage_setting_by_id: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.StoragesettingsApi(api_client)
    stset_id = 'stset_id_example' # str | The storage setting id in the form stset_9m4e2mr0ui3e8a215n4g
storage_setting_update_request = tiledb.cloud._common.api_v4.StorageSettingUpdateRequest() # StorageSettingUpdateRequest | storage setting update details
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Update storage setting
        api_instance.patch_storage_setting_by_id(stset_id, storage_setting_update_request, teamspace_id=teamspace_id)
    except ApiException as e:
        print("Exception when calling StoragesettingsApi->patch_storage_setting_by_id: %s\n" % e)
```

### Parameters

| Name                               | Type                                                              | Description                                                                        | Notes      |
| ---------------------------------- | ----------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ---------- |
| **stset_id**                       | **str**                                                           | The storage setting id in the form stset_9m4e2mr0ui3e8a215n4g                      |
| **storage_setting_update_request** | [**StorageSettingUpdateRequest**](StorageSettingUpdateRequest.md) | storage setting update details                                                     |
| **teamspace_id**                   | **str**                                                           | Teamspace id should be empty, if the request is about an action on workspace level | [optional] |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description                                  | Response headers |
| ----------- | -------------------------------------------- | ---------------- |
| **204**     | The storage setting was updated successfully | -                |
| **404**     | Storage setting does not exist               | -                |
| **0**       | error response                               | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
