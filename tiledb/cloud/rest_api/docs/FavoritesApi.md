# tiledb.cloud.rest_api.FavoritesApi

All URIs are relative to *http://localhost/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_favorite**](FavoritesApi.md#add_favorite) | **POST** /favorites | 
[**delete_favorite**](FavoritesApi.md#delete_favorite) | **DELETE** /favorites/{id} | 
[**get_favorite**](FavoritesApi.md#get_favorite) | **GET** /favorites/{id} | 
[**list_favorites**](FavoritesApi.md#list_favorites) | **GET** /favorites | 


# **add_favorite**
> add_favorite(body=body)



Add a new favorite

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
    api_instance = tiledb.cloud.rest_api.FavoritesApi(api_client)
    body = tiledb.cloud.rest_api.FavoriteCreate() # FavoriteCreate |  (optional)

    try:
        api_instance.add_favorite(body=body)
    except ApiException as e:
        print("Exception when calling FavoritesApi->add_favorite: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.FavoritesApi(api_client)
    body = tiledb.cloud.rest_api.FavoriteCreate() # FavoriteCreate |  (optional)

    try:
        api_instance.add_favorite(body=body)
    except ApiException as e:
        print("Exception when calling FavoritesApi->add_favorite: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FavoriteCreate**](FavoriteCreate.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Item added to favorites successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_favorite**
> delete_favorite(id)



Delete specific favorite

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
    api_instance = tiledb.cloud.rest_api.FavoritesApi(api_client)
    id = 'id_example' # str | The uuid of the favorite

    try:
        api_instance.delete_favorite(id)
    except ApiException as e:
        print("Exception when calling FavoritesApi->delete_favorite: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.FavoritesApi(api_client)
    id = 'id_example' # str | The uuid of the favorite

    try:
        api_instance.delete_favorite(id)
    except ApiException as e:
        print("Exception when calling FavoritesApi->delete_favorite: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The uuid of the favorite | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Favorite item deleted successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_favorite**
> Favorite get_favorite(id)



Fetch specific favorite of a user

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
    api_instance = tiledb.cloud.rest_api.FavoritesApi(api_client)
    id = 'id_example' # str | The uuid of the favorite

    try:
        api_response = api_instance.get_favorite(id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FavoritesApi->get_favorite: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.FavoritesApi(api_client)
    id = 'id_example' # str | The uuid of the favorite

    try:
        api_response = api_instance.get_favorite(id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FavoritesApi->get_favorite: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The uuid of the favorite | 

### Return type

[**Favorite**](Favorite.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_favorites**
> FavoritesData list_favorites(type=type)



Fetch all favorites of connected user

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
    api_instance = tiledb.cloud.rest_api.FavoritesApi(api_client)
    type = 'type_example' # str | The type of the desired favorites e.g. arrays (optional)

    try:
        api_response = api_instance.list_favorites(type=type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FavoritesApi->list_favorites: %s\n" % e)
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
    api_instance = tiledb.cloud.rest_api.FavoritesApi(api_client)
    type = 'type_example' # str | The type of the desired favorites e.g. arrays (optional)

    try:
        api_response = api_instance.list_favorites(type=type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FavoritesApi->list_favorites: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **type** | **str**| The type of the desired favorites e.g. arrays | [optional] 

### Return type

[**FavoritesData**](FavoritesData.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Available favorites are returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

