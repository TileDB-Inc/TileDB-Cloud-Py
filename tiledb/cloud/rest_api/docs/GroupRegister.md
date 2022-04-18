# GroupRegister

Initial attributes for the registration of a an existing group.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | A human readable description of the contents of the group. | [optional] 
**name** | **str** | The name of the group. If must be unique within the group. | [optional] 
**parent** | **str** | The unique name or id of the parent of the group. If empty, then the new group will be a top level group. | [optional] 
**uri** | **str** | uri of group. | [optional] 
**logo** | **str** | logo (base64 encoded) for the group. Optional | [optional] 
**access_credentials_name** | **str** | the name of the access credentials to use. if unset, the default credentials will be used. | [optional] 
**tags** | **list[str]** | optional tags for groups. | [optional] 
**license_id** | **str** | License identifier from SPDX License List or Custom. | [optional] 
**license_text** | **str** | License text | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


