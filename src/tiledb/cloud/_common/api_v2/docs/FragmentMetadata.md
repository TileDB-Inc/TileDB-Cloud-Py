# FragmentMetadata

Metadata of a fragment

## Properties

| Name                        | Type                                            | Description                                                    | Notes      |
| --------------------------- | ----------------------------------------------- | -------------------------------------------------------------- | ---------- |
| **file_sizes**              | **list[float]**                                 | The size of each attribute file                                | [optional] |
| **file_var_sizes**          | **list[float]**                                 | The size of each var attribute file                            | [optional] |
| **file_validity_sizes**     | **list[float]**                                 | The size of each validity attribute file                       | [optional] |
| **fragment_uri**            | **str**                                         | The uri of the fragment this metadata belongs to               | [optional] |
| **has_timestamps**          | **bool**                                        | True if the fragment has timestamps                            | [optional] |
| **has_delete_meta**         | **bool**                                        | True if the fragment has delete metadata                       | [optional] |
| **sparse_tile_num**         | **float**                                       | The number of sparse tiles                                     | [optional] |
| **tile_index_base**         | **float**                                       | Used to track the tile index base between global order writes  | [optional] |
| **tile_offsets**            | **list[list[float]]**                           | Tile offsets in their attribute files                          | [optional] |
| **tile_var_offsets**        | **list[list[float]]**                           | Variable tile offsets in their attribute files                 | [optional] |
| **tile_var_sizes**          | **list[list[float]]**                           | The sizes of the uncompressed variable tiles                   | [optional] |
| **tile_validity_offsets**   | **list[list[float]]**                           | Validity tile offests in their attribute files                 | [optional] |
| **tile_min_buffer**         | **list[list[float]]**                           | tile min buffers                                               | [optional] |
| **tile_min_var_buffer**     | **list[list[float]]**                           | tile min buffers for var length data                           | [optional] |
| **tile_max_buffer**         | **list[list[float]]**                           | tile max buffers                                               | [optional] |
| **tile_max_var_buffer**     | **list[list[float]]**                           | tile max buffers for var length data                           | [optional] |
| **tile_sums**               | **list[list[float]]**                           | tile sum values                                                | [optional] |
| **tile_null_counts**        | **list[list[float]]**                           | tile null count values                                         | [optional] |
| **fragment_mins**           | **list[list[float]]**                           | fragment min values                                            | [optional] |
| **fragment_maxs**           | **list[list[float]]**                           | fragment max values                                            | [optional] |
| **fragment_sums**           | **list[float]**                                 | fragment sum values                                            | [optional] |
| **fragment_null_counts**    | **list[float]**                                 | fragment null count values                                     | [optional] |
| **version**                 | **int**                                         | the format version of this metadata                            | [optional] |
| **timestamp_range**         | **list[float]**                                 | A pair of timestamps for fragment                              | [optional] |
| **last_tile_cell_num**      | **int**                                         | The number of cells in the last tile                           | [optional] |
| **non_empty_domain**        | [**NonEmptyDomainList**](NonEmptyDomainList.md) |                                                                | [optional] |
| **rtree**                   | **file**                                        | The RTree for the MBRs serialized as a blob                    | [optional] |
| **has_consolidated_footer** | **bool**                                        | if the fragment metadata footer appears in a consolidated file | [optional] |
| **gt_offsets**              | [**GenericTileOffsets**](GenericTileOffsets.md) |                                                                | [optional] |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
