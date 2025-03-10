# tiledb.cloud.\_common.api_v4.AssetsApi

All URIs are relative to *https://api.tiledb.com/v4*

| Method                                      | HTTP request                   | Description                                     |
| ------------------------------------------- | ------------------------------ | ----------------------------------------------- |
| [**list_assets**](AssetsApi.md#list_assets) | **GET** /assets/{teamspace_id} | Retrieves asset listing for the given teamspace |

# **list_assets**

> AssetListResponse list_assets(teamspace_id, page=page, per_page=per_page, asset_type=asset_type, created_by=created_by, order_by=order_by)

Retrieves asset listing for the given teamspace

End point to retrieve assets for the passed teamspace

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
    api_instance = tiledb.cloud._common.api_v4.AssetsApi(api_client)
    teamspace_id = 'teamspace_id_example' # str | The teamspace id in the form ts_9m4e2mr0ui3e8a215n4g
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
asset_type = tiledb.cloud._common.api_v4.AssetType() # AssetType | asset type to filter to (optional)
created_by = 'created_by_example' # str | users that created the asset to filter to (optional)
order_by = 'order_by_example' # str | order by string (optional)

    try:
        # Retrieves asset listing for the given teamspace
        api_response = api_instance.list_assets(teamspace_id, page=page, per_page=per_page, asset_type=asset_type, created_by=created_by, order_by=order_by)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AssetsApi->list_assets: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.AssetsApi(api_client)
    teamspace_id = 'teamspace_id_example' # str | The teamspace id in the form ts_9m4e2mr0ui3e8a215n4g
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
asset_type = tiledb.cloud._common.api_v4.AssetType() # AssetType | asset type to filter to (optional)
created_by = 'created_by_example' # str | users that created the asset to filter to (optional)
order_by = 'order_by_example' # str | order by string (optional)

    try:
        # Retrieves asset listing for the given teamspace
        api_response = api_instance.list_assets(teamspace_id, page=page, per_page=per_page, asset_type=asset_type, created_by=created_by, order_by=order_by)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AssetsApi->list_assets: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.AssetsApi(api_client)
    teamspace_id = 'teamspace_id_example' # str | The teamspace id in the form ts_9m4e2mr0ui3e8a215n4g
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
asset_type = tiledb.cloud._common.api_v4.AssetType() # AssetType | asset type to filter to (optional)
created_by = 'created_by_example' # str | users that created the asset to filter to (optional)
order_by = 'order_by_example' # str | order by string (optional)

    try:
        # Retrieves asset listing for the given teamspace
        api_response = api_instance.list_assets(teamspace_id, page=page, per_page=per_page, asset_type=asset_type, created_by=created_by, order_by=order_by)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AssetsApi->list_assets: %s\n" % e)
```

### Parameters

| Name             | Type                 | Description                                          | Notes      |
| ---------------- | -------------------- | ---------------------------------------------------- | ---------- |
| **teamspace_id** | **str**              | The teamspace id in the form ts_9m4e2mr0ui3e8a215n4g |
| **page**         | **int**              | pagination offset                                    | [optional] |
| **per_page**     | **int**              | pagination limit                                     | [optional] |
| **asset_type**   | [**AssetType**](.md) | asset type to filter to                              | [optional] |
| **created_by**   | **str**              | users that created the asset to filter to            | [optional] |
| **order_by**     | **str**              | order by string                                      | [optional] |

### Return type

[**AssetListResponse**](AssetListResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description                       | Response headers |
| ----------- | --------------------------------- | ---------------- |
| **200**     | Successful asset listing response | -                |
| **404**     | Teamspace not found               | -                |
| **0**       | error response                    | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
