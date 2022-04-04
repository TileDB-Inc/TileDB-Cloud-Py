# GroupInfo

metadata of a group
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | unique ID of registered group | [optional] 
**namespace** | **str** | namespace group is in | [optional] 
**name** | **str** | name of group | [optional] 
**description** | **str** | description of group | [optional] 
**uri** | **str** | uri of group | [optional] 
**tiledb_uri** | **str** | uri for access through TileDB cloud | [optional] 
**asset_count** | **float** | A count of direct array members | [optional] 
**group_count** | **float** | A count of direct group members | [optional] 
**size** | **float** | A count of direct members. This is the sum of asset_count and group_count | [optional] 
**last_accessed** | **datetime** | Datetime groups was last accessed in UTC | [optional] 
**allowed_actions** | [**list[GroupActions]**](GroupActions.md) | list of actions user is allowed to do on this group | [optional] 
**logo** | **str** | logo (base64 encoded) for the gruop. Optional | [optional] 
**access_credentials_name** | **str** | the name of the access credentials to use. if unset, the default credentials will be used | [optional] 
**share_count** | **float** | number of unique namespaces this group is shared with | [optional] 
**public_share** | **bool** | Suggests if the group was shared to public by owner | [optional] 
**tags** | **list[str]** | optional tags for group | [optional] 
**license_id** | **str** | License identifier from SPDX License List or Custom | [optional] 
**license_text** | **str** | License text | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


