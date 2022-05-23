# UDFInfoUpdate

User-defined function that can persist in db, used and shared multiple times

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | name of UDF | [optional] 
**language** | [**UDFLanguage**](UDFLanguage.md) |  | [optional] 
**version** | **str** | Type-specific version | [optional] 
**image_name** | **str** | Docker image name to use for UDF | [optional] 
**type** | [**UDFType**](UDFType.md) |  | [optional] 
**_exec** | **str** | Type-specific executable text | [optional] 
**exec_raw** | **str** | optional raw text to store of serialized function, used for showing in UI | [optional] 
**readme** | **str** | Markdown readme of UDFs | [optional] 
**license_id** | **str** | License identifier from SPDX License List or Custom | [optional] 
**license_text** | **str** | License text | [optional] 
**tags** | **[str]** | optional tags for UDF | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


