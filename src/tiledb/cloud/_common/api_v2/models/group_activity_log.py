# coding: utf-8

"""
    Tiledb Storage Platform API

    TileDB Storage Platform REST API

    The version of the OpenAPI document: 1.4.0
    Generated by: https://openapi-generator.tech
"""


import pprint

from tiledb.cloud._common.api_v2.configuration import Configuration


class GroupActivityLog(object):
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
        "event_at": "datetime",
        "action": "GroupActivityEventType",
        "username": "str",
    }

    attribute_map = {
        "id": "id",
        "event_at": "event_at",
        "action": "action",
        "username": "username",
    }

    def __init__(
        self,
        id=None,
        event_at=None,
        action=None,
        username=None,
        local_vars_configuration=None,
    ):
        """GroupActivityLog - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._event_at = None
        self._action = None
        self._username = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if event_at is not None:
            self.event_at = event_at
        if action is not None:
            self.action = action
        if username is not None:
            self.username = username

    @property
    def id(self):
        """Gets the id of this GroupActivityLog.

        id of the activity

        :return: The id of this GroupActivityLog.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this GroupActivityLog.

        id of the activity

        :param id: The id of this GroupActivityLog.
        :type: str
        """

        self._id = id

    @property
    def event_at(self):
        """Gets the event_at of this GroupActivityLog.

        time event took place (RFC3339)

        :return: The event_at of this GroupActivityLog.
        :rtype: datetime
        """
        return self._event_at

    @event_at.setter
    def event_at(self, event_at):
        """Sets the event_at of this GroupActivityLog.

        time event took place (RFC3339)

        :param event_at: The event_at of this GroupActivityLog.
        :type: datetime
        """

        self._event_at = event_at

    @property
    def action(self):
        """Gets the action of this GroupActivityLog.


        :return: The action of this GroupActivityLog.
        :rtype: GroupActivityEventType
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this GroupActivityLog.


        :param action: The action of this GroupActivityLog.
        :type: GroupActivityEventType
        """

        self._action = action

    @property
    def username(self):
        """Gets the username of this GroupActivityLog.

        user who performed the action

        :return: The username of this GroupActivityLog.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this GroupActivityLog.

        user who performed the action

        :param username: The username of this GroupActivityLog.
        :type: str
        """

        self._username = username

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
        if not isinstance(other, GroupActivityLog):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GroupActivityLog):
            return True

        return self.to_dict() != other.to_dict()
