# tiledb.cloud.\_common.api_v2.ArrayApi

All URIs are relative to _http://localhost_

| Method                                                   | HTTP request                                    | Description |
| -------------------------------------------------------- | ----------------------------------------------- | ----------- |
| [**array_activity_log**](ArrayApi.md#array_activity_log) | **GET** /v2/arrays/{namespace}/{array}/activity |
| [**get_array**](ArrayApi.md#get_array)                   | **POST** /v2/arrays/{namespace}/{array}         |

# **array_activity_log**

> ArrayActivityLogData array_activity_log(namespace, array, start=start, end=end, event_types=event_types, task_id=task_id, has_task_id=has_task_id, page=page, per_page=per_page)

get array activity logs

### Example

- Api Key Authentication (ApiKeyAuth):

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
    api_instance = tiledb.cloud._common.api_v2.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
start = 56 # int | Start time of window of fetch logs, unix epoch in seconds (default: seven days ago) (optional)
end = 56 # int | End time of window of fetch logs, unix epoch in seconds (default: current utc timestamp) (optional)
event_types = ['event_types_example'] # list[str] | Refer to ActivityEventType for possible values (optional)
task_id = 'task_id_example' # str | Array task id To filter activity to (optional)
has_task_id = True # bool | Excludes activity log results that does not contain an array task uuid (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        api_response = api_instance.array_activity_log(namespace, array, start=start, end=end, event_types=event_types, task_id=task_id, has_task_id=has_task_id, page=page, per_page=per_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->array_activity_log: %s\n" % e)
```

- Basic Authentication (BasicAuth):

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
    api_instance = tiledb.cloud._common.api_v2.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
start = 56 # int | Start time of window of fetch logs, unix epoch in seconds (default: seven days ago) (optional)
end = 56 # int | End time of window of fetch logs, unix epoch in seconds (default: current utc timestamp) (optional)
event_types = ['event_types_example'] # list[str] | Refer to ActivityEventType for possible values (optional)
task_id = 'task_id_example' # str | Array task id To filter activity to (optional)
has_task_id = True # bool | Excludes activity log results that does not contain an array task uuid (optional)
page = 56 # int | pagination offset (optional)
per_page = 56 # int | pagination limit (optional)

    try:
        api_response = api_instance.array_activity_log(namespace, array, start=start, end=end, event_types=event_types, task_id=task_id, has_task_id=has_task_id, page=page, per_page=per_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->array_activity_log: %s\n" % e)
```

### Parameters

| Name            | Type                    | Description                                                                              | Notes      |
| --------------- | ----------------------- | ---------------------------------------------------------------------------------------- | ---------- |
| **namespace**   | **str**                 | namespace array is in (an organization name or user&#39;s username)                      |
| **array**       | **str**                 | name/uri of array that is url-encoded                                                    |
| **start**       | **int**                 | Start time of window of fetch logs, unix epoch in seconds (default: seven days ago)      | [optional] |
| **end**         | **int**                 | End time of window of fetch logs, unix epoch in seconds (default: current utc timestamp) | [optional] |
| **event_types** | [**list[str]**](str.md) | Refer to ActivityEventType for possible values                                           | [optional] |
| **task_id**     | **str**                 | Array task id To filter activity to                                                      | [optional] |
| **has_task_id** | **bool**                | Excludes activity log results that does not contain an array task uuid                   | [optional] |
| **page**        | **int**                 | pagination offset                                                                        | [optional] |
| **per_page**    | **int**                 | pagination limit                                                                         | [optional] |

### Return type

[**ArrayActivityLogData**](ArrayActivityLogData.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description           | Response headers |
| ----------- | --------------------- | ---------------- |
| **200**     | log of array activity | -                |
| **502**     | Bad Gateway           | -                |
| **0**       | error response        | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_array**

> Array get_array(namespace, array, content_type, array_fetch)

Get a array at a specified URI registered to a group/project

### Example

- Api Key Authentication (ApiKeyAuth):

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
    api_instance = tiledb.cloud._common.api_v2.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
content_type = 'application/json' # str | Content Type of input and return mime (default to 'application/json')
array_fetch = tiledb.cloud._common.api_v2.ArrayFetch() # ArrayFetch | Details for array being fetched

    try:
        api_response = api_instance.get_array(namespace, array, content_type, array_fetch)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->get_array: %s\n" % e)
```

- Basic Authentication (BasicAuth):

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
    api_instance = tiledb.cloud._common.api_v2.ArrayApi(api_client)
    namespace = 'namespace_example' # str | namespace array is in (an organization name or user's username)
array = 'array_example' # str | name/uri of array that is url-encoded
content_type = 'application/json' # str | Content Type of input and return mime (default to 'application/json')
array_fetch = tiledb.cloud._common.api_v2.ArrayFetch() # ArrayFetch | Details for array being fetched

    try:
        api_response = api_instance.get_array(namespace, array, content_type, array_fetch)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ArrayApi->get_array: %s\n" % e)
```

### Parameters

| Name             | Type                            | Description                                                         | Notes                                   |
| ---------------- | ------------------------------- | ------------------------------------------------------------------- | --------------------------------------- |
| **namespace**    | **str**                         | namespace array is in (an organization name or user&#39;s username) |
| **array**        | **str**                         | name/uri of array that is url-encoded                               |
| **content_type** | **str**                         | Content Type of input and return mime                               | [default to &#39;application/json&#39;] |
| **array_fetch**  | [**ArrayFetch**](ArrayFetch.md) | Details for array being fetched                                     |

### Return type

[**Array**](Array.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description               | Response headers |
| ----------- | ------------------------- | ---------------- |
| **200**     | Array opened successfully | -                |
| **502**     | Bad Gateway               | -                |
| **0**       | error response            | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
