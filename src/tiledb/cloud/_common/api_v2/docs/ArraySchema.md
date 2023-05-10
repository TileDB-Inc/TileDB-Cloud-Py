# ArraySchema

ArraySchema during creation or retrieval

## Properties

| Name                         | Type                                    | Description                                                                       | Notes      |
| ---------------------------- | --------------------------------------- | --------------------------------------------------------------------------------- | ---------- |
| **uri**                      | **str**                                 | URI of schema                                                                     | [optional] |
| **name**                     | **str**                                 | name of schema                                                                    | [optional] |
| **version**                  | **list[int]**                           | file format version                                                               |
| **array_type**               | [**ArrayType**](ArrayType.md)           |                                                                                   |
| **tile_order**               | [**Layout**](Layout.md)                 |                                                                                   |
| **cell_order**               | [**Layout**](Layout.md)                 |                                                                                   |
| **capacity**                 | **int**                                 | Capacity of array                                                                 |
| **coords_filter_pipeline**   | [**FilterPipeline**](FilterPipeline.md) |                                                                                   |
| **offset_filter_pipeline**   | [**FilterPipeline**](FilterPipeline.md) |                                                                                   |
| **validity_filter_pipeline** | [**FilterPipeline**](FilterPipeline.md) |                                                                                   | [optional] |
| **domain**                   | [**Domain**](Domain.md)                 |                                                                                   |
| **attributes**               | [**list[Attribute]**](Attribute.md)     | Attributes of array                                                               |
| **allows_duplicates**        | **bool**                                | True if the array allows coordinate duplicates. Applicable only to sparse arrays. | [optional] |
| **timestamp_range**          | **list[int]**                           | The list of sizes per range                                                       | [optional] |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
