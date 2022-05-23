# AWSAccessCredentials

Model representing aws keys or service role, service roles are currently ignored, but will be preferred option in the future

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**secret_access_key** | **str** | aws secret access key, never returned in get requests | [optional] 
**access_key_id** | **str** | aws access key | [optional] 
**service_role_arn** | **str** | aws service role to use for access | [optional] 
**name** | **str** | human readable name | [optional] 
**default** | **bool** | true if this is the default credential to be used within this namespace | [optional] 
**buckets** | **[str]** | a whitelist of one or more buckets this key should access | [optional] 
**created_at** | **datetime** | Time when UDF dependencies were created (rfc3339) | [optional] [readonly] 
**updated_at** | **datetime** | Time when UDF dependencies was last updated (rfc3339) | [optional] [readonly] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


