# ArrayDirectory

Array directory (for reads)

## Properties

| Name                                   | Type                                                                    | Description                                                                                                                      | Notes      |
| -------------------------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| **unfiltered_fragment_uris**           | **list[str]**                                                           | fragment URIs                                                                                                                    | [optional] |
| **consolidated_commit_uris**           | **list[str]**                                                           | consolidated commit URI set                                                                                                      | [optional] |
| **array_schema_uris**                  | **list[str]**                                                           | URIs of all the array schema files                                                                                               | [optional] |
| **latest_array_schema_uri**            | **str**                                                                 | latest array schema URI.                                                                                                         | [optional] |
| **array_meta_uris_to_vacuum**          | **list[str]**                                                           | the array metadata files to vacuum                                                                                               | [optional] |
| **array_meta_vac_uris_to_vacuum**      | **list[str]**                                                           | the array metadata vac files to vacuum                                                                                           | [optional] |
| **commit_uris_to_consolidate**         | **list[str]**                                                           | the commit files to consolidate                                                                                                  | [optional] |
| **commit_uris_to_vacuum**              | **list[str]**                                                           | the commit files to vacuum                                                                                                       | [optional] |
| **consolidated_commit_uris_to_vacuum** | **list[str]**                                                           | the consolidated commit files to vacuum                                                                                          | [optional] |
| **fragment_meta_uris**                 | **list[str]**                                                           | the URIs of the consolidated fragment metadata files                                                                             | [optional] |
| **timestamp_start**                    | **float**                                                               | Only the files created after timestamp_start are listed                                                                          | [optional] |
| **timestamp_end**                      | **float**                                                               | Only the files created before timestamp_end are listed                                                                           | [optional] |
| **array_meta_uris**                    | [**list[TimestampedURI]**](TimestampedURI.md)                           | the timestamped filtered array metadata URIs, after removing the ones that need to be vacuumed and those that do not fall within | [optional] |
| **delete_and_update_tile_location**    | [**list[DeleteAndUpdateTileLocation]**](DeleteAndUpdateTileLocation.md) | the location of delete tiles                                                                                                     | [optional] |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
