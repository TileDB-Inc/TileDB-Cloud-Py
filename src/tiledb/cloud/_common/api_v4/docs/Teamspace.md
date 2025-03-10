# Teamspace

The teamspace object

## Properties

| Name             | Type                                              | Description                                                  | Notes      |
| ---------------- | ------------------------------------------------- | ------------------------------------------------------------ | ---------- |
| **teamspace_id** | **str**                                           | The teamspace&#39;s ID                                       |
| **name**         | **str**                                           | The teamspace name                                           |
| **icon**         | **str**                                           | The teamspace icon as a UTF8-encoded Unicode symbol, e.g. 🚀 | [optional] |
| **created_at**   | **datetime**                                      | The datetime the teamspace was created (in UTC)              |
| **created_by**   | [**TeamspaceUser**](TeamspaceUser.md)             |                                                              |
| **description**  | **str**                                           | The teamspace description                                    | [optional] |
| **\_self**       | [**TeamspaceUser**](TeamspaceUser.md)             |                                                              | [optional] |
| **visibility**   | [**TeamspaceVisibility**](TeamspaceVisibility.md) |                                                              |
| **updated_at**   | **datetime**                                      | The datetime the teamspace was updated (in UTC)              | [optional] |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
