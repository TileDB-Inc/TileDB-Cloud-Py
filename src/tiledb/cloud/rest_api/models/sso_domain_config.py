# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API

    The version of the OpenAPI document: 2.17.51
    Generated by: https://openapi-generator.tech
"""


import pprint

from tiledb.cloud.rest_api.configuration import Configuration


class SSODomainConfig(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        "uuid": "str",
        "domain": "str",
        "oidc_issuer": "str",
        "oidc_client_id": "str",
        "oidc_client_secret": "str",
        "domain_setup": "SSODomainSetup",
        "verification_status": "DomainVerificationStatus",
        "check_results": "list[DomainCheckResult]",
    }

    attribute_map = {
        "uuid": "uuid",
        "domain": "domain",
        "oidc_issuer": "oidc_issuer",
        "oidc_client_id": "oidc_client_id",
        "oidc_client_secret": "oidc_client_secret",
        "domain_setup": "domain_setup",
        "verification_status": "verification_status",
        "check_results": "check_results",
    }

    def __init__(
        self,
        uuid=None,
        domain=None,
        oidc_issuer=None,
        oidc_client_id=None,
        oidc_client_secret=None,
        domain_setup=None,
        verification_status=None,
        check_results=None,
        local_vars_configuration=None,
    ):
        """SSODomainConfig - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._uuid = None
        self._domain = None
        self._oidc_issuer = None
        self._oidc_client_id = None
        self._oidc_client_secret = None
        self._domain_setup = None
        self._verification_status = None
        self._check_results = None
        self.discriminator = None

        if uuid is not None:
            self.uuid = uuid
        self.domain = domain
        if oidc_issuer is not None:
            self.oidc_issuer = oidc_issuer
        if oidc_client_id is not None:
            self.oidc_client_id = oidc_client_id
        if oidc_client_secret is not None:
            self.oidc_client_secret = oidc_client_secret
        if domain_setup is not None:
            self.domain_setup = domain_setup
        if verification_status is not None:
            self.verification_status = verification_status
        if check_results is not None:
            self.check_results = check_results

    @property
    def uuid(self):
        """Gets the uuid of this SSODomainConfig.

        A server-generated ID for the configuration.

        :return: The uuid of this SSODomainConfig.
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this SSODomainConfig.

        A server-generated ID for the configuration.

        :param uuid: The uuid of this SSODomainConfig.
        :type: str
        """

        self._uuid = uuid

    @property
    def domain(self):
        """Gets the domain of this SSODomainConfig.

        The fully-qualified domain (but with no trailing dot) to connect for single sign-on. This may not be changed after creation.

        :return: The domain of this SSODomainConfig.
        :rtype: str
        """
        return self._domain

    @domain.setter
    def domain(self, domain):
        """Sets the domain of this SSODomainConfig.

        The fully-qualified domain (but with no trailing dot) to connect for single sign-on. This may not be changed after creation.

        :param domain: The domain of this SSODomainConfig.
        :type: str
        """

        self._domain = domain

    @property
    def oidc_issuer(self):
        """Gets the oidc_issuer of this SSODomainConfig.

        The URL of the OpenID Connect issuer that can be used to authenticate this domain's users. The prefix where the `/.well-known/openid-configuration` file can be found; usually without a trailing slash.

        :return: The oidc_issuer of this SSODomainConfig.
        :rtype: str
        """
        return self._oidc_issuer

    @oidc_issuer.setter
    def oidc_issuer(self, oidc_issuer):
        """Sets the oidc_issuer of this SSODomainConfig.

        The URL of the OpenID Connect issuer that can be used to authenticate this domain's users. The prefix where the `/.well-known/openid-configuration` file can be found; usually without a trailing slash.

        :param oidc_issuer: The oidc_issuer of this SSODomainConfig.
        :type: str
        """

        self._oidc_issuer = oidc_issuer

    @property
    def oidc_client_id(self):
        """Gets the oidc_client_id of this SSODomainConfig.

        The OpenID Connect client ID for this SSO instance.

        :return: The oidc_client_id of this SSODomainConfig.
        :rtype: str
        """
        return self._oidc_client_id

    @oidc_client_id.setter
    def oidc_client_id(self, oidc_client_id):
        """Sets the oidc_client_id of this SSODomainConfig.

        The OpenID Connect client ID for this SSO instance.

        :param oidc_client_id: The oidc_client_id of this SSODomainConfig.
        :type: str
        """

        self._oidc_client_id = oidc_client_id

    @property
    def oidc_client_secret(self):
        """Gets the oidc_client_secret of this SSODomainConfig.

        The OpenID Connect client secret for this SSO instance.

        :return: The oidc_client_secret of this SSODomainConfig.
        :rtype: str
        """
        return self._oidc_client_secret

    @oidc_client_secret.setter
    def oidc_client_secret(self, oidc_client_secret):
        """Sets the oidc_client_secret of this SSODomainConfig.

        The OpenID Connect client secret for this SSO instance.

        :param oidc_client_secret: The oidc_client_secret of this SSODomainConfig.
        :type: str
        """

        self._oidc_client_secret = oidc_client_secret

    @property
    def domain_setup(self):
        """Gets the domain_setup of this SSODomainConfig.


        :return: The domain_setup of this SSODomainConfig.
        :rtype: SSODomainSetup
        """
        return self._domain_setup

    @domain_setup.setter
    def domain_setup(self, domain_setup):
        """Sets the domain_setup of this SSODomainConfig.


        :param domain_setup: The domain_setup of this SSODomainConfig.
        :type: SSODomainSetup
        """

        self._domain_setup = domain_setup

    @property
    def verification_status(self):
        """Gets the verification_status of this SSODomainConfig.


        :return: The verification_status of this SSODomainConfig.
        :rtype: DomainVerificationStatus
        """
        return self._verification_status

    @verification_status.setter
    def verification_status(self, verification_status):
        """Sets the verification_status of this SSODomainConfig.


        :param verification_status: The verification_status of this SSODomainConfig.
        :type: DomainVerificationStatus
        """

        self._verification_status = verification_status

    @property
    def check_results(self):
        """Gets the check_results of this SSODomainConfig.

        A list of the results of recent attempts to verify this domain.

        :return: The check_results of this SSODomainConfig.
        :rtype: list[DomainCheckResult]
        """
        return self._check_results

    @check_results.setter
    def check_results(self, check_results):
        """Sets the check_results of this SSODomainConfig.

        A list of the results of recent attempts to verify this domain.

        :param check_results: The check_results of this SSODomainConfig.
        :type: list[DomainCheckResult]
        """

        self._check_results = check_results

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in self.openapi_types.items():
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SSODomainConfig):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SSODomainConfig):
            return True

        return self.to_dict() != other.to_dict()
