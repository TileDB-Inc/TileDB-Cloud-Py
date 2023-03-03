# SQLParameters

Parameters for running sql query
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | name of task, optional | [optional] 
**query** | **str** | query to run | [optional] 
**output_uri** | **str** | Output array uri | [optional] 
**store_results** | **bool** | store results for later retrieval | [optional] 
**dont_download_results** | **bool** | Set to true to avoid downloading the results of this UDF. Useful for intermediate nodes in a task graph where you will not be using the results of your function. Defaults to false (\&quot;yes download results\&quot;). | [optional] 
**resource_class** | **str** | The resource class to use for the SQL execution. Resource classes define resource limits for memory and CPUs. If this is empty, then the SQL will execute in the standard resource class of the TileDB Cloud provider.  | [optional] 
**result_format** | [**ResultFormat**](ResultFormat.md) |  | [optional] 
**init_commands** | **list[str]** | Queries or commands to run before main query | [optional] 
**parameters** | **list[object]** | SQL query parameters | [optional] 
**task_graph_uuid** | **str** | If set, the ID of the log for the task graph that this was part of.  | [optional] 
**client_node_uuid** | **str** | If set, the client-defined ID of the node within this task&#39;s graph.  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


