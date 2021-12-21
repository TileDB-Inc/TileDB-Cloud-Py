# ArrayInfo

metadata of an array
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | unique ID of registered array | [optional] 
**file_type** | [**FileType**](FileType.md) |  | [optional] 
**file_properties** | **dict(str, str)** | map of file properties created for this array | [optional] 
**uri** | **str** | uri of array | [optional] 
**namespace** | **str** | namespace array is in | [optional] 
**size** | **float** | size in bytes of array | [optional] 
**last_accessed** | **datetime** | Datetime array was last accessed in UTC | [optional] 
**description** | **str** | description of array | [optional] 
**name** | **str** | name of array | [optional] 
**allowed_actions** | [**list[ArrayActions]**](ArrayActions.md) | list of actions user is allowed to do on this array | [optional] 
**pricing** | [**list[Pricing]**](Pricing.md) | list of pricing created for this array | [optional] 
**subscriptions** | [**list[Subscription]**](Subscription.md) | list of subscriptions created for this array | [optional] 
**logo** | **str** | logo (base64 encoded) for the array. Optional | [optional] 
**access_credentials_name** | **str** | the name of the access credentials to use. if unset, the default credentials will be used | [optional] 
**type** | **str** | Array type (dense, key-value, sparse) | [optional] 
**share_count** | **float** | number of unique namespaces this array is shared with | [optional] 
**public_share** | **bool** | Suggests if the array was shared to public by owner | [optional] 
**namespace_subscribed** | **bool** | Depends on the namespace asking, denotes the existence of subscription of namespace to this array | [optional] [readonly] 
**tiledb_uri** | **str** | uri for access through TileDB cloud | [optional] 
**tags** | **list[str]** | optional tags for array | [optional] 
**license_id** | **str** | License identifier from SPDX License List or Custom | [optional] 
**license_text** | **str** | License text | [optional] 
**read_only** | **bool** | Suggests if the array is in read_only mode | [optional] 
**is_favorite** | **bool** | Indicates whether the array is in user favorites | [optional] 
**favorite_uuid** | **str** | The favorite UUID if the array if is_favorite is true | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


