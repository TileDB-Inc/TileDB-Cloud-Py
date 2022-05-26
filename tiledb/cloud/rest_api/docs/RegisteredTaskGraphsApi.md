# tiledb.cloud.rest_api.RegisteredTaskGraphsApi

All URIs are relative to *http://localhost/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_registered_task_graph**](RegisteredTaskGraphsApi.md#delete_registered_task_graph) | **DELETE** /taskgraphs/{namespace}/registered/{name} | 
[**get_registered_task_graph**](RegisteredTaskGraphsApi.md#get_registered_task_graph) | **GET** /taskgraphs/{namespace}/registered/{name} | 
[**get_registered_task_graph_sharing_policies**](RegisteredTaskGraphsApi.md#get_registered_task_graph_sharing_policies) | **GET** /taskgraphs/{namespace}/registered/{name}/share | 
[**register_registered_task_graph**](RegisteredTaskGraphsApi.md#register_registered_task_graph) | **POST** /taskgraphs/{namespace}/registered/{name} | 
[**share_registered_task_graph**](RegisteredTaskGraphsApi.md#share_registered_task_graph) | **PATCH** /taskgraphs/{namespace}/registered/{name}/share | 
[**update_registered_task_graph**](RegisteredTaskGraphsApi.md#update_registered_task_graph) | **PATCH** /taskgraphs/{namespace}/registered/{name} | 


# **delete_registered_task_graph**
> delete_registered_task_graph(namespace, name)



Delete the given registered task graph. 

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import registered_task_graphs_api
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
    api_instance = registered_task_graphs_api.RegisteredTaskGraphsApi(api_client)
    namespace = "namespace_example" # str | The namespace that owns this registered UDF.
    name = "name_example" # str | The name of the registered task graph.

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_registered_task_graph(namespace, name)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling RegisteredTaskGraphsApi->delete_registered_task_graph: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| The namespace that owns this registered UDF. |
 **name** | **str**| The name of the registered task graph. |

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
**204** | Task graph successfully deleted. |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_registered_task_graph**
> RegisteredTaskGraph get_registered_task_graph(namespace, name)



Fetch the contents of this registered task graph. 

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import registered_task_graphs_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.registered_task_graph import RegisteredTaskGraph
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
    api_instance = registered_task_graphs_api.RegisteredTaskGraphsApi(api_client)
    namespace = "namespace_example" # str | The namespace that owns this registered UDF.
    name = "name_example" # str | The name of the registered task graph.

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_registered_task_graph(namespace, name)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling RegisteredTaskGraphsApi->get_registered_task_graph: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| The namespace that owns this registered UDF. |
 **name** | **str**| The name of the registered task graph. |

### Return type

[**RegisteredTaskGraph**](RegisteredTaskGraph.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The contents of the registered task graph. |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_registered_task_graph_sharing_policies**
> [TaskGraphSharing] get_registered_task_graph_sharing_policies(namespace, name)



Get sharing policies for the task graph.

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import registered_task_graphs_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.task_graph_sharing import TaskGraphSharing
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
    api_instance = registered_task_graphs_api.RegisteredTaskGraphsApi(api_client)
    namespace = "namespace_example" # str | The namespace that owns the registered task graph.
    name = "name_example" # str | The name of the task graph.

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_registered_task_graph_sharing_policies(namespace, name)
        pprint(api_response)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling RegisteredTaskGraphsApi->get_registered_task_graph_sharing_policies: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| The namespace that owns the registered task graph. |
 **name** | **str**| The name of the task graph. |

### Return type

[**[TaskGraphSharing]**](TaskGraphSharing.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BasicAuth](../README.md#BasicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of all specific sharing policies |  -  |
**404** | The task graph does not exist (or the user does not have permission to view policies)  |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **register_registered_task_graph**
> register_registered_task_graph(namespace, name)



Register a task graph in the given namespace, with the given name. 

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import registered_task_graphs_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.registered_task_graph import RegisteredTaskGraph
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
    api_instance = registered_task_graphs_api.RegisteredTaskGraphsApi(api_client)
    namespace = "namespace_example" # str | The namespace that owns this registered UDF.
    name = "name_example" # str | The name of the registered task graph.
    graph = RegisteredTaskGraph(
        uuid="uuid_example",
        namespace="namespace_example",
        name="name_example",
        readme="readme_example",
        license_id="license_id_example",
        license_text="license_text_example",
        tags=[
            "tags_example",
        ],
        nodes=[
            RegisteredTaskGraphNode(
                client_node_id="client_node_id_example",
                name="name_example",
                depends_on=[
                    "depends_on_example",
                ],
                array_node=UDFArrayDetails(
                    parameter_id="parameter_id_example",
                    uri="uri_example",
                    ranges=QueryRanges(
                        layout=Layout("row-major"),
                        ranges=[
                            [
                                3.14,
                            ],
                        ],
                    ),
                    buffers=[
                        "buffers_example",
                    ],
                ),
                input_node=TGInputNodeData(
                    default_value={},
                    datatype="datatype_example",
                ),
                sql_node=TGSQLNodeData(
                    init_commands=[
                        "init_commands_example",
                    ],
                    query="query_example",
                    parameters=[
                        {},
                    ],
                    result_format=ResultFormat("python_pickle"),
                ),
                udf_node=TGUDFNodeData(
                    registered_udf_name="registered_udf_name_example",
                    executable_code="executable_code_example",
                    source_text="source_text_example",
                    environment=TGUDFEnvironment(
                        language=UDFLanguage("python"),
                        language_version="language_version_example",
                        image_name="image_name_example",
                        resource_class="resource_class_example",
                    ),
                    arguments=[
                        TGUDFArgument(
                            name="name_example",
                            value={},
                        ),
                    ],
                    result_format=ResultFormat("python_pickle"),
                ),
            ),
        ],
    ) # RegisteredTaskGraph | Task graph to register. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_instance.register_registered_task_graph(namespace, name)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling RegisteredTaskGraphsApi->register_registered_task_graph: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_instance.register_registered_task_graph(namespace, name, graph=graph)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling RegisteredTaskGraphsApi->register_registered_task_graph: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| The namespace that owns this registered UDF. |
 **name** | **str**| The name of the registered task graph. |
 **graph** | [**RegisteredTaskGraph**](RegisteredTaskGraph.md)| Task graph to register. | [optional]

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
**204** | Task graph registered successfully. |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **share_registered_task_graph**
> share_registered_task_graph(namespace, name, task_graph_sharing)



Share a task graph.

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import registered_task_graphs_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.task_graph_sharing import TaskGraphSharing
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
    api_instance = registered_task_graphs_api.RegisteredTaskGraphsApi(api_client)
    namespace = "namespace_example" # str | The namespace that owns the registered task graph.
    name = "name_example" # str | The name of the task graph.
    task_graph_sharing = TaskGraphSharing(
        actions=[
            TaskGraphActions("[fetch_task_graph, share_task_graph]"),
        ],
        namespace="MyOrganization",
        namespace_type="organization",
    ) # TaskGraphSharing | Namespace and list of permissions to share with. An empty list of permissions will remove the namespace; if permissions already exist they will be deleted then new ones added. In the event of a failure, the new policies will be rolled back to prevent partial policies, and it's likely the UDF will not be shared with the namespace at all. 

    # example passing only required values which don't have defaults set
    try:
        api_instance.share_registered_task_graph(namespace, name, task_graph_sharing)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling RegisteredTaskGraphsApi->share_registered_task_graph: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| The namespace that owns the registered task graph. |
 **name** | **str**| The name of the task graph. |
 **task_graph_sharing** | [**TaskGraphSharing**](TaskGraphSharing.md)| Namespace and list of permissions to share with. An empty list of permissions will remove the namespace; if permissions already exist they will be deleted then new ones added. In the event of a failure, the new policies will be rolled back to prevent partial policies, and it&#39;s likely the UDF will not be shared with the namespace at all.  |

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
**204** | UDF shared successfully |  -  |
**404** | UDF does not exist or user does not have permissions to share UDF |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_registered_task_graph**
> update_registered_task_graph(namespace, name)



Update the contents of an existing registered task graph. 

### Example

* Api Key Authentication (ApiKeyAuth):
* Basic Authentication (BasicAuth):

```python
import time
import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api import registered_task_graphs_api
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.registered_task_graph import RegisteredTaskGraph
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
    api_instance = registered_task_graphs_api.RegisteredTaskGraphsApi(api_client)
    namespace = "namespace_example" # str | The namespace that owns this registered UDF.
    name = "name_example" # str | The name of the registered task graph.
    graph = RegisteredTaskGraph(
        uuid="uuid_example",
        namespace="namespace_example",
        name="name_example",
        readme="readme_example",
        license_id="license_id_example",
        license_text="license_text_example",
        tags=[
            "tags_example",
        ],
        nodes=[
            RegisteredTaskGraphNode(
                client_node_id="client_node_id_example",
                name="name_example",
                depends_on=[
                    "depends_on_example",
                ],
                array_node=UDFArrayDetails(
                    parameter_id="parameter_id_example",
                    uri="uri_example",
                    ranges=QueryRanges(
                        layout=Layout("row-major"),
                        ranges=[
                            [
                                3.14,
                            ],
                        ],
                    ),
                    buffers=[
                        "buffers_example",
                    ],
                ),
                input_node=TGInputNodeData(
                    default_value={},
                    datatype="datatype_example",
                ),
                sql_node=TGSQLNodeData(
                    init_commands=[
                        "init_commands_example",
                    ],
                    query="query_example",
                    parameters=[
                        {},
                    ],
                    result_format=ResultFormat("python_pickle"),
                ),
                udf_node=TGUDFNodeData(
                    registered_udf_name="registered_udf_name_example",
                    executable_code="executable_code_example",
                    source_text="source_text_example",
                    environment=TGUDFEnvironment(
                        language=UDFLanguage("python"),
                        language_version="language_version_example",
                        image_name="image_name_example",
                        resource_class="resource_class_example",
                    ),
                    arguments=[
                        TGUDFArgument(
                            name="name_example",
                            value={},
                        ),
                    ],
                    result_format=ResultFormat("python_pickle"),
                ),
            ),
        ],
    ) # RegisteredTaskGraph | The new contents of the task graph. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_instance.update_registered_task_graph(namespace, name)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling RegisteredTaskGraphsApi->update_registered_task_graph: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_instance.update_registered_task_graph(namespace, name, graph=graph)
    except tiledb.cloud.rest_api.ApiException as e:
        print("Exception when calling RegisteredTaskGraphsApi->update_registered_task_graph: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **str**| The namespace that owns this registered UDF. |
 **name** | **str**| The name of the registered task graph. |
 **graph** | [**RegisteredTaskGraph**](RegisteredTaskGraph.md)| The new contents of the task graph. | [optional]

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
**204** | Task graph updated successfully. |  -  |
**0** | error response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

