# ArrayTask

Synchronous Task to Run
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | task ID | [optional] 
**name** | **str** | Optional task name | [optional] 
**description** | **str** | Optional task description (Tasks purpose) | [optional] 
**array_metadata** | [**ArrayInfo**](ArrayInfo.md) |  | [optional] 
**subarray** | [**DomainArray**](DomainArray.md) |  | [optional] 
**memory** | **int** | memory allocated to task in bytes | [optional] 
**cpu** | **int** | millicpu allocated to task | [optional] 
**namespace** | **str** | namespace task is tied to | [optional] 
**status** | [**ArrayTaskStatus**](ArrayTaskStatus.md) |  | [optional] 
**start_time** | **datetime** | Start time RFC3339 for job | [optional] 
**finish_time** | **datetime** | Finish time RFC3339 for job | [optional] 
**cost** | **float** | Total accumulated for task in USD, example is $0.12 | [optional] 
**egress_cost** | **float** | Total accumulated for egress task in USD, example is $0.12 | [optional] 
**access_cost** | **float** | Cost accumulated for access task in USD, example is $0.12 | [optional] 
**query_type** | [**Querytype**](Querytype.md) |  | [optional] 
**udf_code** | **str** | Optional actual code that is going to be executed | [optional] 
**udf_language** | **str** | Optional actual language used to express udf_code | [optional] 
**sql_query** | **str** | Optional actual sql query that is going to be executed | [optional] 
**type** | [**ArrayTaskType**](ArrayTaskType.md) |  | [optional] 
**activity** | [**list[ArrayActivityLog]**](ArrayActivityLog.md) | Array activity logs for task | [optional] 
**logs** | **str** | logs from array task | [optional] 
**duration** | **float** | duration in nanoseconds of an array task | [optional] 
**sql_init_commands** | **list[str]** | SQL queries or commands to run before main sql query | [optional] 
**sql_parameters** | **list[object]** | SQL query parameters | [optional] 
**result_format** | [**ResultFormat**](ResultFormat.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


