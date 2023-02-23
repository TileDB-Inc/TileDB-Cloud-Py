# TGUDFNodeData

A node specifying the execution of a user-defined function.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**registered_udf_name** | **str** | If set, the name of the registered UDF to execute, in the format &#x60;namespace/name&#x60;. Either this or &#x60;executable_code&#x60; should be set, but not both.  | [optional] 
**executable_code** | **str** | If set, the base64 serialization of the code for this step, encoded in a language-specific format (e.g. Pickle for Python, serialization for R).  | [optional] 
**source_text** | **str** | Optionally, the source text for the code passed in &#x60;executable_code&#x60;. *For reference only; only the code in &#x60;executable_code&#x60; is actually executed.* This will be included in activity logs and may be useful for debugging.  | [optional] 
**environment** | [**TGUDFEnvironment**](TGUDFEnvironment.md) |  | [optional] 
**arguments** | [**list[TGUDFArgument]**](TGUDFArgument.md) | The arguments to a UDF function. This encompasses both named and positional arguments. The format is designed to provide compatibility across languages like Python which have a fairly traditional split between positional arguments and named arguments, and languages like R which has a rather unique way of specifying arguments. For Python (and most other languages), all positional arguments will come before all named arguments (if any are present):      // fn(arg1, arg2, arg3)     [       {value: arg1},       {value: arg2},       {value: arg3},     ]     // fn(arg1, arg2, n&#x3D;kw1, a&#x3D;kw2)     [       {value: arg1},       {value: arg2},       {name: \&quot;n\&quot;, value: kw1},       {name: \&quot;a\&quot;, value: kw2},     ]     // fn(kw&#x3D;k1, only&#x3D;k2)     [       {name: \&quot;kw\&quot;, value: k1},       {name: \&quot;only\&quot;, value: k2},     ]  However, in R, named and positional arguments may be intermixed freely:      // fn(arg, n&#x3D;kw1, arg2)     [       {value: arg},       {name: \&quot;n\&quot;, value: kw1},       {value: arg2},     ]  | [optional] 
**result_format** | [**ResultFormat**](ResultFormat.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


