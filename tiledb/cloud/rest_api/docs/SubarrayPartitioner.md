# SubarrayPartitioner

The subarray partitioner

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**subarray** | [**Subarray**](Subarray.md) |  | [optional] 
**budget** | [**[AttributeBufferSize]**](AttributeBufferSize.md) | Result size budget (in bytes) for all attributes. | [optional] 
**current** | [**SubarrayPartitionerCurrent**](SubarrayPartitionerCurrent.md) |  | [optional] 
**state** | [**SubarrayPartitionerState**](SubarrayPartitionerState.md) |  | [optional] 
**memory_budget** | **int** | The memory budget for the fixed-sized attributes and the offsets of the var-sized attributes | [optional] 
**memory_budget_var** | **int** | The memory budget for the var-sized attributes | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


