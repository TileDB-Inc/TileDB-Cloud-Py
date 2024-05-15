# GroupActivityLog

Activity of a Group

## Properties

| Name         | Type                                                    | Description                     | Notes      |
| ------------ | ------------------------------------------------------- | ------------------------------- | ---------- |
| **id**       | **str**                                                 | id of the activity              | [optional] |
| **event_at** | **datetime**                                            | time event took place (RFC3339) | [optional] |
| **action**   | [**GroupActivityEventType**](GroupActivityEventType.md) |                                 | [optional] |
| **username** | **str**                                                 | user who performed the action   | [optional] |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
