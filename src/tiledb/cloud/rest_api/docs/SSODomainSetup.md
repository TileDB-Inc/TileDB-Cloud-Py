# SSODomainSetup

Configuration settings to verify ownership of a given domain. At least one of these must be completed enable user login from the domain.

## Properties

| Name          | Type    | Description                                     | Notes      |
| ------------- | ------- | ----------------------------------------------- | ---------- |
| **txt**       | **str** | a DNS TXT record to set on the domain to claim. | [optional] |
| **cname_src** | **str** | a DNS name to set a CNAME record on             | [optional] |
| **cname_dst** | **str** | the CNAME target of &#x60;cname_src&#x60;.      | [optional] |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
