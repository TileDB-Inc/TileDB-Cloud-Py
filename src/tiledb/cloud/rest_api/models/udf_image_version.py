# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.17.51
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from tiledb.cloud.rest_api.configuration import Configuration


class UDFImageVersion(object):
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
        "id": "str",
        "name": "str",
        "udf_image_uuid": "str",
        "docker_image": "str",
        "version": "float",
        "default": "bool",
        "latest": "bool",
    }

    attribute_map = {
        "id": "id",
        "name": "name",
        "udf_image_uuid": "udf_image_uuid",
        "docker_image": "docker_image",
        "version": "version",
        "default": "default",
        "latest": "latest",
    }

    def __init__(
        self,
        id=None,
        name=None,
        udf_image_uuid=None,
        docker_image=None,
        version=None,
        default=None,
        latest=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """UDFImageVersion - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._udf_image_uuid = None
        self._docker_image = None
        self._version = None
        self._default = None
        self._latest = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if udf_image_uuid is not None:
            self.udf_image_uuid = udf_image_uuid
        if docker_image is not None:
            self.docker_image = docker_image
        if version is not None:
            self.version = version
        if default is not None:
            self.default = default
        if latest is not None:
            self.latest = latest

    @property
    def id(self):
        """Gets the id of this UDFImageVersion.  # noqa: E501

        Unique ID of a versioned image  # noqa: E501

        :return: The id of this UDFImageVersion.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this UDFImageVersion.

        Unique ID of a versioned image  # noqa: E501

        :param id: The id of this UDFImageVersion.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this UDFImageVersion.  # noqa: E501

        name of UDFImageVersion  # noqa: E501

        :return: The name of this UDFImageVersion.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UDFImageVersion.

        name of UDFImageVersion  # noqa: E501

        :param name: The name of this UDFImageVersion.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def udf_image_uuid(self):
        """Gets the udf_image_uuid of this UDFImageVersion.  # noqa: E501

        Unique ID of the UDF image set  # noqa: E501

        :return: The udf_image_uuid of this UDFImageVersion.  # noqa: E501
        :rtype: str
        """
        return self._udf_image_uuid

    @udf_image_uuid.setter
    def udf_image_uuid(self, udf_image_uuid):
        """Sets the udf_image_uuid of this UDFImageVersion.

        Unique ID of the UDF image set  # noqa: E501

        :param udf_image_uuid: The udf_image_uuid of this UDFImageVersion.  # noqa: E501
        :type: str
        """

        self._udf_image_uuid = udf_image_uuid

    @property
    def docker_image(self):
        """Gets the docker_image of this UDFImageVersion.  # noqa: E501

        Uri of docker image related to current entry  # noqa: E501

        :return: The docker_image of this UDFImageVersion.  # noqa: E501
        :rtype: str
        """
        return self._docker_image

    @docker_image.setter
    def docker_image(self, docker_image):
        """Sets the docker_image of this UDFImageVersion.

        Uri of docker image related to current entry  # noqa: E501

        :param docker_image: The docker_image of this UDFImageVersion.  # noqa: E501
        :type: str
        """

        self._docker_image = docker_image

    @property
    def version(self):
        """Gets the version of this UDFImageVersion.  # noqa: E501

        Image-specific version  # noqa: E501

        :return: The version of this UDFImageVersion.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this UDFImageVersion.

        Image-specific version  # noqa: E501

        :param version: The version of this UDFImageVersion.  # noqa: E501
        :type: float
        """

        self._version = version

    @property
    def default(self):
        """Gets the default of this UDFImageVersion.  # noqa: E501

        If current image is default version  # noqa: E501

        :return: The default of this UDFImageVersion.  # noqa: E501
        :rtype: bool
        """
        return self._default

    @default.setter
    def default(self, default):
        """Sets the default of this UDFImageVersion.

        If current image is default version  # noqa: E501

        :param default: The default of this UDFImageVersion.  # noqa: E501
        :type: bool
        """

        self._default = default

    @property
    def latest(self):
        """Gets the latest of this UDFImageVersion.  # noqa: E501

        If current image is latest version  # noqa: E501

        :return: The latest of this UDFImageVersion.  # noqa: E501
        :rtype: bool
        """
        return self._latest

    @latest.setter
    def latest(self, latest):
        """Sets the latest of this UDFImageVersion.

        If current image is latest version  # noqa: E501

        :param latest: The latest of this UDFImageVersion.  # noqa: E501
        :type: bool
        """

        self._latest = latest

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
        if not isinstance(other, UDFImageVersion):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UDFImageVersion):
            return True

        return self.to_dict() != other.to_dict()
