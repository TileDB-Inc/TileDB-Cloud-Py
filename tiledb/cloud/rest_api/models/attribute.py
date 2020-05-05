# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.0.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class Attribute(object):
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
        "type": "Datatype",
        "filter_pipeline": "FilterPipeline",
        "cell_val_num": "int",
    }

    attribute_map = {
        "name": "name",
        "type": "type",
        "filter_pipeline": "filterPipeline",
        "cell_val_num": "cellValNum",
    }

    def __init__(
        self, name=None, type=None, filter_pipeline=None, cell_val_num=None
    ):  # noqa: E501
        """Attribute - a model defined in OpenAPI"""  # noqa: E501

        self._name = None
        self._type = None
        self._filter_pipeline = None
        self._cell_val_num = None
        self.discriminator = None

        self.name = name
        self.type = type
        self.filter_pipeline = filter_pipeline
        self.cell_val_num = cell_val_num

    @property
    def name(self):
        """Gets the name of this Attribute.  # noqa: E501

        Attribute name  # noqa: E501

        :return: The name of this Attribute.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Attribute.

        Attribute name  # noqa: E501

        :param name: The name of this Attribute.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError(
                "Invalid value for `name`, must not be `None`"
            )  # noqa: E501

        self._name = name

    @property
    def type(self):
        """Gets the type of this Attribute.  # noqa: E501


        :return: The type of this Attribute.  # noqa: E501
        :rtype: Datatype
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Attribute.


        :param type: The type of this Attribute.  # noqa: E501
        :type: Datatype
        """
        if type is None:
            raise ValueError(
                "Invalid value for `type`, must not be `None`"
            )  # noqa: E501

        self._type = type

    @property
    def filter_pipeline(self):
        """Gets the filter_pipeline of this Attribute.  # noqa: E501


        :return: The filter_pipeline of this Attribute.  # noqa: E501
        :rtype: FilterPipeline
        """
        return self._filter_pipeline

    @filter_pipeline.setter
    def filter_pipeline(self, filter_pipeline):
        """Sets the filter_pipeline of this Attribute.


        :param filter_pipeline: The filter_pipeline of this Attribute.  # noqa: E501
        :type: FilterPipeline
        """
        if filter_pipeline is None:
            raise ValueError(
                "Invalid value for `filter_pipeline`, must not be `None`"
            )  # noqa: E501

        self._filter_pipeline = filter_pipeline

    @property
    def cell_val_num(self):
        """Gets the cell_val_num of this Attribute.  # noqa: E501

        Attribute number of values per cell  # noqa: E501

        :return: The cell_val_num of this Attribute.  # noqa: E501
        :rtype: int
        """
        return self._cell_val_num

    @cell_val_num.setter
    def cell_val_num(self, cell_val_num):
        """Sets the cell_val_num of this Attribute.

        Attribute number of values per cell  # noqa: E501

        :param cell_val_num: The cell_val_num of this Attribute.  # noqa: E501
        :type: int
        """
        if cell_val_num is None:
            raise ValueError(
                "Invalid value for `cell_val_num`, must not be `None`"
            )  # noqa: E501

        self._cell_val_num = cell_val_num

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
        if not isinstance(other, Attribute):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
