# SSODomainConfig

The information used to set up a single-sign on connection to a customer domain.

## Properties

| Name                    | Type                                                        | Description                                                                                                                                                                                                            | Notes      |
| ----------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| **uuid**                | **str**                                                     | A server-generated ID for the configuration.                                                                                                                                                                           | [optional] |
| **domain**              | **str**                                                     | The fully-qualified domain (but with no trailing dot) to connect for single sign-on. This may not be changed after creation.                                                                                           | [optional] |
| **oidc_issuer**         | **str**                                                     | The URL of the OpenID Connect issuer that can be used to authenticate this domain&#39;s users. The prefix where the &#x60;/.well-known/openid-configuration&#x60; file can be found; usually without a trailing slash. | [optional] |
| **oidc_client_id**      | **str**                                                     | The OpenID Connect client ID for this SSO instance.                                                                                                                                                                    | [optional] |
| **oidc_client_secret**  | **str**                                                     | The OpenID Connect client secret for this SSO instance.                                                                                                                                                                | [optional] |
| **domain_setup**        | [**SSODomainSetup**](SSODomainSetup.md)                     |                                                                                                                                                                                                                        | [optional] |
| **verification_status** | [**DomainVerificationStatus**](DomainVerificationStatus.md) |                                                                                                                                                                                                                        | [optional] |
| **check_results**       | [**list[DomainCheckResult]**](DomainCheckResult.md)         | A list of the results of recent attempts to verify this domain.                                                                                                                                                        | [optional] |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
