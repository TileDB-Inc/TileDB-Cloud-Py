# Error

Object containing data about a handled error by REST server

## Properties

| Name                 | Type                                      | Description                                                                                  | Notes      |
| -------------------- | ----------------------------------------- | -------------------------------------------------------------------------------------------- | ---------- |
| **code**             | **int**                                   | A hardcoded integer which points to a specific file/line of the code that returned the error |
| **message**          | **str**                                   | A friendly message to be shown to the client                                                 |
| **request_id**       | **str**                                   | The request id to be used for tracing/debugging                                              |
| **validation_error** | [**ValidationError**](ValidationError.md) |                                                                                              | [optional] |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
