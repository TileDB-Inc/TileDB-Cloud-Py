# User

object for a registered user

## Properties

| Name               | Type                        | Description                           | Notes      |
| ------------------ | --------------------------- | ------------------------------------- | ---------- |
| **id**             | **str**                     | The user&#39;s ID                     |
| **display_name**   | **str**                     | display name of the user              |
| **image_id**       | **str**                     | The image&#39;s ID                    | [optional] |
| **email**          | **str**                     | user email                            |
| **is_valid_email** | **bool**                    | if a user has validated their email   | [optional] |
| **role**           | [**UserRole**](UserRole.md) |                                       |
| **username**       | **str**                     | user email                            |
| **timezone**       | **str**                     | user timezone                         |
| **created_at**     | **datetime**                | Datetime workspace was created in UTC |
| **updated_at**     | **datetime**                | Datetime workspace was updated in UTC | [optional] |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
