# TaskGraphLog

Logging information about the execution of a task graph.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**uuid** | **str** | The server-generated UUID of the task graph. | [optional] [readonly] 
**namespace** | **str** | The namespace that owns this task graph log. When creating a task graph log, this is used as the namespace to create the log in; thereafter it is read-only.  | [optional] 
**created_by** | **str** | The name of the user who created this task graph log. | [optional] [readonly] 
**name** | **str** | A name for this task graph log, displayed in the UI. Does not need to be unique.  | [optional] 
**created_at** | **datetime** | The date/time when this task graph log was originally created. This is distinct from the execution start_time.  | [optional] [readonly] 
**start_time** | **datetime** | The start time of the task graph, recorded when the server starts executing the first node.  | [optional] [readonly] 
**end_time** | **datetime** | The end time of the task graph, recorded when the client reports completion.  | [optional] [readonly] 
**status** | [**TaskGraphLogStatus**](TaskGraphLogStatus.md) |  | [optional] 
**total_cost** | **float** | If present, the total cost of executing all nodes in this task graph.  | [optional] 
**access_cost** | **float** | If present, the total cost of access from execution of the nodes in this task graph.  | [optional] 
**egress_cost** | **float** | If present, the total cost of access from execution of the nodes in this task graph.  | [optional] 
**execution_time** | **str** | The total execution time of all the nodes in this graph, in ISO 8601 format with hours, minutes, and seconds.  | [optional] 
**status_count** | **dict(str, float)** | A mapping from &#x60;ArrayTaskStatus&#x60; string value to the number of nodes in this graph that are in that status.  | [optional] 
**nodes** | [**list[TaskGraphNodeMetadata]**](TaskGraphNodeMetadata.md) | The structure of the graph. This is provided by the client when first setting up the task graph. Thereafter, it is read-only. This must be topographically sorted; that is, each node must appear after all nodes that it depends upon.  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


