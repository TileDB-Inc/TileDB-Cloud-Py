# tiledb.cloud.rest_api.UserApi

All URIs are relative to *http://localhost/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_aws_access_credentials**](UserApi.md#add_aws_access_credentials) | **POST** /credentials/{namespace}/aws | 
[**add_user_to_organization**](UserApi.md#add_user_to_organization) | **POST** /organizations/{organization}/user | 
[**check_aws_access_credentials**](UserApi.md#check_aws_access_credentials) | **GET** /credentials/{namespace}/aws | 
[**check_aws_access_credentials_by_name**](UserApi.md#check_aws_access_credentials_by_name) | **GET** /credentials/{namespace}/aws/{name} | 
[**confirm_email**](UserApi.md#confirm_email) | **POST** /user/confirm_email | 
[**create_user**](UserApi.md#create_user) | **POST** /user | 
[**delete_aws_access_credentials**](UserApi.md#delete_aws_access_credentials) | **DELETE** /credentials/{namespace}/aws/{name} | 
[**delete_user**](UserApi.md#delete_user) | **DELETE** /users/{username} | 
[**delete_user_from_organization**](UserApi.md#delete_user_from_organization) | **DELETE** /organizations/{organization}/{username} | 
[**get_organization_user**](UserApi.md#get_organization_user) | **GET** /organizations/{organization}/{username} | 
[**get_session**](UserApi.md#get_session) | **GET** /session | 
[**get_token_scopes**](UserApi.md#get_token_scopes) | **GET** /tokens/scopes | 
[**get_user**](UserApi.md#get_user) | **GET** /user | 
[**get_user_with_username**](UserApi.md#get_user_with_username) | **GET** /users/{username} | 
[**request_token**](UserApi.md#request_token) | **POST** /token | 
[**reset_user_password**](UserApi.md#reset_user_password) | **POST** /user/password_reset | 
[**revoke_token**](UserApi.md#revoke_token) | **DELETE** /tokens/{token} | 
[**tokens_get**](UserApi.md#tokens_get) | **GET** /tokens | 
[**tokens_session_get**](UserApi.md#tokens_session_get) | **GET** /tokens/session | 
[**update_aws_access_credentials**](UserApi.md#update_aws_access_credentials) | **PATCH** /credentials/{namespace}/aws/{name} | 
[**update_user**](UserApi.md#update_user) | **PATCH** /users/{username} | 
[**update_user_in_organization**](UserApi.md#update_user_in_organization) | **PATCH** /organizations/{organization}/{username} | 


# **add_aws_access_credentials**
> add_aws_access_credentials(namespace, aws_access_credentials)



Add aws keys

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import user_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.aws_access_credentials import AWSAccessCredentials
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
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)
    namespace = "namespace_example" # str | namespace
    aws_access_credentials = AWSAccessCredentials(
        secret_access_key="secret_access_key_example",
        access_key_id="access_key_id_example",
        service_role_arn="service_role_arn_example",
        name="name_example",
        default=True,
        buckets=[
            "s3://company-bucket-1/tiledb/",
        ],
    ) # AWSAccessCredentials | aws access credentials to store for a namespace

    # example passing only required values which don't have defaults set
    try:
        api_instance.add_aws_access_credentials(namespace, aws_access_credentials)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling UserApi->add_aws_access_credentials: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace |
 **aws_access_credentials** | [**AWSAccessCredentials**](AWSAccessCredentials.md)| aws access credentials to store for a namespace |

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
**204** | AWS keys added successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_user_to_organization**
> add_user_to_organization(organization, user)



add a user to an organization

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import user_api
from tiledb.cloud.rest_api.model.organization_user import OrganizationUser
from tiledb.cloud.rest_api.model.error import Error
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
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)
    organization = "organization_example" # str | organization name
    user = OrganizationUser(
        user_id="00000000-0000-0000-0000-000000000000",
        organization_id="00000000-0000-0000-0000-000000000000",
        username="username",
        organization_name="MyOrganization",
        role=OrganizationRoles("owner"),
        allowed_actions=[
            NamespaceActions("read"),
        ],
    ) # OrganizationUser | user to add

    # example passing only required values which don't have defaults set
    try:
        api_instance.add_user_to_organization(organization, user)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling UserApi->add_user_to_organization: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization** | **str**| organization name |
 **user** | [**OrganizationUser**](OrganizationUser.md)| user to add |

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
**204** | user added to organization successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **check_aws_access_credentials**
> [AWSAccessCredentials] check_aws_access_credentials(namespace)



Check if aws keys are set

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import user_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.aws_access_credentials import AWSAccessCredentials
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
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)
    namespace = "namespace_example" # str | namespace

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.check_aws_access_credentials(namespace)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling UserApi->check_aws_access_credentials: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace |

### Return type

[**[AWSAccessCredentials]**](AWSAccessCredentials.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | AWS keys are set |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **check_aws_access_credentials_by_name**
> AWSAccessCredentials check_aws_access_credentials_by_name(namespace, name)



Check if aws keys are set by name

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import user_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.aws_access_credentials import AWSAccessCredentials
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
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)
    namespace = "namespace_example" # str | namespace
    name = "name_example" # str | name

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.check_aws_access_credentials_by_name(namespace, name)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling UserApi->check_aws_access_credentials_by_name: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace |
 **name** | **str**| name |

### Return type

[**AWSAccessCredentials**](AWSAccessCredentials.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | AWS keys are set |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **confirm_email**
> confirm_email()



confirm user email

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import user_api
from tiledb.cloud.rest_api.model.error import Error
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
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        api_instance.confirm_email()
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling UserApi->confirm_email: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

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
**204** | User email confirmed successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_user**
> create_user(user)



create a user

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import user_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.user import User
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
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)
    user = User(
        id="00000000-0000-0000-0000-000000000000",
        username="username",
        password="password",
        name="Jane Doe",
        email="jane.doe@example.com",
        company="TileDB",
        logo="logo_example",
        timezone="Europe/Athens",
        allowed_actions=[
            NamespaceActions("read"),
        ],
        default_s3_path="default_s3_path_example",
        default_s3_path_credentials_name="default_s3_path_credentials_name_example",
        default_namespace_charged="default_namespace_charged_example",
    ) # User | user to create

    # example passing only required values which don't have defaults set
    try:
        api_instance.create_user(user)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling UserApi->create_user: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | [**User**](User.md)| user to create |

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
**204** | user created successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_aws_access_credentials**
> delete_aws_access_credentials(namespace, name)



delete a AWS Access credentials in a namespace. This will likely cause arrays to become unreachable

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import user_api
from tiledb.cloud.rest_api.model.error import Error
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
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)
    namespace = "namespace_example" # str | namespace
    name = "name_example" # str | name

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_aws_access_credentials(namespace, name)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling UserApi->delete_aws_access_credentials: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace |
 **name** | **str**| name |

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
**204** | AWS credentials deleted |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_user**
> delete_user(username)



delete a user

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import user_api
from tiledb.cloud.rest_api.model.error import Error
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
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)
    username = "username_example" # str | username or ID

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_user(username)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling UserApi->delete_user: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **str**| username or ID |

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
**204** | user deleted |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_user_from_organization**
> delete_user_from_organization(organization, username)



delete a user from an organization

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import user_api
from tiledb.cloud.rest_api.model.error import Error
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
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)
    organization = "organization_example" # str | organization name
    username = "username_example" # str | username to manipulate

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_user_from_organization(organization, username)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling UserApi->delete_user_from_organization: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization** | **str**| organization name |
 **username** | **str**| username to manipulate |

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
**204** | user delete from organization successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_organization_user**
> OrganizationUser get_organization_user(organization, username)



get a user from an organization

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import user_api
from tiledb.cloud.rest_api.model.organization_user import OrganizationUser
from tiledb.cloud.rest_api.model.error import Error
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
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)
    organization = "organization_example" # str | organization name
    username = "username_example" # str | username to manipulate

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_organization_user(organization, username)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling UserApi->get_organization_user: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization** | **str**| organization name |
 **username** | **str**| username to manipulate |

### Return type

[**OrganizationUser**](OrganizationUser.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | user from organization |  -  |
**404** | User is not in organization |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_session**
> Token get_session()



Get session token for user

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import user_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.token import Token
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
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)
    remember_me = "remember_me_example" # str | flag to create a token with expiration of 30 days, default is false (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_session(remember_me=remember_me)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling UserApi->get_session: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **remember_me** | **str**| flag to create a token with expiration of 30 days, default is false | [optional]

### Return type

[**Token**](Token.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Session token |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_token_scopes**
> [TokenScope] get_token_scopes()



retrieves available token scopes for a user

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import user_api
from tiledb.cloud.rest_api.model.token_scope import TokenScope
from tiledb.cloud.rest_api.model.error import Error
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
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        api_response = api_instance.get_token_scopes()
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling UserApi->get_token_scopes: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[TokenScope]**](TokenScope.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | available token scopes |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user**
> User get_user()



get a user

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import user_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.user import User
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
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        api_response = api_instance.get_user()
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling UserApi->get_user: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**User**](User.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | user details |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_with_username**
> User get_user_with_username(username)



get a user

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import user_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.user import User
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
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)
    username = "username_example" # str | username or ID

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_user_with_username(username)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling UserApi->get_user_with_username: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **str**| username or ID |

### Return type

[**User**](User.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | user details |  -  |
**404** | User does not exist |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **request_token**
> Token request_token()



Request an authorization token, optionally taken a TokenRequest object to set parameters on the token

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import user_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.token_request import TokenRequest
from tiledb.cloud.rest_api.model.token import Token
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
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)
    token_request = TokenRequest(
        expires=dateutil_parser('1970-01-01T00:00:00.00Z'),
        name="myToken",
        scope="*",
    ) # TokenRequest | token request object (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.request_token(token_request=token_request)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling UserApi->request_token: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token_request** | [**TokenRequest**](TokenRequest.md)| token request object | [optional]

### Return type

[**Token**](Token.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | token |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reset_user_password**
> reset_user_password(user)



reset user password

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import user_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.inline_object import InlineObject
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
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)
    user = InlineObject(
        password="password",
    ) # InlineObject | 

    # example passing only required values which don't have defaults set
    try:
        api_instance.reset_user_password(user)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling UserApi->reset_user_password: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | [**InlineObject**](InlineObject.md)|  |

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
**204** | User password updated successfully |  -  |
**404** | User not found |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **revoke_token**
> revoke_token(token)



revoke an authorization token

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import user_api
from tiledb.cloud.rest_api.model.error import Error
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
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)
    token = "token_example" # str | token name or token itself

    # example passing only required values which don't have defaults set
    try:
        api_instance.revoke_token(token)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling UserApi->revoke_token: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token** | **str**| token name or token itself |

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
**204** | revokation successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tokens_get**
> [Token] tokens_get()



Fetch a list of user tokens

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import user_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.token import Token
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
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        api_response = api_instance.tokens_get()
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling UserApi->tokens_get: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[Token]**](Token.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Array of user created non-session tokens |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tokens_session_get**
> [Token] tokens_session_get()



Fetch a list of user session tokens

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import user_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.token import Token
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
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        api_response = api_instance.tokens_session_get()
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling UserApi->tokens_session_get: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[Token]**](Token.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Array of user created session tokens |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_aws_access_credentials**
> update_aws_access_credentials(namespace, name, aws_access_credentials)



Update aws keys or associated buckets. This will update the key associations for each array in the namespace

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import user_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.aws_access_credentials import AWSAccessCredentials
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
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)
    namespace = "namespace_example" # str | namespace
    name = "name_example" # str | name
    aws_access_credentials = AWSAccessCredentials(
        secret_access_key="secret_access_key_example",
        access_key_id="access_key_id_example",
        service_role_arn="service_role_arn_example",
        name="name_example",
        default=True,
        buckets=[
            "s3://company-bucket-1/tiledb/",
        ],
    ) # AWSAccessCredentials | aws credentials to update

    # example passing only required values which don't have defaults set
    try:
        api_instance.update_aws_access_credentials(namespace, name, aws_access_credentials)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling UserApi->update_aws_access_credentials: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace |
 **name** | **str**| name |
 **aws_access_credentials** | [**AWSAccessCredentials**](AWSAccessCredentials.md)| aws credentials to update |

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
**204** | AWS keys updated successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user**
> update_user(username, user)



update a user

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import user_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.user import User
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
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)
    username = "username_example" # str | username or ID
    user = User(
        id="00000000-0000-0000-0000-000000000000",
        username="username",
        password="password",
        name="Jane Doe",
        email="jane.doe@example.com",
        company="TileDB",
        logo="logo_example",
        timezone="Europe/Athens",
        allowed_actions=[
            NamespaceActions("read"),
        ],
        default_s3_path="default_s3_path_example",
        default_s3_path_credentials_name="default_s3_path_credentials_name_example",
        default_namespace_charged="default_namespace_charged_example",
    ) # User | user details to update

    # example passing only required values which don't have defaults set
    try:
        api_instance.update_user(username, user)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling UserApi->update_user: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **str**| username or ID |
 **user** | [**User**](User.md)| user details to update |

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
**204** | user updated successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user_in_organization**
> update_user_in_organization(organization, username, user)



update a user in an organization

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import user_api
from tiledb.cloud.rest_api.model.organization_user import OrganizationUser
from tiledb.cloud.rest_api.model.error import Error
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
configuration.api_key['ApiKeyAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure HTTP basic authorization: BasicAuth
configuration = tiledb.cloud.rest_api.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with tiledb.cloud.rest_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)
    organization = "organization_example" # str | organization name
    username = "username_example" # str | username to manipulate
    user = OrganizationUser(
        user_id="00000000-0000-0000-0000-000000000000",
        organization_id="00000000-0000-0000-0000-000000000000",
        username="username",
        organization_name="MyOrganization",
        role=OrganizationRoles("owner"),
        allowed_actions=[
            NamespaceActions("read"),
        ],
    ) # OrganizationUser | user details to update

    # example passing only required values which don't have defaults set
    try:
        api_instance.update_user_in_organization(organization, username, user)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling UserApi->update_user_in_organization: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization** | **str**| organization name |
 **username** | **str**| username to manipulate |
 **user** | [**OrganizationUser**](OrganizationUser.md)| user details to update |

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
**204** | user update in organization successfully |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

