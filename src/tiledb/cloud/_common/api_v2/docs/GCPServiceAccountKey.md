# GCPServiceAccountKey

The key to a Google Cloud Platform service account.

## Properties

| Name           | Type    | Description                                                                                                                                                                                                                            | Notes      |
| -------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| **account_id** | **str** | The ID of the service account (i.e., its email address). This is ignored when uploading key information, and is only provided by the server when downloading metadata about an existing key.                                           | [optional] |
| **key_id**     | **str** | The ID of the particular key. This identifies it among other keys issued for this service account. This is ignored when uploading key information, and is only provided by the server when downloading metadata about an existing key. | [optional] |
| **key_text**   | **str** | The full file provided by Google Cloud. This is usually in the form of a JSON document, but TileDB Cloud treats it as opaque (except to attempt to extract the service account ID and the key ID).                                     | [optional] |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
