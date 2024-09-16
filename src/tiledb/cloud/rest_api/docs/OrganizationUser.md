# OrganizationUser

user in an organization

## Properties

| Name                  | Type                                              | Description                                                 | Notes      |
| --------------------- | ------------------------------------------------- | ----------------------------------------------------------- | ---------- |
| **user_id**           | **str**                                           | unique ID of user                                           | [optional] |
| **organization_id**   | **str**                                           | unique ID of organization                                   | [optional] |
| **username**          | **str**                                           | username for user                                           | [optional] |
| **user_full_name**    | **str**                                           | full name of the user; available to organization admins     | [optional] |
| **user_email**        | **str**                                           | email address of the user; available to organization admins | [optional] |
| **organization_name** | **str**                                           | name of organization                                        | [optional] |
| **role**              | [**OrganizationRoles**](OrganizationRoles.md)     |                                                             | [optional] |
| **allowed_actions**   | [**list[NamespaceActions]**](NamespaceActions.md) | list of actions user is allowed to do on this organization  | [optional] |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
