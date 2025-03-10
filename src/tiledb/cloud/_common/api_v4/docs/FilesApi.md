# tiledb.cloud.\_common.api_v4.FilesApi

All URIs are relative to *https://api.tiledb.com/v4*

| Method                                     | HTTP request                          | Description                                      |
| ------------------------------------------ | ------------------------------------- | ------------------------------------------------ |
| [**file_get**](FilesApi.md#file_get)       | **GET** /files/{teamspace_id}/{path}  | Download the file at the given path              |
| [**file_head**](FilesApi.md#file_head)     | **HEAD** /files/{teamspace_id}/{path} | Get information about the file at the given path |
| [**folder_list**](FilesApi.md#folder_list) | **GET** /files/{teamspace_id}         | List folders and files contained in a folder     |

# **file_get**

> file_get(teamspace_id, path, range=range)

Download the file at the given path

End point to download the file at the given path

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
    api_instance = tiledb.cloud._common.api_v4.FilesApi(api_client)
    teamspace_id = 'teamspace_id_example' # str | The teamspace id in the form ts_9m4e2mr0ui3e8a215n4g
path = 'path_example' # str | The path to the file
range = 'range_example' # str | The range of bytes to fetch. Supports only single ranges. (optional)

    try:
        # Download the file at the given path
        api_instance.file_get(teamspace_id, path, range=range)
    except ApiException as e:
        print("Exception when calling FilesApi->file_get: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.FilesApi(api_client)
    teamspace_id = 'teamspace_id_example' # str | The teamspace id in the form ts_9m4e2mr0ui3e8a215n4g
path = 'path_example' # str | The path to the file
range = 'range_example' # str | The range of bytes to fetch. Supports only single ranges. (optional)

    try:
        # Download the file at the given path
        api_instance.file_get(teamspace_id, path, range=range)
    except ApiException as e:
        print("Exception when calling FilesApi->file_get: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.FilesApi(api_client)
    teamspace_id = 'teamspace_id_example' # str | The teamspace id in the form ts_9m4e2mr0ui3e8a215n4g
path = 'path_example' # str | The path to the file
range = 'range_example' # str | The range of bytes to fetch. Supports only single ranges. (optional)

    try:
        # Download the file at the given path
        api_instance.file_get(teamspace_id, path, range=range)
    except ApiException as e:
        print("Exception when calling FilesApi->file_get: %s\n" % e)
```

### Parameters

| Name             | Type    | Description                                               | Notes      |
| ---------------- | ------- | --------------------------------------------------------- | ---------- |
| **teamspace_id** | **str** | The teamspace id in the form ts_9m4e2mr0ui3e8a215n4g      |
| **path**         | **str** | The path to the file                                      |
| **range**        | **str** | The range of bytes to fetch. Supports only single ranges. | [optional] |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/xml

### HTTP response details

| Status code | Description                         | Response headers |
| ----------- | ----------------------------------- | ---------------- |
| **200**     | Successful file get response        | -                |
| **206**     | Successful file ranged get response | -                |
| **404**     | Teamspace or file does not exist    | -                |
| **416**     | Range not satisfiable               | -                |
| **502**     | Bad Gateway                         | -                |
| **0**       | error response                      | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **file_head**

> file_head(teamspace_id, path, range=range)

Get information about the file at the given path

End point to get information about the file at the given path

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
    api_instance = tiledb.cloud._common.api_v4.FilesApi(api_client)
    teamspace_id = 'teamspace_id_example' # str | The teamspace id in the form ts_9m4e2mr0ui3e8a215n4g
path = 'path_example' # str | The path to the file
range = 'range_example' # str | The range of bytes to fetch. Supports only single ranges. (optional)

    try:
        # Get information about the file at the given path
        api_instance.file_head(teamspace_id, path, range=range)
    except ApiException as e:
        print("Exception when calling FilesApi->file_head: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.FilesApi(api_client)
    teamspace_id = 'teamspace_id_example' # str | The teamspace id in the form ts_9m4e2mr0ui3e8a215n4g
path = 'path_example' # str | The path to the file
range = 'range_example' # str | The range of bytes to fetch. Supports only single ranges. (optional)

    try:
        # Get information about the file at the given path
        api_instance.file_head(teamspace_id, path, range=range)
    except ApiException as e:
        print("Exception when calling FilesApi->file_head: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.FilesApi(api_client)
    teamspace_id = 'teamspace_id_example' # str | The teamspace id in the form ts_9m4e2mr0ui3e8a215n4g
path = 'path_example' # str | The path to the file
range = 'range_example' # str | The range of bytes to fetch. Supports only single ranges. (optional)

    try:
        # Get information about the file at the given path
        api_instance.file_head(teamspace_id, path, range=range)
    except ApiException as e:
        print("Exception when calling FilesApi->file_head: %s\n" % e)
```

### Parameters

| Name             | Type    | Description                                               | Notes      |
| ---------------- | ------- | --------------------------------------------------------- | ---------- |
| **teamspace_id** | **str** | The teamspace id in the form ts_9m4e2mr0ui3e8a215n4g      |
| **path**         | **str** | The path to the file                                      |
| **range**        | **str** | The range of bytes to fetch. Supports only single ranges. | [optional] |

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined

### HTTP response details

| Status code | Description                         | Response headers |
| ----------- | ----------------------------------- | ---------------- |
| **200**     | Successful file get response        | -                |
| **206**     | Successful file ranged get response | -                |
| **404**     | Teamspace or file does not exist    | -                |
| **416**     | Range not satisfiable               | -                |
| **502**     | Bad Gateway                         | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **folder_list**

> FileListResponse folder_list(teamspace_id, list_type, delimiter, prefix=prefix, max_keys=max_keys, continuation_token=continuation_token)

List folders and files contained in a folder

End point to list files and folders for the passed teamspace

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
    api_instance = tiledb.cloud._common.api_v4.FilesApi(api_client)
    teamspace_id = 'teamspace_id_example' # str | The teamspace id in the form ts_9m4e2mr0ui3e8a215n4g
list_type = 56 # int | Required for S3 API compatibility, must be set to 2.
delimiter = 'delimiter_example' # str | The string that delimits the path segments. Only forward slash is supported
prefix = 'prefix_example' # str | The directory of files to list. (optional)
max_keys = 56 # int | The maximum number of items to return. (optional)
continuation_token = 'continuation_token_example' # str | Used to resume an incomplete list operation (optional)

    try:
        # List folders and files contained in a folder
        api_response = api_instance.folder_list(teamspace_id, list_type, delimiter, prefix=prefix, max_keys=max_keys, continuation_token=continuation_token)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->folder_list: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.FilesApi(api_client)
    teamspace_id = 'teamspace_id_example' # str | The teamspace id in the form ts_9m4e2mr0ui3e8a215n4g
list_type = 56 # int | Required for S3 API compatibility, must be set to 2.
delimiter = 'delimiter_example' # str | The string that delimits the path segments. Only forward slash is supported
prefix = 'prefix_example' # str | The directory of files to list. (optional)
max_keys = 56 # int | The maximum number of items to return. (optional)
continuation_token = 'continuation_token_example' # str | Used to resume an incomplete list operation (optional)

    try:
        # List folders and files contained in a folder
        api_response = api_instance.folder_list(teamspace_id, list_type, delimiter, prefix=prefix, max_keys=max_keys, continuation_token=continuation_token)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->folder_list: %s\n" % e)
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
    api_instance = tiledb.cloud._common.api_v4.FilesApi(api_client)
    teamspace_id = 'teamspace_id_example' # str | The teamspace id in the form ts_9m4e2mr0ui3e8a215n4g
list_type = 56 # int | Required for S3 API compatibility, must be set to 2.
delimiter = 'delimiter_example' # str | The string that delimits the path segments. Only forward slash is supported
prefix = 'prefix_example' # str | The directory of files to list. (optional)
max_keys = 56 # int | The maximum number of items to return. (optional)
continuation_token = 'continuation_token_example' # str | Used to resume an incomplete list operation (optional)

    try:
        # List folders and files contained in a folder
        api_response = api_instance.folder_list(teamspace_id, list_type, delimiter, prefix=prefix, max_keys=max_keys, continuation_token=continuation_token)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->folder_list: %s\n" % e)
```

### Parameters

| Name                   | Type    | Description                                                                 | Notes      |
| ---------------------- | ------- | --------------------------------------------------------------------------- | ---------- |
| **teamspace_id**       | **str** | The teamspace id in the form ts_9m4e2mr0ui3e8a215n4g                        |
| **list_type**          | **int** | Required for S3 API compatibility, must be set to 2.                        |
| **delimiter**          | **str** | The string that delimits the path segments. Only forward slash is supported |
| **prefix**             | **str** | The directory of files to list.                                             | [optional] |
| **max_keys**           | **int** | The maximum number of items to return.                                      | [optional] |
| **continuation_token** | **str** | Used to resume an incomplete list operation                                 | [optional] |

### Return type

[**FileListResponse**](FileListResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth), [OAuth2](../README.md#OAuth2)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/xml

### HTTP response details

| Status code | Description                     | Response headers |
| ----------- | ------------------------------- | ---------------- |
| **200**     | Successful folder list response | -                |
| **404**     | Teamspace does not exist        | -                |
| **502**     | Bad Gateway                     | -                |
| **0**       | error response                  | -                |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
