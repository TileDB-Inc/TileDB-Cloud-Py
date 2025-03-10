# tiledb.cloud.\_common.api_v4.AcademyApi

All URIs are relative to *https://api.tiledb.com/v4*

| Method                                                                   | HTTP request                                       | Description                                    |
| ------------------------------------------------------------------------ | -------------------------------------------------- | ---------------------------------------------- |
| [**get_academy_lessons**](AcademyApi.md#get_academy_lessons)             | **GET** /academy/lessons                           | Get information about user lessons             |
| [**get_academy_questionnaire**](AcademyApi.md#get_academy_questionnaire) | **GET** /academy/questionnaires/{questionnaire_id} | Get academy questionnaire information for user |
| [**put_academy_lessons**](AcademyApi.md#put_academy_lessons)             | **PUT** /academy/lessons                           | Academy lessons to create                      |
| [**put_academy_questionnaire**](AcademyApi.md#put_academy_questionnaire) | **PUT** /academy/questionnaires/{questionnaire_id} | Create or update academy questionnaire         |

# **get_academy_lessons**

> AcademyLessonsListResponse get_academy_lessons()

Get information about user lessons

Get a list of user lessons with details about each of them

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
    api_instance = tiledb.cloud._common.api_v4.AcademyApi(api_client)

    try:
        # Get information about user lessons
        api_response = api_instance.get_academy_lessons()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AcademyApi->get_academy_lessons: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.AcademyApi(api_client)

    try:
        # Get information about user lessons
        api_response = api_instance.get_academy_lessons()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AcademyApi->get_academy_lessons: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.AcademyApi(api_client)

    try:
        # Get information about user lessons
        api_response = api_instance.get_academy_lessons()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AcademyApi->get_academy_lessons: %s\n" % e)
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**AcademyLessonsListResponse**](AcademyLessonsListResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description     | Response headers |
| ----------- | --------------- | ---------------- |
| **200**     | Academy lessons | -                |
| **0**       | error response  | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_academy_questionnaire**

> AcademyQuestionnaireListResponse get_academy_questionnaire(questionnaire_id)

Get academy questionnaire information for user

Get academy questionnaire information for user. For example, questionnaire version, completion status and user answers

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
    api_instance = tiledb.cloud._common.api_v4.AcademyApi(api_client)
    questionnaire_id = 'questionnaire_id_example' # str | questionnaire's id

    try:
        # Get academy questionnaire information for user
        api_response = api_instance.get_academy_questionnaire(questionnaire_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AcademyApi->get_academy_questionnaire: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.AcademyApi(api_client)
    questionnaire_id = 'questionnaire_id_example' # str | questionnaire's id

    try:
        # Get academy questionnaire information for user
        api_response = api_instance.get_academy_questionnaire(questionnaire_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AcademyApi->get_academy_questionnaire: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.AcademyApi(api_client)
    questionnaire_id = 'questionnaire_id_example' # str | questionnaire's id

    try:
        # Get academy questionnaire information for user
        api_response = api_instance.get_academy_questionnaire(questionnaire_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AcademyApi->get_academy_questionnaire: %s\n" % e)
```

### Parameters

| Name                 | Type    | Description            | Notes |
| -------------------- | ------- | ---------------------- | ----- |
| **questionnaire_id** | **str** | questionnaire&#39;s id |

### Return type

[**AcademyQuestionnaireListResponse**](AcademyQuestionnaireListResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description                               | Response headers |
| ----------- | ----------------------------------------- | ---------------- |
| **200**     | Successful academy questionnaire response | -                |
| **404**     | answers not found                         | -                |
| **0**       | error response                            | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_academy_lessons**

> put_academy_lessons(academy_lesson)

Academy lessons to create

Create one or more user lessons

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
    api_instance = tiledb.cloud._common.api_v4.AcademyApi(api_client)
    academy_lesson = [tiledb.cloud._common.api_v4.AcademyLesson()] # list[AcademyLesson] | Academy lesson to create

    try:
        # Academy lessons to create
        api_instance.put_academy_lessons(academy_lesson)
    except ApiException as e:
        print("Exception when calling AcademyApi->put_academy_lessons: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.AcademyApi(api_client)
    academy_lesson = [tiledb.cloud._common.api_v4.AcademyLesson()] # list[AcademyLesson] | Academy lesson to create

    try:
        # Academy lessons to create
        api_instance.put_academy_lessons(academy_lesson)
    except ApiException as e:
        print("Exception when calling AcademyApi->put_academy_lessons: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.AcademyApi(api_client)
    academy_lesson = [tiledb.cloud._common.api_v4.AcademyLesson()] # list[AcademyLesson] | Academy lesson to create

    try:
        # Academy lessons to create
        api_instance.put_academy_lessons(academy_lesson)
    except ApiException as e:
        print("Exception when calling AcademyApi->put_academy_lessons: %s\n" % e)
```

### Parameters

| Name               | Type                                        | Description              | Notes |
| ------------------ | ------------------------------------------- | ------------------------ | ----- |
| **academy_lesson** | [**list[AcademyLesson]**](AcademyLesson.md) | Academy lesson to create |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description              | Response headers |
| ----------- | ------------------------ | ---------------- |
| **200**     | create or update success | -                |
| **0**       | error response           | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_academy_questionnaire**

> put_academy_questionnaire(questionnaire_id, academy_questionnaire_put_request)

Create or update academy questionnaire

Create a new questionnaire or update an existing one

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
    api_instance = tiledb.cloud._common.api_v4.AcademyApi(api_client)
    questionnaire_id = 'questionnaire_id_example' # str | questionnaire's id
academy_questionnaire_put_request = tiledb.cloud._common.api_v4.AcademyQuestionnairePutRequest() # AcademyQuestionnairePutRequest | academy lesson to create

    try:
        # Create or update academy questionnaire
        api_instance.put_academy_questionnaire(questionnaire_id, academy_questionnaire_put_request)
    except ApiException as e:
        print("Exception when calling AcademyApi->put_academy_questionnaire: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.AcademyApi(api_client)
    questionnaire_id = 'questionnaire_id_example' # str | questionnaire's id
academy_questionnaire_put_request = tiledb.cloud._common.api_v4.AcademyQuestionnairePutRequest() # AcademyQuestionnairePutRequest | academy lesson to create

    try:
        # Create or update academy questionnaire
        api_instance.put_academy_questionnaire(questionnaire_id, academy_questionnaire_put_request)
    except ApiException as e:
        print("Exception when calling AcademyApi->put_academy_questionnaire: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.AcademyApi(api_client)
    questionnaire_id = 'questionnaire_id_example' # str | questionnaire's id
academy_questionnaire_put_request = tiledb.cloud._common.api_v4.AcademyQuestionnairePutRequest() # AcademyQuestionnairePutRequest | academy lesson to create

    try:
        # Create or update academy questionnaire
        api_instance.put_academy_questionnaire(questionnaire_id, academy_questionnaire_put_request)
    except ApiException as e:
        print("Exception when calling AcademyApi->put_academy_questionnaire: %s\n" % e)
```

### Parameters

| Name                                  | Type                                                                    | Description              | Notes |
| ------------------------------------- | ----------------------------------------------------------------------- | ------------------------ | ----- |
| **questionnaire_id**                  | **str**                                                                 | questionnaire&#39;s id   |
| **academy_questionnaire_put_request** | [**AcademyQuestionnairePutRequest**](AcademyQuestionnairePutRequest.md) | academy lesson to create |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description              | Response headers |
| ----------- | ------------------------ | ---------------- |
| **200**     | create or update success | -                |
| **0**       | error response           | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
