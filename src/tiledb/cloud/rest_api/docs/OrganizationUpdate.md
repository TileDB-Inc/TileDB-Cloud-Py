# OrganizationUpdate

OrganizationUpdate

## Properties

| Name                                 | Type                                    | Description                                                                                                                                                                                  | Notes      |
| ------------------------------------ | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| **name**                             | **str**                                 | organization name must be unique                                                                                                                                                             | [optional] |
| **logo**                             | **str**                                 | Organization logo                                                                                                                                                                            | [optional] |
| **description**                      | **str**                                 | Organization description                                                                                                                                                                     | [optional] |
| **default_s3_path**                  | **str**                                 | The default location to store newly-created notebooks and other assets like UDFs. The name &#x60;default_s3_path&#x60; is a legacy holdover; it may refer to any supported storage location. | [optional] |
| **default_s3_path_credentials_name** | **str**                                 | The name of the credentials used to create and access files in the &#x60;default_s3_path&#x60;, if needed.                                                                                   | [optional] |
| **asset_locations**                  | [**AssetLocations**](AssetLocations.md) |                                                                                                                                                                                              | [optional] |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
