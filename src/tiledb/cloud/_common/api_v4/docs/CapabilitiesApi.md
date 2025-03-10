# tiledb.cloud.\_common.api_v4.CapabilitiesApi

All URIs are relative to *https://api.tiledb.com/v4*

| Method                                                                    | HTTP request          | Description           |
| ------------------------------------------------------------------------- | --------------------- | --------------------- |
| [**handle_get_capabilities**](CapabilitiesApi.md#handle_get_capabilities) | **GET** /capabilities | Get REST capabilities |

# **handle_get_capabilities**

> RestCapabilities handle_get_capabilities()

Get REST capabilities

Get REST capabilities

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
    api_instance = tiledb.cloud._common.api_v4.CapabilitiesApi(api_client)

    try:
        # Get REST capabilities
        api_response = api_instance.handle_get_capabilities()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CapabilitiesApi->handle_get_capabilities: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.CapabilitiesApi(api_client)

    try:
        # Get REST capabilities
        api_response = api_instance.handle_get_capabilities()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CapabilitiesApi->handle_get_capabilities: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.CapabilitiesApi(api_client)

    try:
        # Get REST capabilities
        api_response = api_instance.handle_get_capabilities()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CapabilitiesApi->handle_get_capabilities: %s\n" % e)
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**RestCapabilities**](RestCapabilities.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description                 | Response headers |
| ----------- | --------------------------- | ---------------- |
| **200**     | Retrieved REST capabilities | -                |
| **0**       | error response              | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
