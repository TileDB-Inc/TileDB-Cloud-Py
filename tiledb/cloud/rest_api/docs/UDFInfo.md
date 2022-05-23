# UDFInfo

User-defined function that can persist in db, used and shared multiple times

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique ID of UDF | [optional] 
**name** | **str** | name of UDF | [optional] 
**language** | [**UDFLanguage**](UDFLanguage.md) |  | [optional] 
**type** | [**UDFType**](UDFType.md) |  | [optional] 
**readme** | **str** | Markdown readme of UDFs | [optional] 
**license_id** | **str** | License identifier from SPDX License List or Custom | [optional] 
**license_text** | **str** | License text | [optional] 
**tags** | **[str]** | optional tags for UDF | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


