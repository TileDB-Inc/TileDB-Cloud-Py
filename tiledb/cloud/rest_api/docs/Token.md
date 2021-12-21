# Token

A api token and its metadata
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**token** | **str** | A api token | [optional] 
**name** | **str** | Name of token to revoke | [optional] 
**issued_at** | **datetime** | datetime the token was created | [optional] 
**expires_at** | **datetime** | datetime the token when token will expire | [optional] 
**scope** | **str** | Optional scope to limit token, defaults to all permissions, current supported values are password_reset or * | [optional] [default to '*']

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


