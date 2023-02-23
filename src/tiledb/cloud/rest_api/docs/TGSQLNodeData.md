# TGSQLNodeData

A node specifying an SQL query to execute in TileDB Cloud. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**init_commands** | **list[str]** | The commands to execute before running the query itself. | [optional] 
**query** | **str** | The text of the SQL query to execute. Parameters are substituted in for &#x60;?&#x60;s, just as in a regular MariaDB query.  | [optional] 
**parameters** | **list[object]** | The parameters to substitute in for arguments in the &#x60;query&#x60;. Fixed-length. Arguments must be in JSON format.  | [optional] 
**result_format** | [**ResultFormat**](ResultFormat.md) |  | [optional] 
**namespace** | **str** | If set, the non-default namespace to execute this SQL query under.  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


