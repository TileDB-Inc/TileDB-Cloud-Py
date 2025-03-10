# CredentialUpdateRequest

The credential update object

## Properties

| Name                 | Type                                                | Description                                                                                                                                                         | Notes      |
| -------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| **name**             | **str**                                             | A user-specified name for the key                                                                                                                                   | [optional] |
| **provider_default** | **bool**                                            | True if this is the user&#39;s default credential to be used when connecting to the given cloud provider. There can be at most one default for each unique provider | [optional] |
| **provider**         | [**CloudProvider**](CloudProvider.md)               |                                                                                                                                                                     | [optional] |
| **allowed_in_tasks** | **bool**                                            | Is this credential allowed to be used in tasks                                                                                                                      | [optional] |
| **credential**       | [**Credential**](Credential.md)                     |                                                                                                                                                                     | [optional] |
| **role**             | [**AccessCredentialRole**](AccessCredentialRole.md) |                                                                                                                                                                     | [optional] |
| **token**            | [**Token**](Token.md)                               |                                                                                                                                                                     | [optional] |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
