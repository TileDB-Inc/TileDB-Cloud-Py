# RetryStrategy

RetryStrategy provides controls on how to retry a taskgraph node

## Properties

| Name             | Type                              | Description                                                                                                                                                                              | Notes      |
| ---------------- | --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| **backoff**      | [**Backoff**](Backoff.md)         |                                                                                                                                                                                          | [optional] |
| **expression**   | **str**                           | Expression is a condition expression for when a node will be retried. If it evaluates to false, the node will not be retried and the retry strategy will be ignored                      | [optional] |
| **limit**        | **int**                           | Limit is the maximum number of retry attempts when retrying a container. It does not include the original container; the maximum number of total attempts will be &#x60;limit + 1&#x60;. | [optional] |
| **retry_policy** | [**RetryPolicy**](RetryPolicy.md) |                                                                                                                                                                                          | [optional] |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
