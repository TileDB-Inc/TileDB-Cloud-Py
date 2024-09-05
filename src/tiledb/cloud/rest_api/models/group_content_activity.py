# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API

    The version of the OpenAPI document: 2.17.51
    Generated by: https://openapi-generator.tech
"""


import pprint

from tiledb.cloud.rest_api.configuration import Configuration


class GroupContentActivity:
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
        "asset": "GroupContentActivityAsset",
        "activity_log": "ArrayActivityLog",
    }

    attribute_map = {"asset": "asset", "activity_log": "activity_log"}

    def __init__(self, asset=None, activity_log=None, local_vars_configuration=None):
        """GroupContentActivity - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._asset = None
        self._activity_log = None
        self.discriminator = None

        if asset is not None:
            self.asset = asset
        if activity_log is not None:
            self.activity_log = activity_log

    @property
    def asset(self):
        """Gets the asset of this GroupContentActivity.


        :return: The asset of this GroupContentActivity.
        :rtype: GroupContentActivityAsset
        """
        return self._asset

    @asset.setter
    def asset(self, asset):
        """Sets the asset of this GroupContentActivity.


        :param asset: The asset of this GroupContentActivity.
        :type: GroupContentActivityAsset
        """

        self._asset = asset

    @property
    def activity_log(self):
        """Gets the activity_log of this GroupContentActivity.


        :return: The activity_log of this GroupContentActivity.
        :rtype: ArrayActivityLog
        """
        return self._activity_log

    @activity_log.setter
    def activity_log(self, activity_log):
        """Sets the activity_log of this GroupContentActivity.


        :param activity_log: The activity_log of this GroupContentActivity.
        :type: ArrayActivityLog
        """

        self._activity_log = activity_log

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
        if not isinstance(other, GroupContentActivity):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GroupContentActivity):
            return True

        return self.to_dict() != other.to_dict()
