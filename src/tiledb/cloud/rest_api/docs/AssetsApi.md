# tiledb.cloud.rest_api.AssetsApi

All URIs are relative to _http://localhost_

| Method                                                    | HTTP request                   | Description |
| --------------------------------------------------------- | ------------------------------ | ----------- |
| [**list_assets**](AssetsApi.md#list_assets)               | **GET** /v1/assets/{namespace} |
| [**list_public_assets**](AssetsApi.md#list_public_assets) | **GET** /v1/public_assets      |

# **list_assets**

> AssetListResponse list_assets(namespace, asset_type=asset_type, ownership_level=ownership_level, depth=depth, search=search, page=page, per_page=per_page, order_by=order_by, expand=expand)

List assets in a namespace

### Example

- Api Key Authentication (ApiKeyAuth):

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
    api_instance = tiledb.cloud.rest_api.AssetsApi(api_client)
    namespace = 'namespace_example' # str | namespace
asset_type = 'asset_type_example' # str | asset_type to filter to (optional)
ownership_level = 'ownership_level_example' # str | ownership_level to filter to (owned, shared) (optional)
depth = 'depth_example' # str | depth of assets to be returned (optional)
search = 'search_example' # str | search string (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
order_by = 'order_by_example' # str | order by a specific property, defaults to `created_at desc` supported values are created_at, name, asset_type can also include the order type (asc or desc) separated by space i.e. `name asc` `name desc` etc.  (optional)
expand = 'expand_example' # str | expansion option for the AssetInfo object to be added to the response (optional)

    try:
        api_response = api_instance.list_assets(namespace, asset_type=asset_type, ownership_level=ownership_level, depth=depth, search=search, page=page, per_page=per_page, order_by=order_by, expand=expand)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AssetsApi->list_assets: %s\n" % e)
```

- Basic Authentication (BasicAuth):

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
    api_instance = tiledb.cloud.rest_api.AssetsApi(api_client)
    namespace = 'namespace_example' # str | namespace
asset_type = 'asset_type_example' # str | asset_type to filter to (optional)
ownership_level = 'ownership_level_example' # str | ownership_level to filter to (owned, shared) (optional)
depth = 'depth_example' # str | depth of assets to be returned (optional)
search = 'search_example' # str | search string (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
order_by = 'order_by_example' # str | order by a specific property, defaults to `created_at desc` supported values are created_at, name, asset_type can also include the order type (asc or desc) separated by space i.e. `name asc` `name desc` etc.  (optional)
expand = 'expand_example' # str | expansion option for the AssetInfo object to be added to the response (optional)

    try:
        api_response = api_instance.list_assets(namespace, asset_type=asset_type, ownership_level=ownership_level, depth=depth, search=search, page=page, per_page=per_page, order_by=order_by, expand=expand)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AssetsApi->list_assets: %s\n" % e)
```

### Parameters

| Name                | Type    | Description                                                                                                                                                                                                                                   | Notes      |
| ------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| **namespace**       | **str** | namespace                                                                                                                                                                                                                                     |
| **asset_type**      | **str** | asset_type to filter to                                                                                                                                                                                                                       | [optional] |
| **ownership_level** | **str** | ownership_level to filter to (owned, shared)                                                                                                                                                                                                  | [optional] |
| **depth**           | **str** | depth of assets to be returned                                                                                                                                                                                                                | [optional] |
| **search**          | **str** | search string                                                                                                                                                                                                                                 | [optional] |
| **page**            | **int** | pagination offset                                                                                                                                                                                                                             | [optional] |
| **per_page**        | **int** | pagination limit                                                                                                                                                                                                                              | [optional] |
| **order_by**        | **str** | order by a specific property, defaults to &#x60;created_at desc&#x60; supported values are created_at, name, asset_type can also include the order type (asc or desc) separated by space i.e. &#x60;name asc&#x60; &#x60;name desc&#x60; etc. | [optional] |
| **expand**          | **str** | expansion option for the AssetInfo object to be added to the response                                                                                                                                                                         | [optional] |

### Return type

[**AssetListResponse**](AssetListResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description               | Response headers |
| ----------- | ------------------------- | ---------------- |
| **200**     | Successful list of assets | -                |
| **502**     | Bad Gateway               | -                |
| **0**       | error response            | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_public_assets**

> AssetListResponse list_public_assets(asset_type=asset_type, depth=depth, search=search, page=page, per_page=per_page, order_by=order_by)

List public assets

### Example

- Api Key Authentication (ApiKeyAuth):

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
    api_instance = tiledb.cloud.rest_api.AssetsApi(api_client)
    asset_type = 'asset_type_example' # str | asset_type to filter to (optional)
depth = 'depth_example' # str | depth of assets to be returned (optional)
search = 'search_example' # str | search string (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
order_by = 'order_by_example' # str | order by a specific property, defaults to `created_at desc` supported values are created_at, name, asset_type can also include the order type (asc or desc) separated by space i.e. `name asc` `name desc` etc.  (optional)

    try:
        api_response = api_instance.list_public_assets(asset_type=asset_type, depth=depth, search=search, page=page, per_page=per_page, order_by=order_by)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AssetsApi->list_public_assets: %s\n" % e)
```

- Basic Authentication (BasicAuth):

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
    api_instance = tiledb.cloud.rest_api.AssetsApi(api_client)
    asset_type = 'asset_type_example' # str | asset_type to filter to (optional)
depth = 'depth_example' # str | depth of assets to be returned (optional)
search = 'search_example' # str | search string (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)
order_by = 'order_by_example' # str | order by a specific property, defaults to `created_at desc` supported values are created_at, name, asset_type can also include the order type (asc or desc) separated by space i.e. `name asc` `name desc` etc.  (optional)

    try:
        api_response = api_instance.list_public_assets(asset_type=asset_type, depth=depth, search=search, page=page, per_page=per_page, order_by=order_by)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AssetsApi->list_public_assets: %s\n" % e)
```

### Parameters

| Name           | Type    | Description                                                                                                                                                                                                                                   | Notes      |
| -------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| **asset_type** | **str** | asset_type to filter to                                                                                                                                                                                                                       | [optional] |
| **depth**      | **str** | depth of assets to be returned                                                                                                                                                                                                                | [optional] |
| **search**     | **str** | search string                                                                                                                                                                                                                                 | [optional] |
| **page**       | **int** | pagination offset                                                                                                                                                                                                                             | [optional] |
| **per_page**   | **int** | pagination limit                                                                                                                                                                                                                              | [optional] |
| **order_by**   | **str** | order by a specific property, defaults to &#x60;created_at desc&#x60; supported values are created_at, name, asset_type can also include the order type (asc or desc) separated by space i.e. &#x60;name asc&#x60; &#x60;name desc&#x60; etc. | [optional] |

### Return type

[**AssetListResponse**](AssetListResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description               | Response headers |
| ----------- | ------------------------- | ---------------- |
| **200**     | Successful list of assets | -                |
| **502**     | Bad Gateway               | -                |
| **0**       | error response            | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
