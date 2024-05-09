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


class Query(object):
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
        "type": "Querytype",
        "layout": "Layout",
        "status": "Querystatus",
        "attribute_buffer_headers": "list[AttributeBufferHeader]",
        "writer": "Writer",
        "reader": "QueryReader",
        "array": "Array",
        "total_fixed_length_buffer_bytes": "int",
        "total_var_len_buffer_bytes": "int",
    }

    attribute_map = {
        "type": "type",
        "layout": "layout",
        "status": "status",
        "attribute_buffer_headers": "attributeBufferHeaders",
        "writer": "writer",
        "reader": "reader",
        "array": "array",
        "total_fixed_length_buffer_bytes": "totalFixedLengthBufferBytes",
        "total_var_len_buffer_bytes": "totalVarLenBufferBytes",
    }

    def __init__(
        self,
        type=None,
        layout=None,
        status=None,
        attribute_buffer_headers=None,
        writer=None,
        reader=None,
        array=None,
        total_fixed_length_buffer_bytes=None,
        total_var_len_buffer_bytes=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """Query - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._type = None
        self._layout = None
        self._status = None
        self._attribute_buffer_headers = None
        self._writer = None
        self._reader = None
        self._array = None
        self._total_fixed_length_buffer_bytes = None
        self._total_var_len_buffer_bytes = None
        self.discriminator = None

        self.type = type
        self.layout = layout
        self.status = status
        self.attribute_buffer_headers = attribute_buffer_headers
        if writer is not None:
            self.writer = writer
        if reader is not None:
            self.reader = reader
        self.array = array
        self.total_fixed_length_buffer_bytes = total_fixed_length_buffer_bytes
        self.total_var_len_buffer_bytes = total_var_len_buffer_bytes

    @property
    def type(self):
        """Gets the type of this Query.  # noqa: E501


        :return: The type of this Query.  # noqa: E501
        :rtype: Querytype
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Query.


        :param type: The type of this Query.  # noqa: E501
        :type: Querytype
        """
        if (
            self.local_vars_configuration.client_side_validation and type is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `type`, must not be `None`"
            )  # noqa: E501

        self._type = type

    @property
    def layout(self):
        """Gets the layout of this Query.  # noqa: E501


        :return: The layout of this Query.  # noqa: E501
        :rtype: Layout
        """
        return self._layout

    @layout.setter
    def layout(self, layout):
        """Sets the layout of this Query.


        :param layout: The layout of this Query.  # noqa: E501
        :type: Layout
        """
        if (
            self.local_vars_configuration.client_side_validation and layout is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `layout`, must not be `None`"
            )  # noqa: E501

        self._layout = layout

    @property
    def status(self):
        """Gets the status of this Query.  # noqa: E501


        :return: The status of this Query.  # noqa: E501
        :rtype: Querystatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Query.


        :param status: The status of this Query.  # noqa: E501
        :type: Querystatus
        """
        if (
            self.local_vars_configuration.client_side_validation and status is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `status`, must not be `None`"
            )  # noqa: E501

        self._status = status

    @property
    def attribute_buffer_headers(self):
        """Gets the attribute_buffer_headers of this Query.  # noqa: E501

        List of attribute buffer headers  # noqa: E501

        :return: The attribute_buffer_headers of this Query.  # noqa: E501
        :rtype: list[AttributeBufferHeader]
        """
        return self._attribute_buffer_headers

    @attribute_buffer_headers.setter
    def attribute_buffer_headers(self, attribute_buffer_headers):
        """Sets the attribute_buffer_headers of this Query.

        List of attribute buffer headers  # noqa: E501

        :param attribute_buffer_headers: The attribute_buffer_headers of this Query.  # noqa: E501
        :type: list[AttributeBufferHeader]
        """
        if (
            self.local_vars_configuration.client_side_validation
            and attribute_buffer_headers is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `attribute_buffer_headers`, must not be `None`"
            )  # noqa: E501

        self._attribute_buffer_headers = attribute_buffer_headers

    @property
    def writer(self):
        """Gets the writer of this Query.  # noqa: E501


        :return: The writer of this Query.  # noqa: E501
        :rtype: Writer
        """
        return self._writer

    @writer.setter
    def writer(self, writer):
        """Sets the writer of this Query.


        :param writer: The writer of this Query.  # noqa: E501
        :type: Writer
        """

        self._writer = writer

    @property
    def reader(self):
        """Gets the reader of this Query.  # noqa: E501


        :return: The reader of this Query.  # noqa: E501
        :rtype: QueryReader
        """
        return self._reader

    @reader.setter
    def reader(self, reader):
        """Sets the reader of this Query.


        :param reader: The reader of this Query.  # noqa: E501
        :type: QueryReader
        """

        self._reader = reader

    @property
    def array(self):
        """Gets the array of this Query.  # noqa: E501


        :return: The array of this Query.  # noqa: E501
        :rtype: Array
        """
        return self._array

    @array.setter
    def array(self, array):
        """Sets the array of this Query.


        :param array: The array of this Query.  # noqa: E501
        :type: Array
        """
        if (
            self.local_vars_configuration.client_side_validation and array is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `array`, must not be `None`"
            )  # noqa: E501

        self._array = array

    @property
    def total_fixed_length_buffer_bytes(self):
        """Gets the total_fixed_length_buffer_bytes of this Query.  # noqa: E501

        Total number of bytes in fixed size attribute buffers.  # noqa: E501

        :return: The total_fixed_length_buffer_bytes of this Query.  # noqa: E501
        :rtype: int
        """
        return self._total_fixed_length_buffer_bytes

    @total_fixed_length_buffer_bytes.setter
    def total_fixed_length_buffer_bytes(self, total_fixed_length_buffer_bytes):
        """Sets the total_fixed_length_buffer_bytes of this Query.

        Total number of bytes in fixed size attribute buffers.  # noqa: E501

        :param total_fixed_length_buffer_bytes: The total_fixed_length_buffer_bytes of this Query.  # noqa: E501
        :type: int
        """
        if (
            self.local_vars_configuration.client_side_validation
            and total_fixed_length_buffer_bytes is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `total_fixed_length_buffer_bytes`, must not be `None`"
            )  # noqa: E501

        self._total_fixed_length_buffer_bytes = total_fixed_length_buffer_bytes

    @property
    def total_var_len_buffer_bytes(self):
        """Gets the total_var_len_buffer_bytes of this Query.  # noqa: E501

        Total number of bytes in variable size attribute buffers.  # noqa: E501

        :return: The total_var_len_buffer_bytes of this Query.  # noqa: E501
        :rtype: int
        """
        return self._total_var_len_buffer_bytes

    @total_var_len_buffer_bytes.setter
    def total_var_len_buffer_bytes(self, total_var_len_buffer_bytes):
        """Sets the total_var_len_buffer_bytes of this Query.

        Total number of bytes in variable size attribute buffers.  # noqa: E501

        :param total_var_len_buffer_bytes: The total_var_len_buffer_bytes of this Query.  # noqa: E501
        :type: int
        """
        if (
            self.local_vars_configuration.client_side_validation
            and total_var_len_buffer_bytes is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `total_var_len_buffer_bytes`, must not be `None`"
            )  # noqa: E501

        self._total_var_len_buffer_bytes = total_var_len_buffer_bytes

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
        if not isinstance(other, Query):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Query):
            return True

        return self.to_dict() != other.to_dict()
