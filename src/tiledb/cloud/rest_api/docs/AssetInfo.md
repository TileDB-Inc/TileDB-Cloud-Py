# AssetInfo

metadata of an asset

## Properties

| Name                      | Type                                              | Description                                    | Notes                 |
| ------------------------- | ------------------------------------------------- | ---------------------------------------------- | --------------------- |
| **uuid**                  | **str**                                           | unique ID of a registered asset                | [optional]            |
| **asset_type**            | [**AssetType**](AssetType.md)                     |                                                | [optional]            |
| **asset_backing_type**    | [**AssetBackingType**](AssetBackingType.md)       |                                                | [optional]            |
| **asset_ownership_level** | [**AssetOwnershipLevel**](AssetOwnershipLevel.md) |                                                | [optional]            |
| **namespace_name**        | **str**                                           | namespace_name that the asset is registered to | [optional]            |
| **namespace_uuid**        | **str**                                           | namespace_uuid that the asset is registered to | [optional]            |
| **name**                  | **str**                                           | name of asset                                  | [optional]            |
| **mime_type**             | **str**                                           | mime type of the asset                         | [optional]            |
| **created_at**            | **datetime**                                      | Time when the asset was created (rfc3339)      | [optional] [readonly] |
| **metadata**              | [**MetadataStringified**](MetadataStringified.md) |                                                | [optional]            |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
