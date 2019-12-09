# ArrayInfo

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | unique id of registered array | [optional] 
**uri** | **str** | uri of array | [optional] 
**namespace** | **str** | namespace array is in | [optional] 
**size** | **float** | size in bytes of array | [optional] 
**last_accessed** | **datetime** | Datetime array was last accessed in UTC | [optional] 
**description** | **str** | description of array | [optional] 
**name** | **str** | name of array | [optional] 
**allowed_actions** | [**list[ArrayActions]**](ArrayActions.md) | list of actions user is allowed to do on this array | [optional] 
**logo** | **str** | logo (base64 encoded) for the array. Optional | [optional] 
**access_credentials_name** | **str** | the name of the access credentials to use. if unset, the default credentials will be used | [optional] 
**type** | **str** | Array type (dense, key-value, sparse) | [optional] 
**share_count** | **float** | number of unique namespaces this array is shared with | [optional] 
**public_share** | **bool** | Suggests if the array was shared to public by owner | [optional] 
**tiledb_uri** | **str** | uri for access through TileDB cloud | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


