# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 1.5.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class GenericUDF(object):
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
        "type": "UDFType",
        "version": "str",
        "image_name": "str",
        "_exec": "str",
        "argument": "str",
        "result_format": "UDFResultType",
    }

    attribute_map = {
        "type": "type",
        "version": "version",
        "image_name": "image_name",
        "_exec": "exec",
        "argument": "argument",
        "result_format": "result_format",
    }

    def __init__(
        self,
        type=None,
        version=None,
        image_name=None,
        _exec=None,
        argument=None,
        result_format=None,
    ):  # noqa: E501
        """GenericUDF - a model defined in OpenAPI"""  # noqa: E501

        self._type = None
        self._version = None
        self._image_name = None
        self.__exec = None
        self._argument = None
        self._result_format = None
        self.discriminator = None

        if type is not None:
            self.type = type
        if version is not None:
            self.version = version
        if image_name is not None:
            self.image_name = image_name
        if _exec is not None:
            self._exec = _exec
        if argument is not None:
            self.argument = argument
        if result_format is not None:
            self.result_format = result_format

    @property
    def type(self):
        """Gets the type of this GenericUDF.  # noqa: E501


        :return: The type of this GenericUDF.  # noqa: E501
        :rtype: UDFType
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this GenericUDF.


        :param type: The type of this GenericUDF.  # noqa: E501
        :type: UDFType
        """

        self._type = type

    @property
    def version(self):
        """Gets the version of this GenericUDF.  # noqa: E501

        Type-specific version  # noqa: E501

        :return: The version of this GenericUDF.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this GenericUDF.

        Type-specific version  # noqa: E501

        :param version: The version of this GenericUDF.  # noqa: E501
        :type: str
        """

        self._version = version

    @property
    def image_name(self):
        """Gets the image_name of this GenericUDF.  # noqa: E501

        Docker image name to use for udf  # noqa: E501

        :return: The image_name of this GenericUDF.  # noqa: E501
        :rtype: str
        """
        return self._image_name

    @image_name.setter
    def image_name(self, image_name):
        """Sets the image_name of this GenericUDF.

        Docker image name to use for udf  # noqa: E501

        :param image_name: The image_name of this GenericUDF.  # noqa: E501
        :type: str
        """

        self._image_name = image_name

    @property
    def _exec(self):
        """Gets the _exec of this GenericUDF.  # noqa: E501

        Type-specific executable text  # noqa: E501

        :return: The _exec of this GenericUDF.  # noqa: E501
        :rtype: str
        """
        return self.__exec

    @_exec.setter
    def _exec(self, _exec):
        """Sets the _exec of this GenericUDF.

        Type-specific executable text  # noqa: E501

        :param _exec: The _exec of this GenericUDF.  # noqa: E501
        :type: str
        """

        self.__exec = _exec

    @property
    def argument(self):
        """Gets the argument of this GenericUDF.  # noqa: E501

        Argument to pass to udf function  # noqa: E501

        :return: The argument of this GenericUDF.  # noqa: E501
        :rtype: str
        """
        return self._argument

    @argument.setter
    def argument(self, argument):
        """Sets the argument of this GenericUDF.

        Argument to pass to udf function  # noqa: E501

        :param argument: The argument of this GenericUDF.  # noqa: E501
        :type: str
        """

        self._argument = argument

    @property
    def result_format(self):
        """Gets the result_format of this GenericUDF.  # noqa: E501


        :return: The result_format of this GenericUDF.  # noqa: E501
        :rtype: UDFResultType
        """
        return self._result_format

    @result_format.setter
    def result_format(self, result_format):
        """Sets the result_format of this GenericUDF.


        :param result_format: The result_format of this GenericUDF.  # noqa: E501
        :type: UDFResultType
        """

        self._result_format = result_format

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
        if not isinstance(other, GenericUDF):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
