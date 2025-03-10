# FileListResponse

The result of a list files operation. Compatible with S3's ListObjectResult

## Properties

| Name                        | Type                                      | Description                                                                 | Notes      |
| --------------------------- | ----------------------------------------- | --------------------------------------------------------------------------- | ---------- |
| **name**                    | **str**                                   | The name of the bucket (teamspace) with the objects                         | [optional] |
| **prefix**                  | **str**                                   | The prefix under which objects are listed                                   | [optional] |
| **delimiter**               | **str**                                   | The string that delimits the path segments. Only forward slash is supported | [optional] |
| **max_keys**                | **int**                                   | The maximum amount of objects to return                                     | [optional] |
| **continuation_token**      | **str**                                   | The continuation token that was passed to the operation                     | [optional] |
| **next_continuation_token** | **str**                                   | The continuation token to pass to list the next items                       | [optional] |
| **is_truncated**            | **bool**                                  | Whether there are no more files to list                                     | [optional] |
| **common_prefixes**         | [**list[CommonPrefix]**](CommonPrefix.md) | The common prefixes (folders) contained under prefix.                       | [optional] |
| **objects**                 | [**list[Object]**](Object.md)             | The objects (files) contained under prefix.                                 | [optional] |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
