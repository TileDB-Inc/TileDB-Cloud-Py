# RegisteredTaskGraph

The structure and metadata of a task graph that can be stored on TileDB Cloud and executed by users who have access to it. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**uuid** | **str** | A server-assigned unique ID for the UDF, in UUID format. | [optional] 
**namespace** | **str** | The namespace that owns this task graph log. | [optional] 
**name** | **str** | The name of this graph, to appear in URLs. Must be unique per-namespace.  | [optional] 
**readme** | **str** | Documentation for the task graph, in Markdown format. | [optional] 
**license_id** | **str, none_type** | SPDX license identifier. | [optional] 
**license_text** | **str, none_type** | Full text of the license. | [optional] 
**tags** | **[str]** | Optional tags to classify the graph. | [optional] 
**nodes** | [**[RegisteredTaskGraphNode]**](RegisteredTaskGraphNode.md) | The structure of the graph, in the form of the nodes that make it up. As with &#x60;TaskGraphLog&#x60;, nodes must topologically sorted, so that any node appears after all the nodes it depends on.  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


