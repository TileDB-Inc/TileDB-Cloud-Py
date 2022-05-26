# RegisteredTaskGraphNode

Information about a single node within a registered task graph. A single node represents one piece of data or a computational step; either as an input value, a data source, or a computation that acts upon earlier nodes. The structure parallels the existing `TaskGraphNodeMetadata`. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**client_node_id** | **str** | The client-generated UUID of the given graph node. | [optional] 
**name** | **str, none_type** | A client-specified name for the node. If provided, this must be unique.  | [optional] 
**depends_on** | **[str]** | The client_node_uuid of each node that this node depends upon. Used to define the structure of the graph.  | [optional] 
**array_node** | [**UDFArrayDetails**](UDFArrayDetails.md) |  | [optional] 
**input_node** | [**TGInputNodeData**](TGInputNodeData.md) |  | [optional] 
**sql_node** | [**TGSQLNodeData**](TGSQLNodeData.md) |  | [optional] 
**udf_node** | [**TGUDFNodeData**](TGUDFNodeData.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


