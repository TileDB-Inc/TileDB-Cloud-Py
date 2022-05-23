# ArrayActivityLog

Actvity of an Array

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**event_at** | **datetime** | time event took place (RFC3339) | [optional] 
**action** | [**ActivityEventType**](ActivityEventType.md) |  | [optional] 
**username** | **str** | User who performed action | [optional] 
**bytes_sent** | **int** | Bytes sent to client | [optional] 
**bytes_received** | **int** | Bytes recieved from client | [optional] 
**array_task_id** | **str** | UUID of associated array task | [optional] 
**id** | **str** | ID of the activity | [optional] 
**query_ranges** | **str** | ranges for query | [optional] 
**query_stats** | **str** | stats for query | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


