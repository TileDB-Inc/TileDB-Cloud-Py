# coding: utf-8

"""
    Tiledb Storage Platform API

    TileDB Storage Platform REST API

    The version of the OpenAPI document: 1.4.0
    Generated by: https://openapi-generator.tech
"""


import pprint

from tiledb.cloud._common.api_v2.configuration import Configuration


class ArrayDirectory:
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
        "unfiltered_fragment_uris": "list[str]",
        "consolidated_commit_uris": "list[str]",
        "array_schema_uris": "list[str]",
        "latest_array_schema_uri": "str",
        "array_meta_uris_to_vacuum": "list[str]",
        "array_meta_vac_uris_to_vacuum": "list[str]",
        "commit_uris_to_consolidate": "list[str]",
        "commit_uris_to_vacuum": "list[str]",
        "consolidated_commit_uris_to_vacuum": "list[str]",
        "fragment_meta_uris": "list[str]",
        "timestamp_start": "float",
        "timestamp_end": "float",
        "array_meta_uris": "list[TimestampedURI]",
        "delete_and_update_tile_location": "list[DeleteAndUpdateTileLocation]",
    }

    attribute_map = {
        "unfiltered_fragment_uris": "unfilteredFragmentUris",
        "consolidated_commit_uris": "consolidatedCommitUris",
        "array_schema_uris": "arraySchemaUris",
        "latest_array_schema_uri": "latestArraySchemaUri",
        "array_meta_uris_to_vacuum": "arrayMetaUrisToVacuum",
        "array_meta_vac_uris_to_vacuum": "arrayMetaVacUrisToVacuum",
        "commit_uris_to_consolidate": "commitUrisToConsolidate",
        "commit_uris_to_vacuum": "commitUrisToVacuum",
        "consolidated_commit_uris_to_vacuum": "consolidatedCommitUrisToVacuum",
        "fragment_meta_uris": "fragmentMetaUris",
        "timestamp_start": "timestampStart",
        "timestamp_end": "timestampEnd",
        "array_meta_uris": "arrayMetaUris",
        "delete_and_update_tile_location": "deleteAndUpdateTileLocation",
    }

    def __init__(
        self,
        unfiltered_fragment_uris=None,
        consolidated_commit_uris=None,
        array_schema_uris=None,
        latest_array_schema_uri=None,
        array_meta_uris_to_vacuum=None,
        array_meta_vac_uris_to_vacuum=None,
        commit_uris_to_consolidate=None,
        commit_uris_to_vacuum=None,
        consolidated_commit_uris_to_vacuum=None,
        fragment_meta_uris=None,
        timestamp_start=None,
        timestamp_end=None,
        array_meta_uris=None,
        delete_and_update_tile_location=None,
        local_vars_configuration=None,
    ):
        """ArrayDirectory - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._unfiltered_fragment_uris = None
        self._consolidated_commit_uris = None
        self._array_schema_uris = None
        self._latest_array_schema_uri = None
        self._array_meta_uris_to_vacuum = None
        self._array_meta_vac_uris_to_vacuum = None
        self._commit_uris_to_consolidate = None
        self._commit_uris_to_vacuum = None
        self._consolidated_commit_uris_to_vacuum = None
        self._fragment_meta_uris = None
        self._timestamp_start = None
        self._timestamp_end = None
        self._array_meta_uris = None
        self._delete_and_update_tile_location = None
        self.discriminator = None

        if unfiltered_fragment_uris is not None:
            self.unfiltered_fragment_uris = unfiltered_fragment_uris
        if consolidated_commit_uris is not None:
            self.consolidated_commit_uris = consolidated_commit_uris
        if array_schema_uris is not None:
            self.array_schema_uris = array_schema_uris
        if latest_array_schema_uri is not None:
            self.latest_array_schema_uri = latest_array_schema_uri
        if array_meta_uris_to_vacuum is not None:
            self.array_meta_uris_to_vacuum = array_meta_uris_to_vacuum
        if array_meta_vac_uris_to_vacuum is not None:
            self.array_meta_vac_uris_to_vacuum = array_meta_vac_uris_to_vacuum
        if commit_uris_to_consolidate is not None:
            self.commit_uris_to_consolidate = commit_uris_to_consolidate
        if commit_uris_to_vacuum is not None:
            self.commit_uris_to_vacuum = commit_uris_to_vacuum
        if consolidated_commit_uris_to_vacuum is not None:
            self.consolidated_commit_uris_to_vacuum = consolidated_commit_uris_to_vacuum
        if fragment_meta_uris is not None:
            self.fragment_meta_uris = fragment_meta_uris
        if timestamp_start is not None:
            self.timestamp_start = timestamp_start
        if timestamp_end is not None:
            self.timestamp_end = timestamp_end
        if array_meta_uris is not None:
            self.array_meta_uris = array_meta_uris
        if delete_and_update_tile_location is not None:
            self.delete_and_update_tile_location = delete_and_update_tile_location

    @property
    def unfiltered_fragment_uris(self):
        """Gets the unfiltered_fragment_uris of this ArrayDirectory.

        fragment URIs

        :return: The unfiltered_fragment_uris of this ArrayDirectory.
        :rtype: list[str]
        """
        return self._unfiltered_fragment_uris

    @unfiltered_fragment_uris.setter
    def unfiltered_fragment_uris(self, unfiltered_fragment_uris):
        """Sets the unfiltered_fragment_uris of this ArrayDirectory.

        fragment URIs

        :param unfiltered_fragment_uris: The unfiltered_fragment_uris of this ArrayDirectory.
        :type: list[str]
        """

        self._unfiltered_fragment_uris = unfiltered_fragment_uris

    @property
    def consolidated_commit_uris(self):
        """Gets the consolidated_commit_uris of this ArrayDirectory.

        consolidated commit URI set

        :return: The consolidated_commit_uris of this ArrayDirectory.
        :rtype: list[str]
        """
        return self._consolidated_commit_uris

    @consolidated_commit_uris.setter
    def consolidated_commit_uris(self, consolidated_commit_uris):
        """Sets the consolidated_commit_uris of this ArrayDirectory.

        consolidated commit URI set

        :param consolidated_commit_uris: The consolidated_commit_uris of this ArrayDirectory.
        :type: list[str]
        """

        self._consolidated_commit_uris = consolidated_commit_uris

    @property
    def array_schema_uris(self):
        """Gets the array_schema_uris of this ArrayDirectory.

        URIs of all the array schema files

        :return: The array_schema_uris of this ArrayDirectory.
        :rtype: list[str]
        """
        return self._array_schema_uris

    @array_schema_uris.setter
    def array_schema_uris(self, array_schema_uris):
        """Sets the array_schema_uris of this ArrayDirectory.

        URIs of all the array schema files

        :param array_schema_uris: The array_schema_uris of this ArrayDirectory.
        :type: list[str]
        """

        self._array_schema_uris = array_schema_uris

    @property
    def latest_array_schema_uri(self):
        """Gets the latest_array_schema_uri of this ArrayDirectory.

        latest array schema URI.

        :return: The latest_array_schema_uri of this ArrayDirectory.
        :rtype: str
        """
        return self._latest_array_schema_uri

    @latest_array_schema_uri.setter
    def latest_array_schema_uri(self, latest_array_schema_uri):
        """Sets the latest_array_schema_uri of this ArrayDirectory.

        latest array schema URI.

        :param latest_array_schema_uri: The latest_array_schema_uri of this ArrayDirectory.
        :type: str
        """

        self._latest_array_schema_uri = latest_array_schema_uri

    @property
    def array_meta_uris_to_vacuum(self):
        """Gets the array_meta_uris_to_vacuum of this ArrayDirectory.

        the array metadata files to vacuum

        :return: The array_meta_uris_to_vacuum of this ArrayDirectory.
        :rtype: list[str]
        """
        return self._array_meta_uris_to_vacuum

    @array_meta_uris_to_vacuum.setter
    def array_meta_uris_to_vacuum(self, array_meta_uris_to_vacuum):
        """Sets the array_meta_uris_to_vacuum of this ArrayDirectory.

        the array metadata files to vacuum

        :param array_meta_uris_to_vacuum: The array_meta_uris_to_vacuum of this ArrayDirectory.
        :type: list[str]
        """

        self._array_meta_uris_to_vacuum = array_meta_uris_to_vacuum

    @property
    def array_meta_vac_uris_to_vacuum(self):
        """Gets the array_meta_vac_uris_to_vacuum of this ArrayDirectory.

        the array metadata vac files to vacuum

        :return: The array_meta_vac_uris_to_vacuum of this ArrayDirectory.
        :rtype: list[str]
        """
        return self._array_meta_vac_uris_to_vacuum

    @array_meta_vac_uris_to_vacuum.setter
    def array_meta_vac_uris_to_vacuum(self, array_meta_vac_uris_to_vacuum):
        """Sets the array_meta_vac_uris_to_vacuum of this ArrayDirectory.

        the array metadata vac files to vacuum

        :param array_meta_vac_uris_to_vacuum: The array_meta_vac_uris_to_vacuum of this ArrayDirectory.
        :type: list[str]
        """

        self._array_meta_vac_uris_to_vacuum = array_meta_vac_uris_to_vacuum

    @property
    def commit_uris_to_consolidate(self):
        """Gets the commit_uris_to_consolidate of this ArrayDirectory.

        the commit files to consolidate

        :return: The commit_uris_to_consolidate of this ArrayDirectory.
        :rtype: list[str]
        """
        return self._commit_uris_to_consolidate

    @commit_uris_to_consolidate.setter
    def commit_uris_to_consolidate(self, commit_uris_to_consolidate):
        """Sets the commit_uris_to_consolidate of this ArrayDirectory.

        the commit files to consolidate

        :param commit_uris_to_consolidate: The commit_uris_to_consolidate of this ArrayDirectory.
        :type: list[str]
        """

        self._commit_uris_to_consolidate = commit_uris_to_consolidate

    @property
    def commit_uris_to_vacuum(self):
        """Gets the commit_uris_to_vacuum of this ArrayDirectory.

        the commit files to vacuum

        :return: The commit_uris_to_vacuum of this ArrayDirectory.
        :rtype: list[str]
        """
        return self._commit_uris_to_vacuum

    @commit_uris_to_vacuum.setter
    def commit_uris_to_vacuum(self, commit_uris_to_vacuum):
        """Sets the commit_uris_to_vacuum of this ArrayDirectory.

        the commit files to vacuum

        :param commit_uris_to_vacuum: The commit_uris_to_vacuum of this ArrayDirectory.
        :type: list[str]
        """

        self._commit_uris_to_vacuum = commit_uris_to_vacuum

    @property
    def consolidated_commit_uris_to_vacuum(self):
        """Gets the consolidated_commit_uris_to_vacuum of this ArrayDirectory.

        the consolidated commit files to vacuum

        :return: The consolidated_commit_uris_to_vacuum of this ArrayDirectory.
        :rtype: list[str]
        """
        return self._consolidated_commit_uris_to_vacuum

    @consolidated_commit_uris_to_vacuum.setter
    def consolidated_commit_uris_to_vacuum(self, consolidated_commit_uris_to_vacuum):
        """Sets the consolidated_commit_uris_to_vacuum of this ArrayDirectory.

        the consolidated commit files to vacuum

        :param consolidated_commit_uris_to_vacuum: The consolidated_commit_uris_to_vacuum of this ArrayDirectory.
        :type: list[str]
        """

        self._consolidated_commit_uris_to_vacuum = consolidated_commit_uris_to_vacuum

    @property
    def fragment_meta_uris(self):
        """Gets the fragment_meta_uris of this ArrayDirectory.

        the URIs of the consolidated fragment metadata files

        :return: The fragment_meta_uris of this ArrayDirectory.
        :rtype: list[str]
        """
        return self._fragment_meta_uris

    @fragment_meta_uris.setter
    def fragment_meta_uris(self, fragment_meta_uris):
        """Sets the fragment_meta_uris of this ArrayDirectory.

        the URIs of the consolidated fragment metadata files

        :param fragment_meta_uris: The fragment_meta_uris of this ArrayDirectory.
        :type: list[str]
        """

        self._fragment_meta_uris = fragment_meta_uris

    @property
    def timestamp_start(self):
        """Gets the timestamp_start of this ArrayDirectory.

        Only the files created after timestamp_start are listed

        :return: The timestamp_start of this ArrayDirectory.
        :rtype: float
        """
        return self._timestamp_start

    @timestamp_start.setter
    def timestamp_start(self, timestamp_start):
        """Sets the timestamp_start of this ArrayDirectory.

        Only the files created after timestamp_start are listed

        :param timestamp_start: The timestamp_start of this ArrayDirectory.
        :type: float
        """

        self._timestamp_start = timestamp_start

    @property
    def timestamp_end(self):
        """Gets the timestamp_end of this ArrayDirectory.

        Only the files created before timestamp_end are listed

        :return: The timestamp_end of this ArrayDirectory.
        :rtype: float
        """
        return self._timestamp_end

    @timestamp_end.setter
    def timestamp_end(self, timestamp_end):
        """Sets the timestamp_end of this ArrayDirectory.

        Only the files created before timestamp_end are listed

        :param timestamp_end: The timestamp_end of this ArrayDirectory.
        :type: float
        """

        self._timestamp_end = timestamp_end

    @property
    def array_meta_uris(self):
        """Gets the array_meta_uris of this ArrayDirectory.

        the timestamped filtered array metadata URIs, after removing the ones that need to be vacuumed and those that do not fall within

        :return: The array_meta_uris of this ArrayDirectory.
        :rtype: list[TimestampedURI]
        """
        return self._array_meta_uris

    @array_meta_uris.setter
    def array_meta_uris(self, array_meta_uris):
        """Sets the array_meta_uris of this ArrayDirectory.

        the timestamped filtered array metadata URIs, after removing the ones that need to be vacuumed and those that do not fall within

        :param array_meta_uris: The array_meta_uris of this ArrayDirectory.
        :type: list[TimestampedURI]
        """

        self._array_meta_uris = array_meta_uris

    @property
    def delete_and_update_tile_location(self):
        """Gets the delete_and_update_tile_location of this ArrayDirectory.

        the location of delete tiles

        :return: The delete_and_update_tile_location of this ArrayDirectory.
        :rtype: list[DeleteAndUpdateTileLocation]
        """
        return self._delete_and_update_tile_location

    @delete_and_update_tile_location.setter
    def delete_and_update_tile_location(self, delete_and_update_tile_location):
        """Sets the delete_and_update_tile_location of this ArrayDirectory.

        the location of delete tiles

        :param delete_and_update_tile_location: The delete_and_update_tile_location of this ArrayDirectory.
        :type: list[DeleteAndUpdateTileLocation]
        """

        self._delete_and_update_tile_location = delete_and_update_tile_location

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
        if not isinstance(other, ArrayDirectory):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ArrayDirectory):
            return True

        return self.to_dict() != other.to_dict()
