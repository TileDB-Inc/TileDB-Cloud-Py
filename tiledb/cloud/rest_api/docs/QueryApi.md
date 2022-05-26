# tiledb.cloud.rest_api.QueryApi

All URIs are relative to *http://localhost/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**finalize_query**](QueryApi.md#finalize_query) | **POST** /arrays/{namespace}/{array}/query/finalize | 
[**get_est_result_sizes**](QueryApi.md#get_est_result_sizes) | **POST** /arrays/{namespace}/{array}/query/est_result_sizes | 
[**get_file**](QueryApi.md#get_file) | **GET** /arrays/{namespace}/{array}/query/get_file | 
[**submit_query**](QueryApi.md#submit_query) | **POST** /arrays/{namespace}/{array}/query/submit | 
[**submit_query_json**](QueryApi.md#submit_query_json) | **POST** /arrays/{namespace}/{array}/query/submit_query_json | 


# **finalize_query**
> Query finalize_query(namespace, array, type, query)



send a query to run against a specified array/URI registered to a group/project

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import query_api
from tiledb.cloud.rest_api.model.query import Query
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
    api_instance = query_api.QueryApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded
    type = "type_example" # str | type of query
    query = Query(
        type=Querytype("READ"),
        layout=Layout("row-major"),
        status=Querystatus("FAILED"),
        attribute_buffer_headers=[
            AttributeBufferHeader(
                name="attribute1",
                fixed_len_buffer_size_in_bytes=1,
                var_len_buffer_size_in_bytes=1,
            ),
        ],
        writer=Writer(
            check_coord_dups=True,
            check_coord_oob=True,
            dedup_coords=True,
            subarray=DomainArray(
                int8=[
                    1,
                ],
                uint8=[
                    1,
                ],
                int16=[
                    1,
                ],
                uint16=[
                    1,
                ],
                int32=[
                    1,
                ],
                uint32=[
                    1,
                ],
                int64=[
                    1,
                ],
                uint64=[
                    1,
                ],
                float32=[
                    3.14,
                ],
                float64=[
                    3.14,
                ],
            ),
        ),
        reader=QueryReader(
            layout=Layout("row-major"),
            subarray=Subarray(
                layout=Layout("row-major"),
                ranges=[
                    SubarrayRanges(
                        type=Datatype("INT32"),
                        has_default_range=True,
                        buffer=[
                            1,
                        ],
                    ),
                ],
            ),
            read_state=ReadState(
                initialized=True,
                overflowed=True,
                unsplittable=True,
                subarray_partitioner=SubarrayPartitioner(
                    subarray=Subarray(
                        layout=Layout("row-major"),
                        ranges=[
                            SubarrayRanges(
                                type=Datatype("INT32"),
                                has_default_range=True,
                                buffer=[
                                    1,
                                ],
                            ),
                        ],
                    ),
                    budget=[
                        AttributeBufferSize(
                            attribute="attribute_example",
                            offset_bytes=1,
                            data_bytes=1,
                        ),
                    ],
                    current=SubarrayPartitionerCurrent(
                        subarray=Subarray(
                            layout=Layout("row-major"),
                            ranges=[
                                SubarrayRanges(
                                    type=Datatype("INT32"),
                                    has_default_range=True,
                                    buffer=[
                                        1,
                                    ],
                                ),
                            ],
                        ),
                        start=1,
                        end=1,
                        split_multi_range=True,
                    ),
                    state=SubarrayPartitionerState(
                        start=1,
                        end=1,
                        single_range=[
                            Subarray(
                                layout=Layout("row-major"),
                                ranges=[
                                    SubarrayRanges(
                                        type=Datatype("INT32"),
                                        has_default_range=True,
                                        buffer=[
                                            1,
                                        ],
                                    ),
                                ],
                            ),
                        ],
                        multi_range=[
                            Subarray(
                                layout=Layout("row-major"),
                                ranges=[
                                    SubarrayRanges(
                                        type=Datatype("INT32"),
                                        has_default_range=True,
                                        buffer=[
                                            1,
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    memory_budget=1,
                    memory_budget_var=1,
                ),
            ),
            var_offsets_mode="var_offsets_mode_example",
            var_offsets_add_extra_element=True,
            var_offsets_bitsize=1,
        ),
        array=Array(
            timestamp=1540471791873,
            query_type=Querytype("READ"),
            uri="uri_example",
        ),
        total_fixed_length_buffer_bytes=1,
        total_var_len_buffer_bytes=1,
    ) # Query | query to run
    x_payer = "X-Payer_example" # str | Name of organization or user who should be charged for this request (optional)
    open_at = 1 # int | open_at for array in unix epoch (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.finalize_query(namespace, array, type, query)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling QueryApi->finalize_query: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.finalize_query(namespace, array, type, query, x_payer=x_payer, open_at=open_at)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling QueryApi->finalize_query: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |
 **type** | **str**| type of query |
 **query** | [**Query**](Query.md)| query to run |
 **content_type** | **str**| Content Type of input and return mime | defaults to "application/json"
 **x_payer** | **str**| Name of organization or user who should be charged for this request | [optional]
 **open_at** | **int**| open_at for array in unix epoch | [optional]

### Return type

[**Query**](Query.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/capnp
 - **Accept**: application/json, application/capnp


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | query completed and results are returned in query object |  * X-TILEDB-CLOUD-TASK-ID - Task ID for just completed request <br>  |
**204** | query completed successfully with no return |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_est_result_sizes**
> Query get_est_result_sizes(namespace, array, type, query)



send a query to run against a specified array/URI registered to a group/project

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import query_api
from tiledb.cloud.rest_api.model.query import Query
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
    api_instance = query_api.QueryApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded
    type = "type_example" # str | type of query
    query = Query(
        type=Querytype("READ"),
        layout=Layout("row-major"),
        status=Querystatus("FAILED"),
        attribute_buffer_headers=[
            AttributeBufferHeader(
                name="attribute1",
                fixed_len_buffer_size_in_bytes=1,
                var_len_buffer_size_in_bytes=1,
            ),
        ],
        writer=Writer(
            check_coord_dups=True,
            check_coord_oob=True,
            dedup_coords=True,
            subarray=DomainArray(
                int8=[
                    1,
                ],
                uint8=[
                    1,
                ],
                int16=[
                    1,
                ],
                uint16=[
                    1,
                ],
                int32=[
                    1,
                ],
                uint32=[
                    1,
                ],
                int64=[
                    1,
                ],
                uint64=[
                    1,
                ],
                float32=[
                    3.14,
                ],
                float64=[
                    3.14,
                ],
            ),
        ),
        reader=QueryReader(
            layout=Layout("row-major"),
            subarray=Subarray(
                layout=Layout("row-major"),
                ranges=[
                    SubarrayRanges(
                        type=Datatype("INT32"),
                        has_default_range=True,
                        buffer=[
                            1,
                        ],
                    ),
                ],
            ),
            read_state=ReadState(
                initialized=True,
                overflowed=True,
                unsplittable=True,
                subarray_partitioner=SubarrayPartitioner(
                    subarray=Subarray(
                        layout=Layout("row-major"),
                        ranges=[
                            SubarrayRanges(
                                type=Datatype("INT32"),
                                has_default_range=True,
                                buffer=[
                                    1,
                                ],
                            ),
                        ],
                    ),
                    budget=[
                        AttributeBufferSize(
                            attribute="attribute_example",
                            offset_bytes=1,
                            data_bytes=1,
                        ),
                    ],
                    current=SubarrayPartitionerCurrent(
                        subarray=Subarray(
                            layout=Layout("row-major"),
                            ranges=[
                                SubarrayRanges(
                                    type=Datatype("INT32"),
                                    has_default_range=True,
                                    buffer=[
                                        1,
                                    ],
                                ),
                            ],
                        ),
                        start=1,
                        end=1,
                        split_multi_range=True,
                    ),
                    state=SubarrayPartitionerState(
                        start=1,
                        end=1,
                        single_range=[
                            Subarray(
                                layout=Layout("row-major"),
                                ranges=[
                                    SubarrayRanges(
                                        type=Datatype("INT32"),
                                        has_default_range=True,
                                        buffer=[
                                            1,
                                        ],
                                    ),
                                ],
                            ),
                        ],
                        multi_range=[
                            Subarray(
                                layout=Layout("row-major"),
                                ranges=[
                                    SubarrayRanges(
                                        type=Datatype("INT32"),
                                        has_default_range=True,
                                        buffer=[
                                            1,
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    memory_budget=1,
                    memory_budget_var=1,
                ),
            ),
            var_offsets_mode="var_offsets_mode_example",
            var_offsets_add_extra_element=True,
            var_offsets_bitsize=1,
        ),
        array=Array(
            timestamp=1540471791873,
            query_type=Querytype("READ"),
            uri="uri_example",
        ),
        total_fixed_length_buffer_bytes=1,
        total_var_len_buffer_bytes=1,
    ) # Query | query to run
    x_payer = "X-Payer_example" # str | Name of organization or user who should be charged for this request (optional)
    open_at = 1 # int | open_at for array in unix epoch (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_est_result_sizes(namespace, array, type, query)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling QueryApi->get_est_result_sizes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_est_result_sizes(namespace, array, type, query, x_payer=x_payer, open_at=open_at)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling QueryApi->get_est_result_sizes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |
 **type** | **str**| type of query |
 **query** | [**Query**](Query.md)| query to run |
 **content_type** | **str**| Content Type of input and return mime | defaults to "application/json"
 **x_payer** | **str**| Name of organization or user who should be charged for this request | [optional]
 **open_at** | **int**| open_at for array in unix epoch | [optional]

### Return type

[**Query**](Query.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/capnp
 - **Accept**: application/json, application/capnp


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | query est result size computed and results are returned in query object |  * X-TILEDB-CLOUD-TASK-ID - Task ID for just completed request <br>  |
**204** | query completed successfully with no return |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_file**
> file_type get_file(namespace, array, )



send a query to run against a specified array/URI registered to a group/project, returns file bytes

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import query_api
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
    api_instance = query_api.QueryApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded
    x_payer = "X-Payer_example" # str | Name of organization or user who should be charged for this request (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_file(namespace, array, )
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling QueryApi->get_file: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_file(namespace, array, x_payer=x_payer)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling QueryApi->get_file: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |
 **content_type** | **str**| Content Type of input and return mime | defaults to "application/json"
 **x_payer** | **str**| Name of organization or user who should be charged for this request | [optional]

### Return type

**file_type**

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/x-ipynb+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | query completed and result bytes are returned |  * X-TILEDB-CLOUD-TASK-ID - Task ID for just completed request <br>  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **submit_query**
> Query submit_query(namespace, array, type, query)



send a query to run against a specified array/URI registered to a group/project

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import query_api
from tiledb.cloud.rest_api.model.query import Query
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
    api_instance = query_api.QueryApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded
    type = "type_example" # str | type of query
    query = Query(
        type=Querytype("READ"),
        layout=Layout("row-major"),
        status=Querystatus("FAILED"),
        attribute_buffer_headers=[
            AttributeBufferHeader(
                name="attribute1",
                fixed_len_buffer_size_in_bytes=1,
                var_len_buffer_size_in_bytes=1,
            ),
        ],
        writer=Writer(
            check_coord_dups=True,
            check_coord_oob=True,
            dedup_coords=True,
            subarray=DomainArray(
                int8=[
                    1,
                ],
                uint8=[
                    1,
                ],
                int16=[
                    1,
                ],
                uint16=[
                    1,
                ],
                int32=[
                    1,
                ],
                uint32=[
                    1,
                ],
                int64=[
                    1,
                ],
                uint64=[
                    1,
                ],
                float32=[
                    3.14,
                ],
                float64=[
                    3.14,
                ],
            ),
        ),
        reader=QueryReader(
            layout=Layout("row-major"),
            subarray=Subarray(
                layout=Layout("row-major"),
                ranges=[
                    SubarrayRanges(
                        type=Datatype("INT32"),
                        has_default_range=True,
                        buffer=[
                            1,
                        ],
                    ),
                ],
            ),
            read_state=ReadState(
                initialized=True,
                overflowed=True,
                unsplittable=True,
                subarray_partitioner=SubarrayPartitioner(
                    subarray=Subarray(
                        layout=Layout("row-major"),
                        ranges=[
                            SubarrayRanges(
                                type=Datatype("INT32"),
                                has_default_range=True,
                                buffer=[
                                    1,
                                ],
                            ),
                        ],
                    ),
                    budget=[
                        AttributeBufferSize(
                            attribute="attribute_example",
                            offset_bytes=1,
                            data_bytes=1,
                        ),
                    ],
                    current=SubarrayPartitionerCurrent(
                        subarray=Subarray(
                            layout=Layout("row-major"),
                            ranges=[
                                SubarrayRanges(
                                    type=Datatype("INT32"),
                                    has_default_range=True,
                                    buffer=[
                                        1,
                                    ],
                                ),
                            ],
                        ),
                        start=1,
                        end=1,
                        split_multi_range=True,
                    ),
                    state=SubarrayPartitionerState(
                        start=1,
                        end=1,
                        single_range=[
                            Subarray(
                                layout=Layout("row-major"),
                                ranges=[
                                    SubarrayRanges(
                                        type=Datatype("INT32"),
                                        has_default_range=True,
                                        buffer=[
                                            1,
                                        ],
                                    ),
                                ],
                            ),
                        ],
                        multi_range=[
                            Subarray(
                                layout=Layout("row-major"),
                                ranges=[
                                    SubarrayRanges(
                                        type=Datatype("INT32"),
                                        has_default_range=True,
                                        buffer=[
                                            1,
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    memory_budget=1,
                    memory_budget_var=1,
                ),
            ),
            var_offsets_mode="var_offsets_mode_example",
            var_offsets_add_extra_element=True,
            var_offsets_bitsize=1,
        ),
        array=Array(
            timestamp=1540471791873,
            query_type=Querytype("READ"),
            uri="uri_example",
        ),
        total_fixed_length_buffer_bytes=1,
        total_var_len_buffer_bytes=1,
    ) # Query | query to run
    x_payer = "X-Payer_example" # str | Name of organization or user who should be charged for this request (optional)
    open_at = 1 # int | open_at for array in unix epoch (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.submit_query(namespace, array, type, query)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling QueryApi->submit_query: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.submit_query(namespace, array, type, query, x_payer=x_payer, open_at=open_at)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling QueryApi->submit_query: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |
 **type** | **str**| type of query |
 **query** | [**Query**](Query.md)| query to run |
 **content_type** | **str**| Content Type of input and return mime | defaults to "application/json"
 **x_payer** | **str**| Name of organization or user who should be charged for this request | [optional]
 **open_at** | **int**| open_at for array in unix epoch | [optional]

### Return type

[**Query**](Query.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/capnp
 - **Accept**: application/json, application/capnp


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | query completed and results are returned in query object |  * X-TILEDB-CLOUD-TASK-ID - Task ID for just completed request <br>  |
**204** | query completed successfully with no return |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **submit_query_json**
> bool, date, datetime, dict, float, int, list, str, none_type submit_query_json(namespace, array, query_json)



send a query to run against a specified array/URI registered to a group/project, returns JSON results

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import query_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.query_json import QueryJson
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
    api_instance = query_api.QueryApi(api_client)
    namespace = "namespace_example" # str | namespace array is in (an organization name or user's username)
    array = "array_example" # str | name/uri of array that is url-encoded
    query_json = QueryJson(
        query_ranges=QueryRanges(
            layout=Layout("row-major"),
            ranges=[
                [
                    3.14,
                ],
            ],
        ),
        fields=[
            "fields_example",
        ],
    ) # QueryJson | query to run
    x_payer = "X-Payer_example" # str | Name of organization or user who should be charged for this request (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.submit_query_json(namespace, array, query_json)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling QueryApi->submit_query_json: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.submit_query_json(namespace, array, query_json, x_payer=x_payer)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling QueryApi->submit_query_json: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| namespace array is in (an organization name or user&#39;s username) |
 **array** | **str**| name/uri of array that is url-encoded |
 **query_json** | [**QueryJson**](QueryJson.md)| query to run |
 **content_type** | **str**| Content Type of input and return mime | defaults to "application/json"
 **x_payer** | **str**| Name of organization or user who should be charged for this request | [optional]

### Return type

**bool, date, datetime, dict, float, int, list, str, none_type**

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | query completed and results are returned in JSON format |  * X-TILEDB-CLOUD-TASK-ID - Task ID for just completed request <br>  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

