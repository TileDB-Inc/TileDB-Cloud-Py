# UDFInfoVersion

Version of User-defined function that can persist in db
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique id of a versioned udf | [optional] 
**udf_image_uuid** | **str** | Unique id of the versioned image used by current udf version | [optional] 
**name** | **str** | name of udf version | [optional] 
**version** | **str** | Type-specific version | [optional] 
**image_name** | **str** | Docker image name to use for udf | [optional] 
**_exec** | **str** | Type-specific executable text | [optional] 
**exec_raw** | **str** | optional raw text to store of serialized function, used for showing in UI | [optional] 
**default** | **bool** | If current image version is default version | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


