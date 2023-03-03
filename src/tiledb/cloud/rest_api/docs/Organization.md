# Organization

Organization
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | unique ID of organization | [optional] 
**role** | [**OrganizationRoles**](OrganizationRoles.md) |  | [optional] 
**name** | **str** | organization name must be unique | 
**created_at** | **datetime** | Datetime organization was created in UTC | [optional] 
**updated_at** | **datetime** | Datetime organization was updated in UTC | [optional] 
**logo** | **str** | Organization logo | [optional] 
**description** | **str** | Organization description | [optional] 
**users** | [**list[OrganizationUser]**](OrganizationUser.md) |  | [optional] 
**allowed_actions** | [**list[NamespaceActions]**](NamespaceActions.md) | list of actions user is allowed to do on this organization | [optional] 
**num_of_arrays** | **float** | number of registered arrays for this organization | [optional] 
**enabled_features** | **list[str]** | List of extra/optional/beta features to enable for namespace | [optional] [readonly] 
**unpaid_subscription** | **bool** | A notice that the user has an unpaid subscription | [optional] [readonly] 
**default_s3_path** | **str** | The default location to store newly-created notebooks and other assets like UDFs. The name &#x60;default_s3_path&#x60; is a legacy holdover; it may refer to any supported storage location.  | [optional] 
**default_s3_path_credentials_name** | **str** | The name of the credentials used to create and access files in the &#x60;default_s3_path&#x60;, if needed.  | [optional] 
**asset_locations** | [**AssetLocations**](AssetLocations.md) |  | [optional] 
**stripe_connect** | **bool** | Denotes that the organization is able to apply pricing to arrays by means of Stripe Connect | [optional] [readonly] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


