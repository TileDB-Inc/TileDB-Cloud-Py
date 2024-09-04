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


class GenericTileOffsets(object):
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
        "rtree": "float",
        "tile_offsets": "list[float]",
        "tile_var_offsets": "list[float]",
        "tile_var_sizes": "list[float]",
        "tile_validity_offsets": "list[float]",
        "tile_min_offsets": "list[float]",
        "tile_max_offsets": "list[float]",
        "tile_sum_offsets": "list[float]",
        "tile_null_count_offsets": "list[float]",
        "fragment_min_max_sum_null_count_offset": "float",
        "processed_conditions_offsets": "float",
    }

    attribute_map = {
        "rtree": "rtree",
        "tile_offsets": "tileOffsets",
        "tile_var_offsets": "tileVarOffsets",
        "tile_var_sizes": "tileVarSizes",
        "tile_validity_offsets": "tileValidityOffsets",
        "tile_min_offsets": "tileMinOffsets",
        "tile_max_offsets": "tileMaxOffsets",
        "tile_sum_offsets": "tileSumOffsets",
        "tile_null_count_offsets": "tileNullCountOffsets",
        "fragment_min_max_sum_null_count_offset": "fragmentMinMaxSumNullCountOffset",
        "processed_conditions_offsets": "processedConditionsOffsets",
    }

    def __init__(
        self,
        rtree=None,
        tile_offsets=None,
        tile_var_offsets=None,
        tile_var_sizes=None,
        tile_validity_offsets=None,
        tile_min_offsets=None,
        tile_max_offsets=None,
        tile_sum_offsets=None,
        tile_null_count_offsets=None,
        fragment_min_max_sum_null_count_offset=None,
        processed_conditions_offsets=None,
        local_vars_configuration=None,
    ):
        """GenericTileOffsets - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._rtree = None
        self._tile_offsets = None
        self._tile_var_offsets = None
        self._tile_var_sizes = None
        self._tile_validity_offsets = None
        self._tile_min_offsets = None
        self._tile_max_offsets = None
        self._tile_sum_offsets = None
        self._tile_null_count_offsets = None
        self._fragment_min_max_sum_null_count_offset = None
        self._processed_conditions_offsets = None
        self.discriminator = None

        if rtree is not None:
            self.rtree = rtree
        if tile_offsets is not None:
            self.tile_offsets = tile_offsets
        if tile_var_offsets is not None:
            self.tile_var_offsets = tile_var_offsets
        if tile_var_sizes is not None:
            self.tile_var_sizes = tile_var_sizes
        if tile_validity_offsets is not None:
            self.tile_validity_offsets = tile_validity_offsets
        if tile_min_offsets is not None:
            self.tile_min_offsets = tile_min_offsets
        if tile_max_offsets is not None:
            self.tile_max_offsets = tile_max_offsets
        if tile_sum_offsets is not None:
            self.tile_sum_offsets = tile_sum_offsets
        if tile_null_count_offsets is not None:
            self.tile_null_count_offsets = tile_null_count_offsets
        if fragment_min_max_sum_null_count_offset is not None:
            self.fragment_min_max_sum_null_count_offset = (
                fragment_min_max_sum_null_count_offset
            )
        if processed_conditions_offsets is not None:
            self.processed_conditions_offsets = processed_conditions_offsets

    @property
    def rtree(self):
        """Gets the rtree of this GenericTileOffsets.

        RTree serialized as a blob

        :return: The rtree of this GenericTileOffsets.
        :rtype: float
        """
        return self._rtree

    @rtree.setter
    def rtree(self, rtree):
        """Sets the rtree of this GenericTileOffsets.

        RTree serialized as a blob

        :param rtree: The rtree of this GenericTileOffsets.
        :type: float
        """

        self._rtree = rtree

    @property
    def tile_offsets(self):
        """Gets the tile_offsets of this GenericTileOffsets.

        tile offsets

        :return: The tile_offsets of this GenericTileOffsets.
        :rtype: list[float]
        """
        return self._tile_offsets

    @tile_offsets.setter
    def tile_offsets(self, tile_offsets):
        """Sets the tile_offsets of this GenericTileOffsets.

        tile offsets

        :param tile_offsets: The tile_offsets of this GenericTileOffsets.
        :type: list[float]
        """

        self._tile_offsets = tile_offsets

    @property
    def tile_var_offsets(self):
        """Gets the tile_var_offsets of this GenericTileOffsets.

        variable tile offsets

        :return: The tile_var_offsets of this GenericTileOffsets.
        :rtype: list[float]
        """
        return self._tile_var_offsets

    @tile_var_offsets.setter
    def tile_var_offsets(self, tile_var_offsets):
        """Sets the tile_var_offsets of this GenericTileOffsets.

        variable tile offsets

        :param tile_var_offsets: The tile_var_offsets of this GenericTileOffsets.
        :type: list[float]
        """

        self._tile_var_offsets = tile_var_offsets

    @property
    def tile_var_sizes(self):
        """Gets the tile_var_sizes of this GenericTileOffsets.

        sizes of the uncompressed variable tiles offsets

        :return: The tile_var_sizes of this GenericTileOffsets.
        :rtype: list[float]
        """
        return self._tile_var_sizes

    @tile_var_sizes.setter
    def tile_var_sizes(self, tile_var_sizes):
        """Sets the tile_var_sizes of this GenericTileOffsets.

        sizes of the uncompressed variable tiles offsets

        :param tile_var_sizes: The tile_var_sizes of this GenericTileOffsets.
        :type: list[float]
        """

        self._tile_var_sizes = tile_var_sizes

    @property
    def tile_validity_offsets(self):
        """Gets the tile_validity_offsets of this GenericTileOffsets.

        tile validity offsets

        :return: The tile_validity_offsets of this GenericTileOffsets.
        :rtype: list[float]
        """
        return self._tile_validity_offsets

    @tile_validity_offsets.setter
    def tile_validity_offsets(self, tile_validity_offsets):
        """Sets the tile_validity_offsets of this GenericTileOffsets.

        tile validity offsets

        :param tile_validity_offsets: The tile_validity_offsets of this GenericTileOffsets.
        :type: list[float]
        """

        self._tile_validity_offsets = tile_validity_offsets

    @property
    def tile_min_offsets(self):
        """Gets the tile_min_offsets of this GenericTileOffsets.

        min tile offsets

        :return: The tile_min_offsets of this GenericTileOffsets.
        :rtype: list[float]
        """
        return self._tile_min_offsets

    @tile_min_offsets.setter
    def tile_min_offsets(self, tile_min_offsets):
        """Sets the tile_min_offsets of this GenericTileOffsets.

        min tile offsets

        :param tile_min_offsets: The tile_min_offsets of this GenericTileOffsets.
        :type: list[float]
        """

        self._tile_min_offsets = tile_min_offsets

    @property
    def tile_max_offsets(self):
        """Gets the tile_max_offsets of this GenericTileOffsets.

        max tile offsets

        :return: The tile_max_offsets of this GenericTileOffsets.
        :rtype: list[float]
        """
        return self._tile_max_offsets

    @tile_max_offsets.setter
    def tile_max_offsets(self, tile_max_offsets):
        """Sets the tile_max_offsets of this GenericTileOffsets.

        max tile offsets

        :param tile_max_offsets: The tile_max_offsets of this GenericTileOffsets.
        :type: list[float]
        """

        self._tile_max_offsets = tile_max_offsets

    @property
    def tile_sum_offsets(self):
        """Gets the tile_sum_offsets of this GenericTileOffsets.

        tile sum offsets

        :return: The tile_sum_offsets of this GenericTileOffsets.
        :rtype: list[float]
        """
        return self._tile_sum_offsets

    @tile_sum_offsets.setter
    def tile_sum_offsets(self, tile_sum_offsets):
        """Sets the tile_sum_offsets of this GenericTileOffsets.

        tile sum offsets

        :param tile_sum_offsets: The tile_sum_offsets of this GenericTileOffsets.
        :type: list[float]
        """

        self._tile_sum_offsets = tile_sum_offsets

    @property
    def tile_null_count_offsets(self):
        """Gets the tile_null_count_offsets of this GenericTileOffsets.

        null count offsets

        :return: The tile_null_count_offsets of this GenericTileOffsets.
        :rtype: list[float]
        """
        return self._tile_null_count_offsets

    @tile_null_count_offsets.setter
    def tile_null_count_offsets(self, tile_null_count_offsets):
        """Sets the tile_null_count_offsets of this GenericTileOffsets.

        null count offsets

        :param tile_null_count_offsets: The tile_null_count_offsets of this GenericTileOffsets.
        :type: list[float]
        """

        self._tile_null_count_offsets = tile_null_count_offsets

    @property
    def fragment_min_max_sum_null_count_offset(self):
        """Gets the fragment_min_max_sum_null_count_offset of this GenericTileOffsets.

        fragment min/max/sum/nullcount offsets

        :return: The fragment_min_max_sum_null_count_offset of this GenericTileOffsets.
        :rtype: float
        """
        return self._fragment_min_max_sum_null_count_offset

    @fragment_min_max_sum_null_count_offset.setter
    def fragment_min_max_sum_null_count_offset(
        self, fragment_min_max_sum_null_count_offset
    ):
        """Sets the fragment_min_max_sum_null_count_offset of this GenericTileOffsets.

        fragment min/max/sum/nullcount offsets

        :param fragment_min_max_sum_null_count_offset: The fragment_min_max_sum_null_count_offset of this GenericTileOffsets.
        :type: float
        """

        self._fragment_min_max_sum_null_count_offset = (
            fragment_min_max_sum_null_count_offset
        )

    @property
    def processed_conditions_offsets(self):
        """Gets the processed_conditions_offsets of this GenericTileOffsets.

        processed conditions offsets

        :return: The processed_conditions_offsets of this GenericTileOffsets.
        :rtype: float
        """
        return self._processed_conditions_offsets

    @processed_conditions_offsets.setter
    def processed_conditions_offsets(self, processed_conditions_offsets):
        """Sets the processed_conditions_offsets of this GenericTileOffsets.

        processed conditions offsets

        :param processed_conditions_offsets: The processed_conditions_offsets of this GenericTileOffsets.
        :type: float
        """

        self._processed_conditions_offsets = processed_conditions_offsets

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
        if not isinstance(other, GenericTileOffsets):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GenericTileOffsets):
            return True

        return self.to_dict() != other.to_dict()
