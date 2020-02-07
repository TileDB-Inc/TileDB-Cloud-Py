# Organization

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | unique id of organization | [optional] 
**role** | [**OrganizationRoles**](OrganizationRoles.md) |  | [optional] 
**name** | **str** | organization name must be unique | 
**created_at** | **datetime** | Datetime organization was created in UTC | [optional] 
**updated_at** | **datetime** | Datetime organization was updated in UTC | [optional] 
**logo** | **str** | Organization logo | [optional] 
**description** | **str** | Organization description | [optional] 
**users** | [**list[OrganizationUser]**](OrganizationUser.md) |  | [optional] 
**allowed_actions** | [**list[NamespaceActions]**](NamespaceActions.md) | list of actions user is allowed to do on this organization | [optional] 
**num_of_arrays** | **float** | number of registered arrays for this organization | [optional] 
**enabled_features** | **list[str]** | List of extra/optional/beta features to enable for namespace | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


