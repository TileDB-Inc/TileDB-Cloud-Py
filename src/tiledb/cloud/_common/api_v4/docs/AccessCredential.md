# AccessCredential

The user credential object

## Properties

| Name                 | Type                                                | Description                                                                                                                                                         | Notes      |
| -------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| **credential_type**  | [**CredentialType**](CredentialType.md)             |                                                                                                                                                                     |
| **uuid**             | **str**                                             | The UUID of the credential                                                                                                                                          |
| **name**             | **str**                                             | credential name                                                                                                                                                     |
| **provider**         | [**CloudProvider**](CloudProvider.md)               |                                                                                                                                                                     |
| **provider_default** | **bool**                                            | True if this is the user&#39;s default credential to be used when connecting to the given cloud provider. There can be at most one default for each unique provider | [optional] |
| **created_at**       | **datetime**                                        | Datetime credentials were created in UTC                                                                                                                            |
| **updated_at**       | **datetime**                                        | Datetime credentials were updated in UTC                                                                                                                            | [optional] |
| **allowed_in_tasks** | **bool**                                            | Is this credential allowed to be used in tasks                                                                                                                      | [optional] |
| **credential**       | [**Credential**](Credential.md)                     |                                                                                                                                                                     | [optional] |
| **role**             | [**AccessCredentialRole**](AccessCredentialRole.md) |                                                                                                                                                                     | [optional] |
| **token**            | [**Token**](Token.md)                               |                                                                                                                                                                     | [optional] |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
