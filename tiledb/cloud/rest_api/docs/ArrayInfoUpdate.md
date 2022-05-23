# ArrayInfoUpdate

metadata of an array

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str, none_type** | description of array | [optional] 
**name** | **str** | description of array | [optional] 
**uri** | **str** | uri of array | [optional] 
**file_type** | [**FileType**](FileType.md) |  | [optional] 
**file_properties** | **{str: (str,)}** | map of file properties created for this array | [optional] 
**access_credentials_name** | **str** | the name of the access credentials to use. if unset, the default credentials will be used | [optional] 
**logo** | **str** | logo (base64 encoded) for the array. Optional | [optional] 
**tags** | **[str]** | optional tags for array | [optional] 
**license_id** | **str** | License identifier from SPDX License List or Custom | [optional] 
**license_text** | **str** | License text | [optional] 
**read_only** | **bool** | Suggests if the array is in read_only mode | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


