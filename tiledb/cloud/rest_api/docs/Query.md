# Query


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | [**Querytype**](Querytype.md) |  | 
**layout** | [**Layout**](Layout.md) |  | 
**status** | [**Querystatus**](Querystatus.md) |  | 
**attribute_buffer_headers** | [**[AttributeBufferHeader]**](AttributeBufferHeader.md) | List of attribute buffer headers | 
**array** | [**Array**](Array.md) |  | 
**total_fixed_length_buffer_bytes** | **int** | Total number of bytes in fixed size attribute buffers. | 
**total_var_len_buffer_bytes** | **int** | Total number of bytes in variable size attribute buffers. | 
**writer** | [**Writer**](Writer.md) |  | [optional] 
**reader** | [**QueryReader**](QueryReader.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


