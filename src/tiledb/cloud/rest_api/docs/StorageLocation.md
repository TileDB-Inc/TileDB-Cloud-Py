# StorageLocation

The path at which a given asset will be stored, and the credentials used to access that asset. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** | The path to store this asset type. If unset, a suffix of the user&#39;s &#x60;default_s3_path&#x60; is used. When updating, explicitly set to &#x60;\&quot;\&quot;&#x60;, the empty string, to clear this path; leaving it &#x60;null&#x60; (or absent) will leave the path unchanged.  | [optional] 
**credentials_name** | **str** | The name of the credentials used to acess this storage path. If unset, the &#x60;default_s3_path_credentials_name&#x60; is used. When updating, explicitly set to &#x60;\&quot;\&quot;&#x60;, the empty string, to clear this name; leaving it &#x60;null&#x60; (or absent) will leave the name unchanged.  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


