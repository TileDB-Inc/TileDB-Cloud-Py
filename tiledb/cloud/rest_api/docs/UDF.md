# UDF

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**registered_udf** | **str** | name of registered udf to run, format is {namespace}/{udf_name}. Can not be used with exec | [optional] 
**language** | [**UDFLanguage**](UDFLanguage.md) |  | [optional] 
**version** | **str** | Type-specific version | [optional] 
**image_name** | **str** | Docker image name to use for udf | [optional] 
**ranges** | [**UDFRanges**](UDFRanges.md) |  | [optional] 
**subarray** | [**UDFSubarray**](UDFSubarray.md) |  | [optional] 
**_exec** | **str** | Type-specific executable text | [optional] 
**exec_raw** | **str** | optional raw text to store of serialized function, used for showing in UI | [optional] 
**buffers** | **list[str]** | List of buffers to fetch (attributes + coordinates) | [optional] 
**result_format** | [**UDFResultType**](UDFResultType.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


