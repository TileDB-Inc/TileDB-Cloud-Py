# QueryReader

Read struct (can't be called reader due to class name conflict)

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**layout** | [**Layout**](Layout.md) |  | [optional] 
**subarray** | [**Subarray**](Subarray.md) |  | [optional] 
**read_state** | [**ReadState**](ReadState.md) |  | [optional] 
**var_offsets_mode** | **str** | The offsets format (bytes or elements) to be used. | [optional] 
**var_offsets_add_extra_element** | **bool** | True if an extra element will be added to the end of the offsets buffer. | [optional] 
**var_offsets_bitsize** | **int** | The offsets bitsize (32 or 64) to be used. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


