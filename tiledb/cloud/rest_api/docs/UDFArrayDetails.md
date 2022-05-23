# UDFArrayDetails

Contains array details for multi-array query including uri, ranges buffers

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**parameter_id** | **str, none_type** | An optional client-generated identifier to distinguish between multiple range/buffer requests from the same array in the same call. This may be set for MultiArrayUDFs that use the &#x60;argument_json&#x60; style of passing arrays.  | [optional] 
**uri** | **str** | array to set ranges and buffers on, must be in tiledb:// format | [optional] 
**ranges** | [**QueryRanges**](QueryRanges.md) |  | [optional] 
**buffers** | **[str]** | List of buffers to fetch (attributes + dimensions) | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


