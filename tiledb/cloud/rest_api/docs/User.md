# User

User
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | unique ID of user | [optional] 
**username** | **str** | username must be unique | 
**password** | **str** | password | [optional] 
**name** | **str** | the user&#39;s full, real name | [optional] 
**email** | **str** | the user&#39;s email | [optional] 
**is_valid_email** | **bool** | user&#39;s email is validated to be correct | [optional] [readonly] 
**stripe_connect** | **bool** | Denotes that the user is able to apply pricing to arrays by means of Stripe Connect | [optional] [readonly] 
**company** | **str** | the user&#39;s company | [optional] 
**logo** | **str** | the user&#39;s logo | [optional] 
**last_activity_date** | **datetime** | when the user last logged in (set by the server) | [optional] [readonly] 
**timezone** | **str** |  | [optional] 
**organizations** | [**list[OrganizationUser]**](OrganizationUser.md) | Array of organizations a user is part of and their roles | [optional] [readonly] 
**allowed_actions** | [**list[NamespaceActions]**](NamespaceActions.md) | list of actions user is allowed to do on this organization | [optional] 
**enabled_features** | **list[str]** | List of extra/optional/beta features to enable for namespace | [optional] [readonly] 
**unpaid_subscription** | **bool** | A notice that the user has an unpaid subscription | [optional] [readonly] 
**default_s3_path** | **str** | default S3 path to store newly created notebooks | [optional] 
**default_s3_path_credentials_name** | **str** | Default S3 path credentials name is the credentials name to use along with default_s3_path | [optional] 
**default_namespace_charged** | **str** | Override the default namespace charged for actions when no namespace is specified | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


