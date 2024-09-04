# coding: utf-8

"""
    Tiledb Storage Platform API

    TileDB Storage Platform REST API

    The version of the OpenAPI document: 1.4.0
    Generated by: https://openapi-generator.tech
"""


import pprint

import six

from tiledb.cloud._common.api_v2.configuration import Configuration


class AttributeBufferHeader(object):
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
        "name": "str",
        "fixed_len_buffer_size_in_bytes": "int",
        "var_len_buffer_size_in_bytes": "int",
        "validity_len_buffer_size_in_bytes": "int",
        "original_fixed_len_buffer_size_in_bytes": "int",
        "original_var_len_buffer_size_in_bytes": "int",
        "original_validity_len_buffer_size_in_bytes": "int",
    }

    attribute_map = {
        "name": "name",
        "fixed_len_buffer_size_in_bytes": "fixedLenBufferSizeInBytes",
        "var_len_buffer_size_in_bytes": "varLenBufferSizeInBytes",
        "validity_len_buffer_size_in_bytes": "validityLenBufferSizeInBytes",
        "original_fixed_len_buffer_size_in_bytes": "originalFixedLenBufferSizeInBytes",
        "original_var_len_buffer_size_in_bytes": "originalVarLenBufferSizeInBytes",
        "original_validity_len_buffer_size_in_bytes": "originalValidityLenBufferSizeInBytes",
    }

    def __init__(
        self,
        name=None,
        fixed_len_buffer_size_in_bytes=None,
        var_len_buffer_size_in_bytes=None,
        validity_len_buffer_size_in_bytes=None,
        original_fixed_len_buffer_size_in_bytes=None,
        original_var_len_buffer_size_in_bytes=None,
        original_validity_len_buffer_size_in_bytes=None,
        local_vars_configuration=None,
    ):
        """AttributeBufferHeader - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._fixed_len_buffer_size_in_bytes = None
        self._var_len_buffer_size_in_bytes = None
        self._validity_len_buffer_size_in_bytes = None
        self._original_fixed_len_buffer_size_in_bytes = None
        self._original_var_len_buffer_size_in_bytes = None
        self._original_validity_len_buffer_size_in_bytes = None
        self.discriminator = None

        self.name = name
        self.fixed_len_buffer_size_in_bytes = fixed_len_buffer_size_in_bytes
        self.var_len_buffer_size_in_bytes = var_len_buffer_size_in_bytes
        if validity_len_buffer_size_in_bytes is not None:
            self.validity_len_buffer_size_in_bytes = validity_len_buffer_size_in_bytes
        if original_fixed_len_buffer_size_in_bytes is not None:
            self.original_fixed_len_buffer_size_in_bytes = (
                original_fixed_len_buffer_size_in_bytes
            )
        if original_var_len_buffer_size_in_bytes is not None:
            self.original_var_len_buffer_size_in_bytes = (
                original_var_len_buffer_size_in_bytes
            )
        if original_validity_len_buffer_size_in_bytes is not None:
            self.original_validity_len_buffer_size_in_bytes = (
                original_validity_len_buffer_size_in_bytes
            )

    @property
    def name(self):
        """Gets the name of this AttributeBufferHeader.

        Attribute name

        :return: The name of this AttributeBufferHeader.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this AttributeBufferHeader.

        Attribute name

        :param name: The name of this AttributeBufferHeader.
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def fixed_len_buffer_size_in_bytes(self):
        """Gets the fixed_len_buffer_size_in_bytes of this AttributeBufferHeader.

        Number of bytes in the fixed-length attribute data buffer (offsets for var-len attributes)

        :return: The fixed_len_buffer_size_in_bytes of this AttributeBufferHeader.
        :rtype: int
        """
        return self._fixed_len_buffer_size_in_bytes

    @fixed_len_buffer_size_in_bytes.setter
    def fixed_len_buffer_size_in_bytes(self, fixed_len_buffer_size_in_bytes):
        """Sets the fixed_len_buffer_size_in_bytes of this AttributeBufferHeader.

        Number of bytes in the fixed-length attribute data buffer (offsets for var-len attributes)

        :param fixed_len_buffer_size_in_bytes: The fixed_len_buffer_size_in_bytes of this AttributeBufferHeader.
        :type: int
        """
        if (
            self.local_vars_configuration.client_side_validation
            and fixed_len_buffer_size_in_bytes is None
        ):
            raise ValueError(
                "Invalid value for `fixed_len_buffer_size_in_bytes`, must not be `None`"
            )

        self._fixed_len_buffer_size_in_bytes = fixed_len_buffer_size_in_bytes

    @property
    def var_len_buffer_size_in_bytes(self):
        """Gets the var_len_buffer_size_in_bytes of this AttributeBufferHeader.

        Number of bytes in the var-length attribute data buffer

        :return: The var_len_buffer_size_in_bytes of this AttributeBufferHeader.
        :rtype: int
        """
        return self._var_len_buffer_size_in_bytes

    @var_len_buffer_size_in_bytes.setter
    def var_len_buffer_size_in_bytes(self, var_len_buffer_size_in_bytes):
        """Sets the var_len_buffer_size_in_bytes of this AttributeBufferHeader.

        Number of bytes in the var-length attribute data buffer

        :param var_len_buffer_size_in_bytes: The var_len_buffer_size_in_bytes of this AttributeBufferHeader.
        :type: int
        """
        if (
            self.local_vars_configuration.client_side_validation
            and var_len_buffer_size_in_bytes is None
        ):
            raise ValueError(
                "Invalid value for `var_len_buffer_size_in_bytes`, must not be `None`"
            )

        self._var_len_buffer_size_in_bytes = var_len_buffer_size_in_bytes

    @property
    def validity_len_buffer_size_in_bytes(self):
        """Gets the validity_len_buffer_size_in_bytes of this AttributeBufferHeader.

        Number of bytes for validity in case attribute is nullable

        :return: The validity_len_buffer_size_in_bytes of this AttributeBufferHeader.
        :rtype: int
        """
        return self._validity_len_buffer_size_in_bytes

    @validity_len_buffer_size_in_bytes.setter
    def validity_len_buffer_size_in_bytes(self, validity_len_buffer_size_in_bytes):
        """Sets the validity_len_buffer_size_in_bytes of this AttributeBufferHeader.

        Number of bytes for validity in case attribute is nullable

        :param validity_len_buffer_size_in_bytes: The validity_len_buffer_size_in_bytes of this AttributeBufferHeader.
        :type: int
        """

        self._validity_len_buffer_size_in_bytes = validity_len_buffer_size_in_bytes

    @property
    def original_fixed_len_buffer_size_in_bytes(self):
        """Gets the original_fixed_len_buffer_size_in_bytes of this AttributeBufferHeader.

        Original user set number of bytes in the fixed-length attribute data buffer

        :return: The original_fixed_len_buffer_size_in_bytes of this AttributeBufferHeader.
        :rtype: int
        """
        return self._original_fixed_len_buffer_size_in_bytes

    @original_fixed_len_buffer_size_in_bytes.setter
    def original_fixed_len_buffer_size_in_bytes(
        self, original_fixed_len_buffer_size_in_bytes
    ):
        """Sets the original_fixed_len_buffer_size_in_bytes of this AttributeBufferHeader.

        Original user set number of bytes in the fixed-length attribute data buffer

        :param original_fixed_len_buffer_size_in_bytes: The original_fixed_len_buffer_size_in_bytes of this AttributeBufferHeader.
        :type: int
        """

        self._original_fixed_len_buffer_size_in_bytes = (
            original_fixed_len_buffer_size_in_bytes
        )

    @property
    def original_var_len_buffer_size_in_bytes(self):
        """Gets the original_var_len_buffer_size_in_bytes of this AttributeBufferHeader.

        Original user set number of bytes in the var-length attribute data buffer

        :return: The original_var_len_buffer_size_in_bytes of this AttributeBufferHeader.
        :rtype: int
        """
        return self._original_var_len_buffer_size_in_bytes

    @original_var_len_buffer_size_in_bytes.setter
    def original_var_len_buffer_size_in_bytes(
        self, original_var_len_buffer_size_in_bytes
    ):
        """Sets the original_var_len_buffer_size_in_bytes of this AttributeBufferHeader.

        Original user set number of bytes in the var-length attribute data buffer

        :param original_var_len_buffer_size_in_bytes: The original_var_len_buffer_size_in_bytes of this AttributeBufferHeader.
        :type: int
        """

        self._original_var_len_buffer_size_in_bytes = (
            original_var_len_buffer_size_in_bytes
        )

    @property
    def original_validity_len_buffer_size_in_bytes(self):
        """Gets the original_validity_len_buffer_size_in_bytes of this AttributeBufferHeader.

        Original user set number of bytes in the validity data buffer

        :return: The original_validity_len_buffer_size_in_bytes of this AttributeBufferHeader.
        :rtype: int
        """
        return self._original_validity_len_buffer_size_in_bytes

    @original_validity_len_buffer_size_in_bytes.setter
    def original_validity_len_buffer_size_in_bytes(
        self, original_validity_len_buffer_size_in_bytes
    ):
        """Sets the original_validity_len_buffer_size_in_bytes of this AttributeBufferHeader.

        Original user set number of bytes in the validity data buffer

        :param original_validity_len_buffer_size_in_bytes: The original_validity_len_buffer_size_in_bytes of this AttributeBufferHeader.
        :type: int
        """

        self._original_validity_len_buffer_size_in_bytes = (
            original_validity_len_buffer_size_in_bytes
        )

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
        if not isinstance(other, AttributeBufferHeader):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AttributeBufferHeader):
            return True

        return self.to_dict() != other.to_dict()
