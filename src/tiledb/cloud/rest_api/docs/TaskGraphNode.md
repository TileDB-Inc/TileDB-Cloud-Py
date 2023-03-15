# TaskGraphNode

Information about a single node within a registered task graph. A single node represents one piece of data or a computational step; either as an input value, a data source, or a computation that acts upon earlier nodes. The structure parallels the existing `TaskGraphNodeMetadata`. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**client_node_id** | **str** | The client-generated UUID of the given graph node. | [optional] 
**name** | **str** | A client-specified name for the node. If provided, this must be unique.  | [optional] 
**depends_on** | **list[str]** | The client_node_uuid of each node that this node depends upon. Used to define the structure of the graph.  | [optional] 
**array_node** | [**UDFArrayDetails**](UDFArrayDetails.md) |  | [optional] 
**input_node** | [**TGInputNodeData**](TGInputNodeData.md) |  | [optional] 
**sql_node** | [**TGSQLNodeData**](TGSQLNodeData.md) |  | [optional] 
**udf_node** | [**TGUDFNodeData**](TGUDFNodeData.md) |  | [optional] 
**retry_strategy** | [**RetryStrategy**](RetryStrategy.md) |  | [optional] 
**expand_node_output** | **str** | Used to create dynamic tasks based on the output of another node. The other node&#39;s output must be a JSON list of values. The expansion process creates one task per item in the output list. The item is also passed as an argument to each task. The value is the client_node_uuid of the node that we want to expand.  | [optional]
**deadline** | **int** | Duration in seconds relative to the node start time which the node is allowed to run before it gets terminated.  | [optional] 


[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


