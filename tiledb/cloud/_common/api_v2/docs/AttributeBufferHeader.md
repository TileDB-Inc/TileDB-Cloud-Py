# AttributeBufferHeader

Represents an attribute buffer header information
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Attribute name | 
**fixed_len_buffer_size_in_bytes** | **int** | Number of bytes in the fixed-length attribute data buffer (offsets for var-len attributes) | 
**var_len_buffer_size_in_bytes** | **int** | Number of bytes in the var-length attribute data buffer | 
**validity_len_buffer_size_in_bytes** | **int** | Number of bytes for validity in case attribute is nullable | [optional] 
**original_fixed_len_buffer_size_in_bytes** | **int** | Original user set number of bytes in the fixed-length attribute data buffer | [optional] 
**original_var_len_buffer_size_in_bytes** | **int** | Original user set number of bytes in the var-length attribute data buffer | [optional] 
**original_validity_len_buffer_size_in_bytes** | **int** | Original user set number of bytes in the validity data buffer | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


