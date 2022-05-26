# ArraySchema

ArraySchema during creation or retrieval

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**version** | **[int]** | file format version | 
**array_type** | [**ArrayType**](ArrayType.md) |  | 
**tile_order** | [**Layout**](Layout.md) |  | 
**cell_order** | [**Layout**](Layout.md) |  | 
**capacity** | **int** | Capacity of array | 
**coords_filter_pipeline** | [**FilterPipeline**](FilterPipeline.md) |  | 
**offset_filter_pipeline** | [**FilterPipeline**](FilterPipeline.md) |  | 
**domain** | [**Domain**](Domain.md) |  | 
**attributes** | [**[Attribute]**](Attribute.md) | Attributes of array | 
**uri** | **str** | URI of schema | [optional] 
**allows_duplicates** | **bool** | True if the array allows coordinate duplicates. Applicable only to sparse arrays. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


