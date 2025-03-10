# StorageSettingsCreateRequest

The path at which a given asset will be stored, and the credentials used to access that asset. Storage setting contains a pair of storage path and storage credentials

## Properties

| Name                 | Type     | Description                                                                    | Notes |
| -------------------- | -------- | ------------------------------------------------------------------------------ | ----- |
| **name**             | **str**  | storage location name                                                          |
| **is_default**       | **bool** | True if this is the workspace&#39;s or teamspace&#39;s default storage setting |
| **path**             | **str**  | The path to store an asset.                                                    |
| **credentials_name** | **str**  | The name of the credentials used to access this storage path                   |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
