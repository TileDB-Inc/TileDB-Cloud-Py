# OrganizationUser

user in an organization

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **str** | unique ID of user | [optional] 
**organization_id** | **str** | unique ID of organization | [optional] 
**username** | **str** | username for user | [optional] 
**organization_name** | **str** | name of organization | [optional] 
**role** | [**OrganizationRoles**](OrganizationRoles.md) |  | [optional] 
**allowed_actions** | [**[NamespaceActions]**](NamespaceActions.md) | list of actions user is allowed to do on this organization | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


