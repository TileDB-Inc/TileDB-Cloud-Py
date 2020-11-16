# Subscription

Subscription of a user (customer) to another user's arrays
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique id of subscription as defined by Stripe | [optional] 
**owner_namespace_uuid** | **str** | Unique id of the array (product) owner | [optional] 
**customer_namespace_uuid** | **str** | Unique id of the array (product) user (customer) | [optional] 
**pricing** | [**list[Pricing]**](Pricing.md) | list of pricing used by this subscription | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


