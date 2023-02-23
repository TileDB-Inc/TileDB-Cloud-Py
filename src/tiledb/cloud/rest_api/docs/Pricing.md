# Pricing

Pricing created by converting an array to product
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique ID of plan as defined by Stripe | [optional] 
**array_uuid** | **str** | Unique ID of registered array | [optional] 
**pricing_name** | **str** | Name of pricing | [optional] 
**pricing_type** | [**PricingType**](PricingType.md) |  | [optional] 
**product_name** | **str** | Name of product | [optional] 
**product_statement_descriptor** | **str** | Extra information about a product which will appear on the credit card statement of the customer | [optional] 
**product_unit_label** | [**PricingUnitLabel**](PricingUnitLabel.md) |  | [optional] 
**currency** | [**PricingCurrency**](PricingCurrency.md) |  | [optional] 
**aggregate_usage** | [**PricingAggregateUsage**](PricingAggregateUsage.md) |  | [optional] 
**interval** | [**PricingInterval**](PricingInterval.md) |  | [optional] 
**divided_by** | **int** | Group of n product unit labels | [optional] 
**charge** | **float** | Price in cents (decimal) per unitlabel | [optional] 
**activated** | **bool** | If pricing is activated | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


