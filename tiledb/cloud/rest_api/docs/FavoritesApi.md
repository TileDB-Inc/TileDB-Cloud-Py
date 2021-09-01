# rest_api.FavoritesApi

All URIs are relative to *http://localhost/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_favorite_id**](FavoritesApi.md#delete_favorite_id) | **DELETE** /favorites/{id} | 
[**get_favorite**](FavoritesApi.md#get_favorite) | **GET** /favorites/{id} | 
[**get_favorites**](FavoritesApi.md#get_favorites) | **GET** /favorites | 
[**post_favorite**](FavoritesApi.md#post_favorite) | **POST** /favorites | 


# **delete_favorite_id**
> delete_favorite_id(id)



Delete specific favorite

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.FavoritesApi(api_client)
    id = 'id_example' # str | The uuid of the favorite

    try:
        api_instance.delete_favorite_id(id)
    except ApiException as e:
        print("Exception when calling FavoritesApi->delete_favorite_id: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.FavoritesApi(api_client)
    id = 'id_example' # str | The uuid of the favorite

    try:
        api_instance.delete_favorite_id(id)
    except ApiException as e:
        print("Exception when calling FavoritesApi->delete_favorite_id: %s\n" % e)
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
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_favorite**
> Favorite get_favorite(id)



Fetch specific favorite of a user

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.FavoritesApi(api_client)
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
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.FavoritesApi(api_client)
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

# **get_favorites**
> list[Favorite] get_favorites(type=type)



Fetch all favorites of connected user

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.FavoritesApi(api_client)
    type = 'type_example' # str | The type of the desired favorites e.g. arrays (optional)

    try:
        api_response = api_instance.get_favorites(type=type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FavoritesApi->get_favorites: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.FavoritesApi(api_client)
    type = 'type_example' # str | The type of the desired favorites e.g. arrays (optional)

    try:
        api_response = api_instance.get_favorites(type=type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FavoritesApi->get_favorites: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **type** | **str**| The type of the desired favorites e.g. arrays | [optional] 

### Return type

[**list[Favorite]**](Favorite.md)

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

# **post_favorite**
> post_favorite(body=body)



Add a new favorite

### Example

* Api Key Authentication (ApiKeyAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.FavoritesApi(api_client)
    body = rest_api.FavoriteUpdate() # FavoriteUpdate |  (optional)

    try:
        api_instance.post_favorite(body=body)
    except ApiException as e:
        print("Exception when calling FavoritesApi->post_favorite: %s\n" % e)
```

* Basic Authentication (BasicAuth):
```python
from __future__ import print_function
import time
import rest_api
from rest_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = rest_api.Configuration(
    host = "http://localhost/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration = rest_api.Configuration(
    host = "http://localhost/v1",
    api_key = {
        'X-TILEDB-REST-API-KEY': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-TILEDB-REST-API-KEY'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = rest_api.FavoritesApi(api_client)
    body = rest_api.FavoriteUpdate() # FavoriteUpdate |  (optional)

    try:
        api_instance.post_favorite(body=body)
    except ApiException as e:
        print("Exception when calling FavoritesApi->post_favorite: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FavoriteUpdate**](FavoriteUpdate.md)|  | [optional] 

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
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

