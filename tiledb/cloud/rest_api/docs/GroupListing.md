# GroupListing

The contents of a group i.e attributes, subgroups and assets
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | the globally unique id of the group | [optional] 
**namespace** | **str** | The namespace of the group | [optional] 
**name** | **str** | The name of the group. It is unique within the namespace. No 2 groups can have the same name | [optional] 
**description** | **str** | A human readable description of the content of the group | [optional] 
**groups** | [**list[Group]**](Group.md) | Contains one page of subgroups of the group. | [optional] 
**assets** | [**list[ArrayInfo]**](ArrayInfo.md) | Contains one page of assets of the group as ArrayInfos | [optional] 
**pagination_metadata** | [**PaginationMetadata**](PaginationMetadata.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


