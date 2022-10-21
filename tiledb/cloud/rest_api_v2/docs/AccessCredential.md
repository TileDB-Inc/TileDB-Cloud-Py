# AccessCredential

A union type which may contain a credential to access any one cloud provider.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | A user-specified name for the key | [optional] 
**provider** | [**CloudProvider**](CloudProvider.md) |  | [optional] 
**provider_default** | **bool** | True if this is the namespace&#39;s default credential to be used when connecting to the given cloud provider. There can be at most one default for each unique provider. | [optional] 
**created_at** | **datetime** | Time when the credential was created (rfc3339) | [optional] [readonly] 
**updated_at** | **datetime** | Time when the credential was last updated (rfc3339) | [optional] [readonly] 
**credential** | [**AccessCredentialCredential**](AccessCredentialCredential.md) |  | [optional] 
**role** | [**AccessCredentialRole**](AccessCredentialRole.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


