# coding: utf-8

"""
    Tiledb Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 1.4.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from tiledb.cloud._common.api_v2.configuration import Configuration


class Array(object):
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
        "query_type": "Querytype",
        "uri": "str",
        "end_timestamp": "float",
        "start_timestamp": "float",
        "array_schema_latest": "ArraySchema",
        "array_schemas_all": "ArraySchemaMap",
        "array_metadata": "ArrayMetadata",
        "non_empty_domain": "NonEmptyDomainList",
        "array_directory": "ArrayDirectory",
        "fragment_metadata_all": "list[FragmentMetadata]",
        "opened_at_end_timestamp": "float",
    }

    attribute_map = {
        "query_type": "queryType",
        "uri": "uri",
        "end_timestamp": "endTimestamp",
        "start_timestamp": "startTimestamp",
        "array_schema_latest": "arraySchemaLatest",
        "array_schemas_all": "arraySchemasAll",
        "array_metadata": "arrayMetadata",
        "non_empty_domain": "nonEmptyDomain",
        "array_directory": "arrayDirectory",
        "fragment_metadata_all": "fragmentMetadataAll",
        "opened_at_end_timestamp": "openedAtEndTimestamp",
    }

    def __init__(
        self,
        query_type=None,
        uri=None,
        end_timestamp=None,
        start_timestamp=None,
        array_schema_latest=None,
        array_schemas_all=None,
        array_metadata=None,
        non_empty_domain=None,
        array_directory=None,
        fragment_metadata_all=None,
        opened_at_end_timestamp=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """Array - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._query_type = None
        self._uri = None
        self._end_timestamp = None
        self._start_timestamp = None
        self._array_schema_latest = None
        self._array_schemas_all = None
        self._array_metadata = None
        self._non_empty_domain = None
        self._array_directory = None
        self._fragment_metadata_all = None
        self._opened_at_end_timestamp = None
        self.discriminator = None

        self.query_type = query_type
        self.uri = uri
        if end_timestamp is not None:
            self.end_timestamp = end_timestamp
        if start_timestamp is not None:
            self.start_timestamp = start_timestamp
        if array_schema_latest is not None:
            self.array_schema_latest = array_schema_latest
        if array_schemas_all is not None:
            self.array_schemas_all = array_schemas_all
        if array_metadata is not None:
            self.array_metadata = array_metadata
        if non_empty_domain is not None:
            self.non_empty_domain = non_empty_domain
        if array_directory is not None:
            self.array_directory = array_directory
        if fragment_metadata_all is not None:
            self.fragment_metadata_all = fragment_metadata_all
        if opened_at_end_timestamp is not None:
            self.opened_at_end_timestamp = opened_at_end_timestamp

    @property
    def query_type(self):
        """Gets the query_type of this Array.  # noqa: E501


        :return: The query_type of this Array.  # noqa: E501
        :rtype: Querytype
        """
        return self._query_type

    @query_type.setter
    def query_type(self, query_type):
        """Sets the query_type of this Array.


        :param query_type: The query_type of this Array.  # noqa: E501
        :type: Querytype
        """
        if (
            self.local_vars_configuration.client_side_validation and query_type is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `query_type`, must not be `None`"
            )  # noqa: E501

        self._query_type = query_type

    @property
    def uri(self):
        """Gets the uri of this Array.  # noqa: E501

        Array uri  # noqa: E501

        :return: The uri of this Array.  # noqa: E501
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """Sets the uri of this Array.

        Array uri  # noqa: E501

        :param uri: The uri of this Array.  # noqa: E501
        :type: str
        """
        if (
            self.local_vars_configuration.client_side_validation and uri is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `uri`, must not be `None`"
            )  # noqa: E501

        self._uri = uri

    @property
    def end_timestamp(self):
        """Gets the end_timestamp of this Array.  # noqa: E501

        Ending timestamp (epoch milliseconds) array is opened at  # noqa: E501

        :return: The end_timestamp of this Array.  # noqa: E501
        :rtype: float
        """
        return self._end_timestamp

    @end_timestamp.setter
    def end_timestamp(self, end_timestamp):
        """Sets the end_timestamp of this Array.

        Ending timestamp (epoch milliseconds) array is opened at  # noqa: E501

        :param end_timestamp: The end_timestamp of this Array.  # noqa: E501
        :type: float
        """

        self._end_timestamp = end_timestamp

    @property
    def start_timestamp(self):
        """Gets the start_timestamp of this Array.  # noqa: E501

        Starting timestamp (epoch milliseconds) array is opened at  # noqa: E501

        :return: The start_timestamp of this Array.  # noqa: E501
        :rtype: float
        """
        return self._start_timestamp

    @start_timestamp.setter
    def start_timestamp(self, start_timestamp):
        """Sets the start_timestamp of this Array.

        Starting timestamp (epoch milliseconds) array is opened at  # noqa: E501

        :param start_timestamp: The start_timestamp of this Array.  # noqa: E501
        :type: float
        """

        self._start_timestamp = start_timestamp

    @property
    def array_schema_latest(self):
        """Gets the array_schema_latest of this Array.  # noqa: E501


        :return: The array_schema_latest of this Array.  # noqa: E501
        :rtype: ArraySchema
        """
        return self._array_schema_latest

    @array_schema_latest.setter
    def array_schema_latest(self, array_schema_latest):
        """Sets the array_schema_latest of this Array.


        :param array_schema_latest: The array_schema_latest of this Array.  # noqa: E501
        :type: ArraySchema
        """

        self._array_schema_latest = array_schema_latest

    @property
    def array_schemas_all(self):
        """Gets the array_schemas_all of this Array.  # noqa: E501


        :return: The array_schemas_all of this Array.  # noqa: E501
        :rtype: ArraySchemaMap
        """
        return self._array_schemas_all

    @array_schemas_all.setter
    def array_schemas_all(self, array_schemas_all):
        """Sets the array_schemas_all of this Array.


        :param array_schemas_all: The array_schemas_all of this Array.  # noqa: E501
        :type: ArraySchemaMap
        """

        self._array_schemas_all = array_schemas_all

    @property
    def array_metadata(self):
        """Gets the array_metadata of this Array.  # noqa: E501


        :return: The array_metadata of this Array.  # noqa: E501
        :rtype: ArrayMetadata
        """
        return self._array_metadata

    @array_metadata.setter
    def array_metadata(self, array_metadata):
        """Sets the array_metadata of this Array.


        :param array_metadata: The array_metadata of this Array.  # noqa: E501
        :type: ArrayMetadata
        """

        self._array_metadata = array_metadata

    @property
    def non_empty_domain(self):
        """Gets the non_empty_domain of this Array.  # noqa: E501


        :return: The non_empty_domain of this Array.  # noqa: E501
        :rtype: NonEmptyDomainList
        """
        return self._non_empty_domain

    @non_empty_domain.setter
    def non_empty_domain(self, non_empty_domain):
        """Sets the non_empty_domain of this Array.


        :param non_empty_domain: The non_empty_domain of this Array.  # noqa: E501
        :type: NonEmptyDomainList
        """

        self._non_empty_domain = non_empty_domain

    @property
    def array_directory(self):
        """Gets the array_directory of this Array.  # noqa: E501


        :return: The array_directory of this Array.  # noqa: E501
        :rtype: ArrayDirectory
        """
        return self._array_directory

    @array_directory.setter
    def array_directory(self, array_directory):
        """Sets the array_directory of this Array.


        :param array_directory: The array_directory of this Array.  # noqa: E501
        :type: ArrayDirectory
        """

        self._array_directory = array_directory

    @property
    def fragment_metadata_all(self):
        """Gets the fragment_metadata_all of this Array.  # noqa: E501

        metadata for all fragments (for reads)  # noqa: E501

        :return: The fragment_metadata_all of this Array.  # noqa: E501
        :rtype: list[FragmentMetadata]
        """
        return self._fragment_metadata_all

    @fragment_metadata_all.setter
    def fragment_metadata_all(self, fragment_metadata_all):
        """Sets the fragment_metadata_all of this Array.

        metadata for all fragments (for reads)  # noqa: E501

        :param fragment_metadata_all: The fragment_metadata_all of this Array.  # noqa: E501
        :type: list[FragmentMetadata]
        """

        self._fragment_metadata_all = fragment_metadata_all

    @property
    def opened_at_end_timestamp(self):
        """Gets the opened_at_end_timestamp of this Array.  # noqa: E501

        The ending timestamp that the array was last opened at  # noqa: E501

        :return: The opened_at_end_timestamp of this Array.  # noqa: E501
        :rtype: float
        """
        return self._opened_at_end_timestamp

    @opened_at_end_timestamp.setter
    def opened_at_end_timestamp(self, opened_at_end_timestamp):
        """Sets the opened_at_end_timestamp of this Array.

        The ending timestamp that the array was last opened at  # noqa: E501

        :param opened_at_end_timestamp: The opened_at_end_timestamp of this Array.  # noqa: E501
        :type: float
        """

        self._opened_at_end_timestamp = opened_at_end_timestamp

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
        if not isinstance(other, Array):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Array):
            return True

        return self.to_dict() != other.to_dict()
