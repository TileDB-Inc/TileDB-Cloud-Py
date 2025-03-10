# Asset

## Properties

| Name             | Type                                        | Description                       | Notes      |
| ---------------- | ------------------------------------------- | --------------------------------- | ---------- |
| **id**           | **str**                                     | The asset&#39;s ID                |
| **workspace_id** | **str**                                     | The workspace&#39;s ID            |
| **teamspace_id** | **str**                                     | The teamspace&#39;s ID            |
| **name**         | **str**                                     | The name of the asset.            |
| **description**  | **str**                                     | The description of the asset.     | [optional] |
| **member_type**  | [**AssetMemberType**](AssetMemberType.md)   |                                   | [optional] |
| **mime**         | **str**                                     | The MIME type of the asset.       | [optional] |
| **backing_type** | [**AssetBackingType**](AssetBackingType.md) |                                   |
| **type**         | [**AssetType**](AssetType.md)               |                                   |
| **created_at**   | **datetime**                                | Datetime asset was created in UTC |
| **updated_at**   | **datetime**                                | Datetime asset was updated in UTC | [optional] |
| **created_by**   | [**WorkspaceUser**](WorkspaceUser.md)       |                                   |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
