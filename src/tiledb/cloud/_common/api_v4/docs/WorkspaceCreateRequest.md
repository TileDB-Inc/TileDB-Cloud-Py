# WorkspaceCreateRequest

object metadata for a workspace that will be created

## Properties

| Name                        | Type                                                                | Description                                                  | Notes      |
| --------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------ | ---------- |
| **name**                    | **str**                                                             | workspace name                                               |
| **description**             | **str**                                                             | Workspace description                                        | [optional] |
| **image**                   | **str**                                                             | Image data in the form data:image/png;base64,iVBORw0KGgoAAAA | [optional] |
| **default_credential**      | [**CredentialCreateRequest**](CredentialCreateRequest.md)           |                                                              |
| **default_storage_setting** | [**StorageSettingsCreateRequest**](StorageSettingsCreateRequest.md) |                                                              |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
