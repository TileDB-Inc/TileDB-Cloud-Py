# Array

Represents an open array

## Properties

| Name                        | Type                                              | Description                                                | Notes      |
| --------------------------- | ------------------------------------------------- | ---------------------------------------------------------- | ---------- |
| **query_type**              | [**Querytype**](Querytype.md)                     |                                                            |
| **uri**                     | **str**                                           | Array uri                                                  |
| **end_timestamp**           | **float**                                         | Ending timestamp (epoch milliseconds) array is opened at   | [optional] |
| **start_timestamp**         | **float**                                         | Starting timestamp (epoch milliseconds) array is opened at | [optional] |
| **array_schema_latest**     | [**ArraySchema**](ArraySchema.md)                 |                                                            | [optional] |
| **array_schemas_all**       | [**ArraySchemaMap**](ArraySchemaMap.md)           |                                                            | [optional] |
| **array_metadata**          | [**ArrayMetadata**](ArrayMetadata.md)             |                                                            | [optional] |
| **non_empty_domain**        | [**NonEmptyDomainList**](NonEmptyDomainList.md)   |                                                            | [optional] |
| **array_directory**         | [**ArrayDirectory**](ArrayDirectory.md)           |                                                            | [optional] |
| **fragment_metadata_all**   | [**list[FragmentMetadata]**](FragmentMetadata.md) | metadata for all fragments (for reads)                     | [optional] |
| **opened_at_end_timestamp** | **float**                                         | The ending timestamp that the array was last opened at     | [optional] |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
