# coding: utf-8

"""
    Specification file for tiledb-server v4 API

    This spec is exposed to the public under /v4 route group  # noqa: E501

    The version of the OpenAPI document: 0.0.1
    Contact: info@tiledb.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from tiledb.cloud._common.api_v4.configuration import Configuration


class AcademyLesson(object):
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
        "lesson_id": "str",
        "lesson_version": "str",
        "completed": "bool",
        "pinned": "bool",
    }

    attribute_map = {
        "lesson_id": "lesson_id",
        "lesson_version": "lesson_version",
        "completed": "completed",
        "pinned": "pinned",
    }

    def __init__(
        self,
        lesson_id=None,
        lesson_version=None,
        completed=None,
        pinned=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """AcademyLesson - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._lesson_id = None
        self._lesson_version = None
        self._completed = None
        self._pinned = None
        self.discriminator = None

        self.lesson_id = lesson_id
        self.lesson_version = lesson_version
        if completed is not None:
            self.completed = completed
        if pinned is not None:
            self.pinned = pinned

    @property
    def lesson_id(self):
        """Gets the lesson_id of this AcademyLesson.  # noqa: E501

        Unique ID of the lesson  # noqa: E501

        :return: The lesson_id of this AcademyLesson.  # noqa: E501
        :rtype: str
        """
        return self._lesson_id

    @lesson_id.setter
    def lesson_id(self, lesson_id):
        """Sets the lesson_id of this AcademyLesson.

        Unique ID of the lesson  # noqa: E501

        :param lesson_id: The lesson_id of this AcademyLesson.  # noqa: E501
        :type: str
        """
        if (
            self.local_vars_configuration.client_side_validation and lesson_id is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `lesson_id`, must not be `None`"
            )  # noqa: E501

        self._lesson_id = lesson_id

    @property
    def lesson_version(self):
        """Gets the lesson_version of this AcademyLesson.  # noqa: E501

        Version of the lesson  # noqa: E501

        :return: The lesson_version of this AcademyLesson.  # noqa: E501
        :rtype: str
        """
        return self._lesson_version

    @lesson_version.setter
    def lesson_version(self, lesson_version):
        """Sets the lesson_version of this AcademyLesson.

        Version of the lesson  # noqa: E501

        :param lesson_version: The lesson_version of this AcademyLesson.  # noqa: E501
        :type: str
        """
        if (
            self.local_vars_configuration.client_side_validation
            and lesson_version is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `lesson_version`, must not be `None`"
            )  # noqa: E501

        self._lesson_version = lesson_version

    @property
    def completed(self):
        """Gets the completed of this AcademyLesson.  # noqa: E501

        Indicates if lesson is completed  # noqa: E501

        :return: The completed of this AcademyLesson.  # noqa: E501
        :rtype: bool
        """
        return self._completed

    @completed.setter
    def completed(self, completed):
        """Sets the completed of this AcademyLesson.

        Indicates if lesson is completed  # noqa: E501

        :param completed: The completed of this AcademyLesson.  # noqa: E501
        :type: bool
        """

        self._completed = completed

    @property
    def pinned(self):
        """Gets the pinned of this AcademyLesson.  # noqa: E501

        Indicates if lesson is pinned  # noqa: E501

        :return: The pinned of this AcademyLesson.  # noqa: E501
        :rtype: bool
        """
        return self._pinned

    @pinned.setter
    def pinned(self, pinned):
        """Sets the pinned of this AcademyLesson.

        Indicates if lesson is pinned  # noqa: E501

        :param pinned: The pinned of this AcademyLesson.  # noqa: E501
        :type: bool
        """

        self._pinned = pinned

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
        if not isinstance(other, AcademyLesson):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AcademyLesson):
            return True

        return self.to_dict() != other.to_dict()
