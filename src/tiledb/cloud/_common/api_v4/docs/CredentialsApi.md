# tiledb.cloud.\_common.api_v4.CredentialsApi

All URIs are relative to *https://api.tiledb.com/v4*

| Method                                                                       | HTTP request                   | Description               |
| ---------------------------------------------------------------------------- | ------------------------------ | ------------------------- |
| [**create_credential**](CredentialsApi.md#create_credential)                 | **POST** /credentials          | Create a credential       |
| [**delete_credential_by_name**](CredentialsApi.md#delete_credential_by_name) | **DELETE** /credentials/{name} | Delete user credential    |
| [**get_credential_by_name**](CredentialsApi.md#get_credential_by_name)       | **GET** /credentials/{name}    | Get user credential       |
| [**get_credentials**](CredentialsApi.md#get_credentials)                     | **GET** /credentials           | Get user credentials      |
| [**patch_credential_by_name**](CredentialsApi.md#patch_credential_by_name)   | **PATCH** /credentials/{name}  | Update user credential    |
| [**verify_credential**](CredentialsApi.md#verify_credential)                 | **POST** /credentials/verify   | Verify a given credential |

# **create_credential**

> create_credential(credential_create_request, teamspace_id=teamspace_id)

Create a credential

create a new credential, the user will create a new credential to access assets

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
    api_instance = tiledb.cloud._common.api_v4.CredentialsApi(api_client)
    credential_create_request = tiledb.cloud._common.api_v4.CredentialCreateRequest() # CredentialCreateRequest | the new credentials to be created
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Create a credential
        api_instance.create_credential(credential_create_request, teamspace_id=teamspace_id)
    except ApiException as e:
        print("Exception when calling CredentialsApi->create_credential: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.CredentialsApi(api_client)
    credential_create_request = tiledb.cloud._common.api_v4.CredentialCreateRequest() # CredentialCreateRequest | the new credentials to be created
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Create a credential
        api_instance.create_credential(credential_create_request, teamspace_id=teamspace_id)
    except ApiException as e:
        print("Exception when calling CredentialsApi->create_credential: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.CredentialsApi(api_client)
    credential_create_request = tiledb.cloud._common.api_v4.CredentialCreateRequest() # CredentialCreateRequest | the new credentials to be created
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Create a credential
        api_instance.create_credential(credential_create_request, teamspace_id=teamspace_id)
    except ApiException as e:
        print("Exception when calling CredentialsApi->create_credential: %s\n" % e)
```

### Parameters

| Name                          | Type                                                      | Description                                                                        | Notes      |
| ----------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------- | ---------- |
| **credential_create_request** | [**CredentialCreateRequest**](CredentialCreateRequest.md) | the new credentials to be created                                                  |
| **teamspace_id**              | **str**                                                   | Teamspace id should be empty, if the request is about an action on workspace level | [optional] |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description                               | Response headers |
| ----------- | ----------------------------------------- | ---------------- |
| **201**     | The new credential was successfully added | -                |
| **0**       | error response                            | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_credential_by_name**

> delete_credential_by_name(name, teamspace_id=teamspace_id)

Delete user credential

Delete the named access credential. Any arrays still set to use this credential will use the user's default and may become unreachable

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
    api_instance = tiledb.cloud._common.api_v4.CredentialsApi(api_client)
    name = 'name_example' # str | The name of the credentials to run CRUD operations against
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Delete user credential
        api_instance.delete_credential_by_name(name, teamspace_id=teamspace_id)
    except ApiException as e:
        print("Exception when calling CredentialsApi->delete_credential_by_name: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.CredentialsApi(api_client)
    name = 'name_example' # str | The name of the credentials to run CRUD operations against
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Delete user credential
        api_instance.delete_credential_by_name(name, teamspace_id=teamspace_id)
    except ApiException as e:
        print("Exception when calling CredentialsApi->delete_credential_by_name: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.CredentialsApi(api_client)
    name = 'name_example' # str | The name of the credentials to run CRUD operations against
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Delete user credential
        api_instance.delete_credential_by_name(name, teamspace_id=teamspace_id)
    except ApiException as e:
        print("Exception when calling CredentialsApi->delete_credential_by_name: %s\n" % e)
```

### Parameters

| Name             | Type    | Description                                                                        | Notes      |
| ---------------- | ------- | ---------------------------------------------------------------------------------- | ---------- |
| **name**         | **str** | The name of the credentials to run CRUD operations against                         |
| **teamspace_id** | **str** | Teamspace id should be empty, if the request is about an action on workspace level | [optional] |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description               | Response headers |
| ----------- | ------------------------- | ---------------- |
| **204**     | user credential deleted   | -                |
| **404**     | credential does not exist | -                |
| **0**       | error response            | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_credential_by_name**

> CredentialGetResponse get_credential_by_name(name, teamspace_id=teamspace_id)

Get user credential

get information about user credential by name

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
    api_instance = tiledb.cloud._common.api_v4.CredentialsApi(api_client)
    name = 'name_example' # str | The name of the credentials to run CRUD operations against
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Get user credential
        api_response = api_instance.get_credential_by_name(name, teamspace_id=teamspace_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CredentialsApi->get_credential_by_name: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.CredentialsApi(api_client)
    name = 'name_example' # str | The name of the credentials to run CRUD operations against
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Get user credential
        api_response = api_instance.get_credential_by_name(name, teamspace_id=teamspace_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CredentialsApi->get_credential_by_name: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.CredentialsApi(api_client)
    name = 'name_example' # str | The name of the credentials to run CRUD operations against
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Get user credential
        api_response = api_instance.get_credential_by_name(name, teamspace_id=teamspace_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CredentialsApi->get_credential_by_name: %s\n" % e)
```

### Parameters

| Name             | Type    | Description                                                                        | Notes      |
| ---------------- | ------- | ---------------------------------------------------------------------------------- | ---------- |
| **name**         | **str** | The name of the credentials to run CRUD operations against                         |
| **teamspace_id** | **str** | Teamspace id should be empty, if the request is about an action on workspace level | [optional] |

### Return type

[**CredentialGetResponse**](CredentialGetResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description                    | Response headers |
| ----------- | ------------------------------ | ---------------- |
| **200**     | Successful credential response | -                |
| **404**     | Credential does not exist      | -                |
| **0**       | error response                 | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_credentials**

> CredentialsListResponse get_credentials(teamspace_id=teamspace_id, provider=provider, type=type, page=page, per_page=per_page)

Get user credentials

list the credentials available for the user

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
    api_instance = tiledb.cloud._common.api_v4.CredentialsApi(api_client)
    teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)
provider = tiledb.cloud._common.api_v4.CloudProvider() # CloudProvider | Show only the credentials from this provider. This should be one of the CloudProvider enum values. (optional)
type = 'type_example' # str | Show only the credentials of this type. This should be one of the AccessCredentialType enum values. (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        # Get user credentials
        api_response = api_instance.get_credentials(teamspace_id=teamspace_id, provider=provider, type=type, page=page, per_page=per_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CredentialsApi->get_credentials: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.CredentialsApi(api_client)
    teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)
provider = tiledb.cloud._common.api_v4.CloudProvider() # CloudProvider | Show only the credentials from this provider. This should be one of the CloudProvider enum values. (optional)
type = 'type_example' # str | Show only the credentials of this type. This should be one of the AccessCredentialType enum values. (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        # Get user credentials
        api_response = api_instance.get_credentials(teamspace_id=teamspace_id, provider=provider, type=type, page=page, per_page=per_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CredentialsApi->get_credentials: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.CredentialsApi(api_client)
    teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)
provider = tiledb.cloud._common.api_v4.CloudProvider() # CloudProvider | Show only the credentials from this provider. This should be one of the CloudProvider enum values. (optional)
type = 'type_example' # str | Show only the credentials of this type. This should be one of the AccessCredentialType enum values. (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        # Get user credentials
        api_response = api_instance.get_credentials(teamspace_id=teamspace_id, provider=provider, type=type, page=page, per_page=per_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CredentialsApi->get_credentials: %s\n" % e)
```

### Parameters

| Name             | Type                     | Description                                                                                         | Notes      |
| ---------------- | ------------------------ | --------------------------------------------------------------------------------------------------- | ---------- |
| **teamspace_id** | **str**                  | Teamspace id should be empty, if the request is about an action on workspace level                  | [optional] |
| **provider**     | [**CloudProvider**](.md) | Show only the credentials from this provider. This should be one of the CloudProvider enum values.  | [optional] |
| **type**         | **str**                  | Show only the credentials of this type. This should be one of the AccessCredentialType enum values. | [optional] |
| **page**         | **int**                  | pagination offset                                                                                   | [optional] |
| **per_page**     | **int**                  | pagination limit                                                                                    | [optional] |

### Return type

[**CredentialsListResponse**](CredentialsListResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description                          | Response headers |
| ----------- | ------------------------------------ | ---------------- |
| **200**     | Successful credentials list response | -                |
| **0**       | error response                       | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_credential_by_name**

> patch_credential_by_name(name, credential_update_request, teamspace_id=teamspace_id)

Update user credential

update user credential given by the user

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
    api_instance = tiledb.cloud._common.api_v4.CredentialsApi(api_client)
    name = 'name_example' # str | The name of the credentials to run CRUD operations against
credential_update_request = tiledb.cloud._common.api_v4.CredentialUpdateRequest() # CredentialUpdateRequest | credential update details
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Update user credential
        api_instance.patch_credential_by_name(name, credential_update_request, teamspace_id=teamspace_id)
    except ApiException as e:
        print("Exception when calling CredentialsApi->patch_credential_by_name: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.CredentialsApi(api_client)
    name = 'name_example' # str | The name of the credentials to run CRUD operations against
credential_update_request = tiledb.cloud._common.api_v4.CredentialUpdateRequest() # CredentialUpdateRequest | credential update details
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Update user credential
        api_instance.patch_credential_by_name(name, credential_update_request, teamspace_id=teamspace_id)
    except ApiException as e:
        print("Exception when calling CredentialsApi->patch_credential_by_name: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.CredentialsApi(api_client)
    name = 'name_example' # str | The name of the credentials to run CRUD operations against
credential_update_request = tiledb.cloud._common.api_v4.CredentialUpdateRequest() # CredentialUpdateRequest | credential update details
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Update user credential
        api_instance.patch_credential_by_name(name, credential_update_request, teamspace_id=teamspace_id)
    except ApiException as e:
        print("Exception when calling CredentialsApi->patch_credential_by_name: %s\n" % e)
```

### Parameters

| Name                          | Type                                                      | Description                                                                        | Notes      |
| ----------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------- | ---------- |
| **name**                      | **str**                                                   | The name of the credentials to run CRUD operations against                         |
| **credential_update_request** | [**CredentialUpdateRequest**](CredentialUpdateRequest.md) | credential update details                                                          |
| **teamspace_id**              | **str**                                                   | Teamspace id should be empty, if the request is about an action on workspace level | [optional] |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description                             | Response headers |
| ----------- | --------------------------------------- | ---------------- |
| **204**     | The credential was updated successfully | -                |
| **0**       | error response                          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **verify_credential**

> verify_credential(credentials_verify_request, teamspace_id=teamspace_id)

Verify a given credential

verify the credentials connection for a namespace

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
    api_instance = tiledb.cloud._common.api_v4.CredentialsApi(api_client)
    credentials_verify_request = tiledb.cloud._common.api_v4.CredentialsVerifyRequest() # CredentialsVerifyRequest | credential to verify
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Verify a given credential
        api_instance.verify_credential(credentials_verify_request, teamspace_id=teamspace_id)
    except ApiException as e:
        print("Exception when calling CredentialsApi->verify_credential: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.CredentialsApi(api_client)
    credentials_verify_request = tiledb.cloud._common.api_v4.CredentialsVerifyRequest() # CredentialsVerifyRequest | credential to verify
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Verify a given credential
        api_instance.verify_credential(credentials_verify_request, teamspace_id=teamspace_id)
    except ApiException as e:
        print("Exception when calling CredentialsApi->verify_credential: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.CredentialsApi(api_client)
    credentials_verify_request = tiledb.cloud._common.api_v4.CredentialsVerifyRequest() # CredentialsVerifyRequest | credential to verify
teamspace_id = 'teamspace_id_example' # str | Teamspace id should be empty, if the request is about an action on workspace level (optional)

    try:
        # Verify a given credential
        api_instance.verify_credential(credentials_verify_request, teamspace_id=teamspace_id)
    except ApiException as e:
        print("Exception when calling CredentialsApi->verify_credential: %s\n" % e)
```

### Parameters

| Name                           | Type                                                        | Description                                                                        | Notes      |
| ------------------------------ | ----------------------------------------------------------- | ---------------------------------------------------------------------------------- | ---------- |
| **credentials_verify_request** | [**CredentialsVerifyRequest**](CredentialsVerifyRequest.md) | credential to verify                                                               |
| **teamspace_id**               | **str**                                                     | Teamspace id should be empty, if the request is about an action on workspace level | [optional] |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description           | Response headers |
| ----------- | --------------------- | ---------------- |
| **200**     | successful connection | -                |
| **0**       | error response        | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
