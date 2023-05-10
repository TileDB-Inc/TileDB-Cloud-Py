# GenericTileOffsets

Array directory (for reads)

## Properties

| Name                                       | Type            | Description                                      | Notes      |
| ------------------------------------------ | --------------- | ------------------------------------------------ | ---------- |
| **rtree**                                  | **float**       | RTree serialized as a blob                       | [optional] |
| **tile_offsets**                           | **list[float]** | tile offsets                                     | [optional] |
| **tile_var_offsets**                       | **list[float]** | variable tile offsets                            | [optional] |
| **tile_var_sizes**                         | **list[float]** | sizes of the uncompressed variable tiles offsets | [optional] |
| **tile_validity_offsets**                  | **list[float]** | tile validity offsets                            | [optional] |
| **tile_min_offsets**                       | **list[float]** | min tile offsets                                 | [optional] |
| **tile_max_offsets**                       | **list[float]** | max tile offsets                                 | [optional] |
| **tile_sum_offsets**                       | **list[float]** | tile sum offsets                                 | [optional] |
| **tile_null_count_offsets**                | **list[float]** | null count offsets                               | [optional] |
| **fragment_min_max_sum_null_count_offset** | **float**       | fragment min/max/sum/nullcount offsets           | [optional] |
| **processed_conditions_offsets**           | **float**       | processed conditions offsets                     | [optional] |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
