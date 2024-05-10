# NotebookStatus

Status details of a notebook server

## Properties

| Name              | Type                          | Description                                   | Notes      |
| ----------------- | ----------------------------- | --------------------------------------------- | ---------- |
| **namespace**     | **str**                       | namespace of notebook                         | [optional] |
| **uptime**        | **int**                       | duration notebook has been running in seconds | [optional] |
| **cpu_usage**     | **int**                       | current cpu usage in millicpu                 | [optional] |
| **gpu_usage**     | **int**                       | gpu usage in milligpu                         | [optional] |
| **memory_usage**  | **int**                       | memory usage in bytes                         | [optional] |
| **gpu_limit**     | **int**                       | gpu limit in milligpu                         | [optional] |
| **memory_limit**  | **int**                       | memory allocated to notebook server in bytes  | [optional] |
| **storage_usage** | **int**                       | storage usage in bytes                        | [optional] |
| **storage_limit** | **int**                       | storage allocated to notebook server in bytes | [optional] |
| **cpu_count**     | **int**                       | millicpu allocated to notebook server         | [optional] |
| **cost**          | **float**                     | cost in USD for the current notebook session  | [optional] |
| **pod_status**    | [**PodStatus**](PodStatus.md) |                                               | [optional] |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
