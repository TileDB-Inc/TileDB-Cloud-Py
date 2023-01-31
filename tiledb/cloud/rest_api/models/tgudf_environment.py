# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.2.19
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from tiledb.cloud.rest_api.configuration import Configuration


class TGUDFEnvironment(object):
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
        "language": "UDFLanguage",
        "language_version": "str",
        "image_name": "str",
        "namespace": "str",
        "resource_class": "str",
        "resources": "TGUDFEnvironmentResources",
        "run_client_side": "bool",
    }

    attribute_map = {
        "language": "language",
        "language_version": "language_version",
        "image_name": "image_name",
        "namespace": "namespace",
        "resource_class": "resource_class",
        "resources": "resources",
        "run_client_side": "run_client_side",
    }

    def __init__(
        self,
        language=None,
        language_version=None,
        image_name=None,
        namespace=None,
        resource_class=None,
        resources=None,
        run_client_side=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """TGUDFEnvironment - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._language = None
        self._language_version = None
        self._image_name = None
        self._namespace = None
        self._resource_class = None
        self._resources = None
        self._run_client_side = None
        self.discriminator = None

        if language is not None:
            self.language = language
        if language_version is not None:
            self.language_version = language_version
        if image_name is not None:
            self.image_name = image_name
        self.namespace = namespace
        if resource_class is not None:
            self.resource_class = resource_class
        if resources is not None:
            self.resources = resources
        if run_client_side is not None:
            self.run_client_side = run_client_side

    @property
    def language(self):
        """Gets the language of this TGUDFEnvironment.  # noqa: E501


        :return: The language of this TGUDFEnvironment.  # noqa: E501
        :rtype: UDFLanguage
        """
        return self._language

    @language.setter
    def language(self, language):
        """Sets the language of this TGUDFEnvironment.


        :param language: The language of this TGUDFEnvironment.  # noqa: E501
        :type: UDFLanguage
        """

        self._language = language

    @property
    def language_version(self):
        """Gets the language_version of this TGUDFEnvironment.  # noqa: E501

        The language version used to execute this UDF. Neither this nor `language` needs to be set for registered UDFs, since the language and version are stored server-side with the UDF itself.   # noqa: E501

        :return: The language_version of this TGUDFEnvironment.  # noqa: E501
        :rtype: str
        """
        return self._language_version

    @language_version.setter
    def language_version(self, language_version):
        """Sets the language_version of this TGUDFEnvironment.

        The language version used to execute this UDF. Neither this nor `language` needs to be set for registered UDFs, since the language and version are stored server-side with the UDF itself.   # noqa: E501

        :param language_version: The language_version of this TGUDFEnvironment.  # noqa: E501
        :type: str
        """

        self._language_version = language_version

    @property
    def image_name(self):
        """Gets the image_name of this TGUDFEnvironment.  # noqa: E501

        The name of the image to use for the execution environment.   # noqa: E501

        :return: The image_name of this TGUDFEnvironment.  # noqa: E501
        :rtype: str
        """
        return self._image_name

    @image_name.setter
    def image_name(self, image_name):
        """Sets the image_name of this TGUDFEnvironment.

        The name of the image to use for the execution environment.   # noqa: E501

        :param image_name: The image_name of this TGUDFEnvironment.  # noqa: E501
        :type: str
        """

        self._image_name = image_name

    @property
    def namespace(self):
        """Gets the namespace of this TGUDFEnvironment.  # noqa: E501

        If set, the non-default namespace to execute this UDF under (and to query any Array Nodes that are used as inputs to this UDF).   # noqa: E501

        :return: The namespace of this TGUDFEnvironment.  # noqa: E501
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this TGUDFEnvironment.

        If set, the non-default namespace to execute this UDF under (and to query any Array Nodes that are used as inputs to this UDF).   # noqa: E501

        :param namespace: The namespace of this TGUDFEnvironment.  # noqa: E501
        :type: str
        """

        self._namespace = namespace

    @property
    def resource_class(self):
        """Gets the resource_class of this TGUDFEnvironment.  # noqa: E501

        The resource class to use for the UDF execution. Resource classes define resource limits for memory and CPUs. If this is empty, then the UDF will execute in the standard resource class of the TileDB Cloud provider.   # noqa: E501

        :return: The resource_class of this TGUDFEnvironment.  # noqa: E501
        :rtype: str
        """
        return self._resource_class

    @resource_class.setter
    def resource_class(self, resource_class):
        """Sets the resource_class of this TGUDFEnvironment.

        The resource class to use for the UDF execution. Resource classes define resource limits for memory and CPUs. If this is empty, then the UDF will execute in the standard resource class of the TileDB Cloud provider.   # noqa: E501

        :param resource_class: The resource_class of this TGUDFEnvironment.  # noqa: E501
        :type: str
        """

        self._resource_class = resource_class

    @property
    def resources(self):
        """Gets the resources of this TGUDFEnvironment.  # noqa: E501


        :return: The resources of this TGUDFEnvironment.  # noqa: E501
        :rtype: TGUDFEnvironmentResources
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """Sets the resources of this TGUDFEnvironment.


        :param resources: The resources of this TGUDFEnvironment.  # noqa: E501
        :type: TGUDFEnvironmentResources
        """

        self._resources = resources

    @property
    def run_client_side(self):
        """Gets the run_client_side of this TGUDFEnvironment.  # noqa: E501

        A hint that, if possible, this function should be executed on the client side rather than on the server. Registered UDFs and functions which take arrays as inputs can never be executed client-side. If the client’s environment is incompatible, or the client does not support client-side execution, the function will be executed on the server.   # noqa: E501

        :return: The run_client_side of this TGUDFEnvironment.  # noqa: E501
        :rtype: bool
        """
        return self._run_client_side

    @run_client_side.setter
    def run_client_side(self, run_client_side):
        """Sets the run_client_side of this TGUDFEnvironment.

        A hint that, if possible, this function should be executed on the client side rather than on the server. Registered UDFs and functions which take arrays as inputs can never be executed client-side. If the client’s environment is incompatible, or the client does not support client-side execution, the function will be executed on the server.   # noqa: E501

        :param run_client_side: The run_client_side of this TGUDFEnvironment.  # noqa: E501
        :type: bool
        """

        self._run_client_side = run_client_side

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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
        if not isinstance(other, TGUDFEnvironment):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TGUDFEnvironment):
            return True

        return self.to_dict() != other.to_dict()
