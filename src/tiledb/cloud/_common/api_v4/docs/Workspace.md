# Workspace

The response object of the GetWorkspace endpoint

## Properties

| Name             | Type                                  | Description                           | Notes      |
| ---------------- | ------------------------------------- | ------------------------------------- | ---------- |
| **workspace_id** | **str**                               | The workspace&#39;s ID                |
| **image_id**     | **str**                               | The image&#39;s ID                    | [optional] |
| **name**         | **str**                               | workspace name                        |
| **created_by**   | [**WorkspaceUser**](WorkspaceUser.md) |                                       |
| **description**  | **str**                               | Workspace description                 | [optional] |
| **\_self**       | [**WorkspaceUser**](WorkspaceUser.md) |                                       |
| **created_at**   | **datetime**                          | Datetime workspace was created in UTC |
| **updated_at**   | **datetime**                          | Datetime workspace was updated in UTC | [optional] |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
