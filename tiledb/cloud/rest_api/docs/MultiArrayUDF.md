# MultiArrayUDF

User-defined function
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**udf_info_name** | **str** | name of UDFInfo to run, format is {namespace}/{udf_name}. Can not be used with exec | [optional] 
**language** | [**UDFLanguage**](UDFLanguage.md) |  | [optional] 
**version** | **str** | Type-specific version | [optional] 
**image_name** | **str** | Docker image name to use for UDF | [optional] 
**_exec** | **str** | Type-specific executable text | [optional] 
**exec_raw** | **str** | optional raw text to store of serialized function, used for showing in UI | [optional] 
**result_format** | [**ResultFormat**](ResultFormat.md) |  | [optional] 
**task_name** | **str** | name of task, optional | [optional] 
**argument** | **str** | Argument(s) to pass to UDF function, tuple or list of args/kwargs which can be in native or JSON format | [optional] 
**stored_param_uuids** | **list[str]** | The UUIDs of stored input parameters (passed in a language-specific format within \&quot;argument\&quot;) to be retrieved from the server-side cache. Serialized in standard hex format with no {}. | [optional] 
**store_results** | **bool** | store results for later retrieval | [optional] 
**dont_download_results** | **bool** | Set to true to avoid downloading the results of this UDF. Useful for intermediate nodes in a task graph where you will not be using the results of your function. Defaults to false (\&quot;yes download results\&quot;). | [optional] 
**ranges** | [**QueryRanges**](QueryRanges.md) |  | [optional] 
**subarray** | [**UDFSubarray**](UDFSubarray.md) |  | [optional] 
**buffers** | **list[str]** | List of buffers to fetch (attributes + dimensions). Deprecated; please set arrays with &#x60;UDFArrayDetails&#x60;. | [optional] 
**arrays** | [**list[UDFArrayDetails]**](UDFArrayDetails.md) | Array ranges/buffer into to run UDF on | [optional] 
**timeout** | **int** | UDF-type timeout in seconds (default: 900) | [optional] 
**task_graph_uuid** | **str** | If set, the ID of the log for the task graph that this was part of.  | [optional] 
**client_node_uuid** | **str** | If set, the client-defined ID of the node within this task&#39;s graph.  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


