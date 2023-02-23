# tiledb.cloud._common.api_v2.OrganizationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_credential**](OrganizationApi.md#add_credential) | **POST** /v2/credentials/{namespace} | 
[**delete_credential**](OrganizationApi.md#delete_credential) | **DELETE** /v2/credentials/{namespace}/{name} | 
[**get_credential**](OrganizationApi.md#get_credential) | **GET** /v2/credentials/{namespace}/{name} | 
[**list_credentials**](OrganizationApi.md#list_credentials) | **GET** /v2/credentials/{namespace} | 
[**update_credential**](OrganizationApi.md#update_credential) | **PATCH** /v2/credentials/{namespace}/{name} | 


# **add_credential**
> add_credential(namespace, access_credential, provider=provider, page=page, per_page=per_page)



Create a new credential for the namespace

### Example

* Api Key Authentication (ApiKeyAuth):
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
    api_instance = tiledb.cloud._common.api_v2.OrganizationApi(api_client)
    namespace = 'namespace_example' # str | namespace
access_credential = tiledb.cloud._common.api_v2.AccessCredential() # AccessCredential | The new credentials to be created.
provider = 'provider_example' # str | Show only the credentials from this provider. This should be one of the CloudProvider enum values. (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        api_instance.add_credential(namespace, access_credential, provider=provider, page=page, per_page=per_page)
    except ApiException as e:
        print("Exception when calling OrganizationApi->add_credential: %s\n" % e)
```

* Basic Authentication (BasicAuth):
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
    api_instance = tiledb.cloud._common.api_v2.OrganizationApi(api_client)
    namespace = 'namespace_example' # str | namespace
access_credential = tiledb.cloud._common.api_v2.AccessCredential() # AccessCredential | The new credentials to be created.
provider = 'provider_example' # str | Show only the credentials from this provider. This should be one of the CloudProvider enum values. (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        api_instance.add_credential(namespace, access_credential, provider=provider, page=page, per_page=per_page)
    except ApiException as e:
        print("Exception when calling OrganizationApi->add_credential: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace | 
 **access_credential** | [**AccessCredential**](AccessCredential.md)| The new credentials to be created. | 
 **provider** | **str**| Show only the credentials from this provider. This should be one of the CloudProvider enum values. | [optional] 
 **page** | **int**| pagination offset | [optional] 
 **per_page** | **int**| pagination limit | [optional] 

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
**204** | The new credential was successfully added. |  -  |
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_credential**
> delete_credential(namespace, name)



Delete the named access credential. Any arrays still set to use this credential will use the namespace's default and may become unreachable.

### Example

* Api Key Authentication (ApiKeyAuth):
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
    api_instance = tiledb.cloud._common.api_v2.OrganizationApi(api_client)
    namespace = 'namespace_example' # str | namespace
name = 'name_example' # str | A URL-safe version of the credential's user-provided name

    try:
        api_instance.delete_credential(namespace, name)
    except ApiException as e:
        print("Exception when calling OrganizationApi->delete_credential: %s\n" % e)
```

* Basic Authentication (BasicAuth):
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
    api_instance = tiledb.cloud._common.api_v2.OrganizationApi(api_client)
    namespace = 'namespace_example' # str | namespace
name = 'name_example' # str | A URL-safe version of the credential's user-provided name

    try:
        api_instance.delete_credential(namespace, name)
    except ApiException as e:
        print("Exception when calling OrganizationApi->delete_credential: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace | 
 **name** | **str**| A URL-safe version of the credential&#39;s user-provided name | 

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
**204** | The credential was deleted successfully |  -  |
**502** | Bad Gateway |  -  |
**0** | Error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_credential**
> AccessCredential get_credential(namespace, name)



Retrieve an access credential by name

### Example

* Api Key Authentication (ApiKeyAuth):
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
    api_instance = tiledb.cloud._common.api_v2.OrganizationApi(api_client)
    namespace = 'namespace_example' # str | namespace
name = 'name_example' # str | A URL-safe version of the credential's user-provided name

    try:
        api_response = api_instance.get_credential(namespace, name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationApi->get_credential: %s\n" % e)
```

* Basic Authentication (BasicAuth):
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
    api_instance = tiledb.cloud._common.api_v2.OrganizationApi(api_client)
    namespace = 'namespace_example' # str | namespace
name = 'name_example' # str | A URL-safe version of the credential's user-provided name

    try:
        api_response = api_instance.get_credential(namespace, name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationApi->get_credential: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace | 
 **name** | **str**| A URL-safe version of the credential&#39;s user-provided name | 

### Return type

[**AccessCredential**](AccessCredential.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Credential exists and can be returned |  -  |
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_credentials**
> AccessCredentialsData list_credentials(namespace, provider=provider, page=page, per_page=per_page)



List the credentials available in the namespace

### Example

* Api Key Authentication (ApiKeyAuth):
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
    api_instance = tiledb.cloud._common.api_v2.OrganizationApi(api_client)
    namespace = 'namespace_example' # str | namespace
provider = 'provider_example' # str | Show only the credentials from this provider. This should be one of the CloudProvider enum values. (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        api_response = api_instance.list_credentials(namespace, provider=provider, page=page, per_page=per_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationApi->list_credentials: %s\n" % e)
```

* Basic Authentication (BasicAuth):
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
    api_instance = tiledb.cloud._common.api_v2.OrganizationApi(api_client)
    namespace = 'namespace_example' # str | namespace
provider = 'provider_example' # str | Show only the credentials from this provider. This should be one of the CloudProvider enum values. (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        api_response = api_instance.list_credentials(namespace, provider=provider, page=page, per_page=per_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationApi->list_credentials: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace | 
 **provider** | **str**| Show only the credentials from this provider. This should be one of the CloudProvider enum values. | [optional] 
 **page** | **int**| pagination offset | [optional] 
 **per_page** | **int**| pagination limit | [optional] 

### Return type

[**AccessCredentialsData**](AccessCredentialsData.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Available credentials are returned |  -  |
**502** | Bad Gateway |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_credential**
> update_credential(namespace, name, access_credential)



Update the named access credential. This will also update the information used to access arrays set to use this credential.

### Example

* Api Key Authentication (ApiKeyAuth):
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
    api_instance = tiledb.cloud._common.api_v2.OrganizationApi(api_client)
    namespace = 'namespace_example' # str | namespace
name = 'name_example' # str | A URL-safe version of the credential's user-provided name
access_credential = tiledb.cloud._common.api_v2.AccessCredential() # AccessCredential | Changes to make to this credential

    try:
        api_instance.update_credential(namespace, name, access_credential)
    except ApiException as e:
        print("Exception when calling OrganizationApi->update_credential: %s\n" % e)
```

* Basic Authentication (BasicAuth):
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
    api_instance = tiledb.cloud._common.api_v2.OrganizationApi(api_client)
    namespace = 'namespace_example' # str | namespace
name = 'name_example' # str | A URL-safe version of the credential's user-provided name
access_credential = tiledb.cloud._common.api_v2.AccessCredential() # AccessCredential | Changes to make to this credential

    try:
        api_instance.update_credential(namespace, name, access_credential)
    except ApiException as e:
        print("Exception when calling OrganizationApi->update_credential: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace | 
 **name** | **str**| A URL-safe version of the credential&#39;s user-provided name | 
 **access_credential** | [**AccessCredential**](AccessCredential.md)| Changes to make to this credential | 

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
**204** | The credential was updated successfully |  -  |
**502** | Bad Gateway |  -  |
**0** | Error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

