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


class ArraySchema(object):
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
        "uri": "str",
        "version": "list[int]",
        "array_type": "ArrayType",
        "tile_order": "Layout",
        "cell_order": "Layout",
        "capacity": "int",
        "coords_filter_pipeline": "FilterPipeline",
        "offset_filter_pipeline": "FilterPipeline",
        "domain": "Domain",
        "attributes": "list[Attribute]",
        "allows_duplicates": "bool",
    }

    attribute_map = {
        "uri": "uri",
        "version": "version",
        "array_type": "arrayType",
        "tile_order": "tileOrder",
        "cell_order": "cellOrder",
        "capacity": "capacity",
        "coords_filter_pipeline": "coordsFilterPipeline",
        "offset_filter_pipeline": "offsetFilterPipeline",
        "domain": "domain",
        "attributes": "attributes",
        "allows_duplicates": "allowsDuplicates",
    }

    def __init__(
        self,
        uri=None,
        version=None,
        array_type=None,
        tile_order=None,
        cell_order=None,
        capacity=None,
        coords_filter_pipeline=None,
        offset_filter_pipeline=None,
        domain=None,
        attributes=None,
        allows_duplicates=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """ArraySchema - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._uri = None
        self._version = None
        self._array_type = None
        self._tile_order = None
        self._cell_order = None
        self._capacity = None
        self._coords_filter_pipeline = None
        self._offset_filter_pipeline = None
        self._domain = None
        self._attributes = None
        self._allows_duplicates = None
        self.discriminator = None

        if uri is not None:
            self.uri = uri
        self.version = version
        self.array_type = array_type
        self.tile_order = tile_order
        self.cell_order = cell_order
        self.capacity = capacity
        self.coords_filter_pipeline = coords_filter_pipeline
        self.offset_filter_pipeline = offset_filter_pipeline
        self.domain = domain
        self.attributes = attributes
        if allows_duplicates is not None:
            self.allows_duplicates = allows_duplicates

    @property
    def uri(self):
        """Gets the uri of this ArraySchema.  # noqa: E501

        URI of schema  # noqa: E501

        :return: The uri of this ArraySchema.  # noqa: E501
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """Sets the uri of this ArraySchema.

        URI of schema  # noqa: E501

        :param uri: The uri of this ArraySchema.  # noqa: E501
        :type: str
        """

        self._uri = uri

    @property
    def version(self):
        """Gets the version of this ArraySchema.  # noqa: E501

        file format version  # noqa: E501

        :return: The version of this ArraySchema.  # noqa: E501
        :rtype: list[int]
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ArraySchema.

        file format version  # noqa: E501

        :param version: The version of this ArraySchema.  # noqa: E501
        :type: list[int]
        """
        if (
            self.local_vars_configuration.client_side_validation and version is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `version`, must not be `None`"
            )  # noqa: E501

        self._version = version

    @property
    def array_type(self):
        """Gets the array_type of this ArraySchema.  # noqa: E501


        :return: The array_type of this ArraySchema.  # noqa: E501
        :rtype: ArrayType
        """
        return self._array_type

    @array_type.setter
    def array_type(self, array_type):
        """Sets the array_type of this ArraySchema.


        :param array_type: The array_type of this ArraySchema.  # noqa: E501
        :type: ArrayType
        """
        if (
            self.local_vars_configuration.client_side_validation and array_type is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `array_type`, must not be `None`"
            )  # noqa: E501

        self._array_type = array_type

    @property
    def tile_order(self):
        """Gets the tile_order of this ArraySchema.  # noqa: E501


        :return: The tile_order of this ArraySchema.  # noqa: E501
        :rtype: Layout
        """
        return self._tile_order

    @tile_order.setter
    def tile_order(self, tile_order):
        """Sets the tile_order of this ArraySchema.


        :param tile_order: The tile_order of this ArraySchema.  # noqa: E501
        :type: Layout
        """
        if (
            self.local_vars_configuration.client_side_validation and tile_order is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `tile_order`, must not be `None`"
            )  # noqa: E501

        self._tile_order = tile_order

    @property
    def cell_order(self):
        """Gets the cell_order of this ArraySchema.  # noqa: E501


        :return: The cell_order of this ArraySchema.  # noqa: E501
        :rtype: Layout
        """
        return self._cell_order

    @cell_order.setter
    def cell_order(self, cell_order):
        """Sets the cell_order of this ArraySchema.


        :param cell_order: The cell_order of this ArraySchema.  # noqa: E501
        :type: Layout
        """
        if (
            self.local_vars_configuration.client_side_validation and cell_order is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `cell_order`, must not be `None`"
            )  # noqa: E501

        self._cell_order = cell_order

    @property
    def capacity(self):
        """Gets the capacity of this ArraySchema.  # noqa: E501

        Capacity of array  # noqa: E501

        :return: The capacity of this ArraySchema.  # noqa: E501
        :rtype: int
        """
        return self._capacity

    @capacity.setter
    def capacity(self, capacity):
        """Sets the capacity of this ArraySchema.

        Capacity of array  # noqa: E501

        :param capacity: The capacity of this ArraySchema.  # noqa: E501
        :type: int
        """
        if (
            self.local_vars_configuration.client_side_validation and capacity is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `capacity`, must not be `None`"
            )  # noqa: E501

        self._capacity = capacity

    @property
    def coords_filter_pipeline(self):
        """Gets the coords_filter_pipeline of this ArraySchema.  # noqa: E501


        :return: The coords_filter_pipeline of this ArraySchema.  # noqa: E501
        :rtype: FilterPipeline
        """
        return self._coords_filter_pipeline

    @coords_filter_pipeline.setter
    def coords_filter_pipeline(self, coords_filter_pipeline):
        """Sets the coords_filter_pipeline of this ArraySchema.


        :param coords_filter_pipeline: The coords_filter_pipeline of this ArraySchema.  # noqa: E501
        :type: FilterPipeline
        """
        if (
            self.local_vars_configuration.client_side_validation
            and coords_filter_pipeline is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `coords_filter_pipeline`, must not be `None`"
            )  # noqa: E501

        self._coords_filter_pipeline = coords_filter_pipeline

    @property
    def offset_filter_pipeline(self):
        """Gets the offset_filter_pipeline of this ArraySchema.  # noqa: E501


        :return: The offset_filter_pipeline of this ArraySchema.  # noqa: E501
        :rtype: FilterPipeline
        """
        return self._offset_filter_pipeline

    @offset_filter_pipeline.setter
    def offset_filter_pipeline(self, offset_filter_pipeline):
        """Sets the offset_filter_pipeline of this ArraySchema.


        :param offset_filter_pipeline: The offset_filter_pipeline of this ArraySchema.  # noqa: E501
        :type: FilterPipeline
        """
        if (
            self.local_vars_configuration.client_side_validation
            and offset_filter_pipeline is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `offset_filter_pipeline`, must not be `None`"
            )  # noqa: E501

        self._offset_filter_pipeline = offset_filter_pipeline

    @property
    def domain(self):
        """Gets the domain of this ArraySchema.  # noqa: E501


        :return: The domain of this ArraySchema.  # noqa: E501
        :rtype: Domain
        """
        return self._domain

    @domain.setter
    def domain(self, domain):
        """Sets the domain of this ArraySchema.


        :param domain: The domain of this ArraySchema.  # noqa: E501
        :type: Domain
        """
        if (
            self.local_vars_configuration.client_side_validation and domain is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `domain`, must not be `None`"
            )  # noqa: E501

        self._domain = domain

    @property
    def attributes(self):
        """Gets the attributes of this ArraySchema.  # noqa: E501

        Attributes of array  # noqa: E501

        :return: The attributes of this ArraySchema.  # noqa: E501
        :rtype: list[Attribute]
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """Sets the attributes of this ArraySchema.

        Attributes of array  # noqa: E501

        :param attributes: The attributes of this ArraySchema.  # noqa: E501
        :type: list[Attribute]
        """
        if (
            self.local_vars_configuration.client_side_validation and attributes is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `attributes`, must not be `None`"
            )  # noqa: E501

        self._attributes = attributes

    @property
    def allows_duplicates(self):
        """Gets the allows_duplicates of this ArraySchema.  # noqa: E501

        True if the array allows coordinate duplicates. Applicable only to sparse arrays.  # noqa: E501

        :return: The allows_duplicates of this ArraySchema.  # noqa: E501
        :rtype: bool
        """
        return self._allows_duplicates

    @allows_duplicates.setter
    def allows_duplicates(self, allows_duplicates):
        """Sets the allows_duplicates of this ArraySchema.

        True if the array allows coordinate duplicates. Applicable only to sparse arrays.  # noqa: E501

        :param allows_duplicates: The allows_duplicates of this ArraySchema.  # noqa: E501
        :type: bool
        """

        self._allows_duplicates = allows_duplicates

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
        if not isinstance(other, ArraySchema):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ArraySchema):
            return True

        return self.to_dict() != other.to_dict()
