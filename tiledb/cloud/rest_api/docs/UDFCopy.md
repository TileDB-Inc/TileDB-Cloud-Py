# UDFCopy

information required to copy a udf

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**output_uri** | **str** | output location of the TileDB File | [optional] 
**namespace** | **str** | namespace to register the copy. If empty use the namespace of the request user | [optional] 
**name** | **str** | name to set for the copy. If empty use the name as the original udf, if it not already used in the namespace | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


