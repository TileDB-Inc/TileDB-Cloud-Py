# Invitation

Invitations to share or collaborate
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique ID of invitation added to magic link | [optional] 
**invitation_type** | [**InvitationType**](InvitationType.md) |  | [optional] 
**owner_namespace_uuid** | **str** | Namespace of the owner of the invitation (user or organization) | [optional] 
**user_namespace_uuid** | **str** | Unique ID of the user accepted the invitation | [optional] 
**organization_user_uuid** | **str** | Unique ID of the organization user accepted the invitation | [optional] 
**organization_name** | **str** | Name of the organization, does not persist in database | [optional] 
**organization_role** | [**OrganizationRoles**](OrganizationRoles.md) |  | [optional] 
**array_uuid** | **str** | Unique ID of the array | [optional] 
**array_name** | **str** | Name of the array, does not persist in database | [optional] 
**email** | **str** | Email of the individual we send the invitation to | [optional] 
**actions** | **str** | A comma separated list of ArrayActions or NamespaceActions | [optional] 
**status** | [**InvitationStatus**](InvitationStatus.md) |  | [optional] 
**created_at** | **datetime** | Datetime the invitation was created in UTC | [optional] 
**expires_at** | **datetime** | Datetime the invitation is expected to expire in UTC | [optional] 
**accepted_at** | **datetime** | Datetime the invitation was accepted in UTC | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


