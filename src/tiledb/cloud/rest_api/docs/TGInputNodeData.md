# TGInputNodeData

Specifies that a node is an “input value”, allowing for parameterized task graphs. An input node may not depend upon any other nodes. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**default_value** | [**object**](.md) | An argument provided to a node. This is one of a direct value (i.e., a raw JSON value) or a &#x60;TGSentinel&#x60;. For example this Python value:      {\&quot;a\&quot;: [1, \&quot;pipe\&quot;, range(30), None], \&quot;b\&quot;: b\&quot;bytes\&quot;}  is encoded thusly (with included comments):      {  // A dictionary with string keys is JSON-encodable.       \&quot;a\&quot;: [  // As is a list.         1,         \&quot;pipe\&quot;,         {  // A &#x60;range&#x60; is replaced with its pickle.           \&quot;__tdbudf__\&quot;: \&quot;immediate\&quot;,           \&quot;format\&quot;: \&quot;python_pickle\&quot;,           \&quot;base64_data\&quot;: \&quot;gASVIAAAAAAAAACMCGJ1aWx0aW5zlIwFcmFuZ2WUk5RLAEseSwGHlFKULg&#x3D;&#x3D;\&quot;         },         null       ],       \&quot;b\&quot;: {  // Raw binary data is encoded into base64.         \&quot;__tdbudf__\&quot;: \&quot;immediate\&quot;         \&quot;format\&quot;: \&quot;bytes\&quot;,         \&quot;base64_data\&quot;: \&quot;Ynl0ZXM&#x3D;\&quot;       }     }  | [optional] 
**datatype** | **str** | An annotation of what datatype this node is supposed to be. Conventionally, this is a Python-format type annotation, but it’s purely for documentation purposes and not validated.  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


