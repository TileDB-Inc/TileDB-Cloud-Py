# ReadState

state for reads

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**initialized** | **bool** | True if the reader has been initialized. | [optional] 
**overflowed** | **bool** | True if the query produced results that could not fit in some buffer. | [optional] 
**unsplittable** | **bool** | True if the current subarray partition is unsplittable. | [optional] 
**subarray_partitioner** | [**SubarrayPartitioner**](SubarrayPartitioner.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


