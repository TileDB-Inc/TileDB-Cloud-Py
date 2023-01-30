# TaskGraph

Information about a task graph.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**uuid** | **str** | The server-generated UUID of the task graph. | [optional] [readonly] 
**namespace** | **str** | The namespace that owns this task graph. When creating a task graph log, this is used as the namespace to create the log in; thereafter it is read-only.  | [optional] 
**created_by** | **str** | The name of the user who created this task graph log. | [optional] [readonly] 
**name** | **str** | A name for this task graph, displayed in the UI. Does not need to be unique.  | [optional] 
**created_at** | **datetime** | The date/time when this task graph was originally created.  | [optional] [readonly] 
**nodes** | [**list[TaskGraphNode]**](TaskGraphNode.md) | The structure of the graph. This is provided by the client when first setting up the task graph.  This must be topographically sorted; that is, each node must appear after all nodes that it depends upon.  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


