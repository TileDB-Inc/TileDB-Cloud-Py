# GroupSharing

sharing state of a group with a namespace

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**group_actions** | [**[GroupActions]**](GroupActions.md) | List of permitted actions for the group and all subgroups | [optional] 
**array_actions** | [**[ArrayActions]**](ArrayActions.md) | List of permitted actions for all the subarrays of the group | [optional] 
**namespace** | **str** | namespace being granted group access can be a user or organization | [optional] 
**namespace_type** | **str** | details on if the namespace is a organization or user | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


