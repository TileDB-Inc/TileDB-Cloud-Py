# AssetActivityLog

## Properties

| Name              | Type                                                  | Description                     | Notes      |
| ----------------- | ----------------------------------------------------- | ------------------------------- | ---------- |
| **id**            | **str**                                               | The ID of the activity          |
| **event_at**      | **datetime**                                          | time event took place (RFC3339) |
| **action**        | **str**                                               | type of the event               |
| **username**      | **str**                                               | User who performed action       |
| **array_task_id** | **str**                                               | uuid of associated array task   | [optional] |
| **asset**         | [**AssetActivityLogAsset**](AssetActivityLogAsset.md) |                                 |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
