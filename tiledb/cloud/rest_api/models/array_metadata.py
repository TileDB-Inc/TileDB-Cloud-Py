# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 1.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class ArrayMetadata(object):
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
        "uri": "str",
        "namespace": "str",
        "size": "float",
        "last_accessed": "datetime",
        "description": "str",
        "name": "str",
        "allowed_actions": "list[ArrayActions]",
        "logo": "str",
        "access_credentials_name": "str",
        "type": "str",
        "share_count": "float",
        "public_share": "bool",
        "tiledb_uri": "str",
    }

    attribute_map = {
        "id": "id",
        "uri": "uri",
        "namespace": "namespace",
        "size": "size",
        "last_accessed": "last_accessed",
        "description": "description",
        "name": "name",
        "allowed_actions": "allowed_actions",
        "logo": "logo",
        "access_credentials_name": "access_credentials_name",
        "type": "type",
        "share_count": "share_count",
        "public_share": "public_share",
        "tiledb_uri": "tiledb_uri",
    }

    def __init__(
        self,
        id=None,
        uri=None,
        namespace=None,
        size=None,
        last_accessed=None,
        description=None,
        name=None,
        allowed_actions=None,
        logo=None,
        access_credentials_name=None,
        type=None,
        share_count=None,
        public_share=None,
        tiledb_uri=None,
    ):  # noqa: E501
        """ArrayMetadata - a model defined in OpenAPI"""  # noqa: E501

        self._id = None
        self._uri = None
        self._namespace = None
        self._size = None
        self._last_accessed = None
        self._description = None
        self._name = None
        self._allowed_actions = None
        self._logo = None
        self._access_credentials_name = None
        self._type = None
        self._share_count = None
        self._public_share = None
        self._tiledb_uri = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if uri is not None:
            self.uri = uri
        if namespace is not None:
            self.namespace = namespace
        if size is not None:
            self.size = size
        if last_accessed is not None:
            self.last_accessed = last_accessed
        if description is not None:
            self.description = description
        if name is not None:
            self.name = name
        if allowed_actions is not None:
            self.allowed_actions = allowed_actions
        if logo is not None:
            self.logo = logo
        if access_credentials_name is not None:
            self.access_credentials_name = access_credentials_name
        if type is not None:
            self.type = type
        if share_count is not None:
            self.share_count = share_count
        if public_share is not None:
            self.public_share = public_share
        if tiledb_uri is not None:
            self.tiledb_uri = tiledb_uri

    @property
    def id(self):
        """Gets the id of this ArrayMetadata.  # noqa: E501

        unique id of registered array  # noqa: E501

        :return: The id of this ArrayMetadata.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ArrayMetadata.

        unique id of registered array  # noqa: E501

        :param id: The id of this ArrayMetadata.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def uri(self):
        """Gets the uri of this ArrayMetadata.  # noqa: E501

        uri of array  # noqa: E501

        :return: The uri of this ArrayMetadata.  # noqa: E501
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """Sets the uri of this ArrayMetadata.

        uri of array  # noqa: E501

        :param uri: The uri of this ArrayMetadata.  # noqa: E501
        :type: str
        """

        self._uri = uri

    @property
    def namespace(self):
        """Gets the namespace of this ArrayMetadata.  # noqa: E501

        namespace array is in  # noqa: E501

        :return: The namespace of this ArrayMetadata.  # noqa: E501
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this ArrayMetadata.

        namespace array is in  # noqa: E501

        :param namespace: The namespace of this ArrayMetadata.  # noqa: E501
        :type: str
        """

        self._namespace = namespace

    @property
    def size(self):
        """Gets the size of this ArrayMetadata.  # noqa: E501

        size in bytes of array  # noqa: E501

        :return: The size of this ArrayMetadata.  # noqa: E501
        :rtype: float
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this ArrayMetadata.

        size in bytes of array  # noqa: E501

        :param size: The size of this ArrayMetadata.  # noqa: E501
        :type: float
        """

        self._size = size

    @property
    def last_accessed(self):
        """Gets the last_accessed of this ArrayMetadata.  # noqa: E501

        Datetime array was last accessed in UTC  # noqa: E501

        :return: The last_accessed of this ArrayMetadata.  # noqa: E501
        :rtype: datetime
        """
        return self._last_accessed

    @last_accessed.setter
    def last_accessed(self, last_accessed):
        """Sets the last_accessed of this ArrayMetadata.

        Datetime array was last accessed in UTC  # noqa: E501

        :param last_accessed: The last_accessed of this ArrayMetadata.  # noqa: E501
        :type: datetime
        """

        self._last_accessed = last_accessed

    @property
    def description(self):
        """Gets the description of this ArrayMetadata.  # noqa: E501

        description of array  # noqa: E501

        :return: The description of this ArrayMetadata.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ArrayMetadata.

        description of array  # noqa: E501

        :param description: The description of this ArrayMetadata.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def name(self):
        """Gets the name of this ArrayMetadata.  # noqa: E501

        name of array  # noqa: E501

        :return: The name of this ArrayMetadata.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ArrayMetadata.

        name of array  # noqa: E501

        :param name: The name of this ArrayMetadata.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def allowed_actions(self):
        """Gets the allowed_actions of this ArrayMetadata.  # noqa: E501

        list of actions user is allowed to do on this array  # noqa: E501

        :return: The allowed_actions of this ArrayMetadata.  # noqa: E501
        :rtype: list[ArrayActions]
        """
        return self._allowed_actions

    @allowed_actions.setter
    def allowed_actions(self, allowed_actions):
        """Sets the allowed_actions of this ArrayMetadata.

        list of actions user is allowed to do on this array  # noqa: E501

        :param allowed_actions: The allowed_actions of this ArrayMetadata.  # noqa: E501
        :type: list[ArrayActions]
        """

        self._allowed_actions = allowed_actions

    @property
    def logo(self):
        """Gets the logo of this ArrayMetadata.  # noqa: E501

        logo (base64 encoded) for the array. Optional  # noqa: E501

        :return: The logo of this ArrayMetadata.  # noqa: E501
        :rtype: str
        """
        return self._logo

    @logo.setter
    def logo(self, logo):
        """Sets the logo of this ArrayMetadata.

        logo (base64 encoded) for the array. Optional  # noqa: E501

        :param logo: The logo of this ArrayMetadata.  # noqa: E501
        :type: str
        """

        self._logo = logo

    @property
    def access_credentials_name(self):
        """Gets the access_credentials_name of this ArrayMetadata.  # noqa: E501

        the name of the access credentials to use. if unset, the default credentials will be used  # noqa: E501

        :return: The access_credentials_name of this ArrayMetadata.  # noqa: E501
        :rtype: str
        """
        return self._access_credentials_name

    @access_credentials_name.setter
    def access_credentials_name(self, access_credentials_name):
        """Sets the access_credentials_name of this ArrayMetadata.

        the name of the access credentials to use. if unset, the default credentials will be used  # noqa: E501

        :param access_credentials_name: The access_credentials_name of this ArrayMetadata.  # noqa: E501
        :type: str
        """

        self._access_credentials_name = access_credentials_name

    @property
    def type(self):
        """Gets the type of this ArrayMetadata.  # noqa: E501

        Array type (dense, key-value, sparse)  # noqa: E501

        :return: The type of this ArrayMetadata.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ArrayMetadata.

        Array type (dense, key-value, sparse)  # noqa: E501

        :param type: The type of this ArrayMetadata.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def share_count(self):
        """Gets the share_count of this ArrayMetadata.  # noqa: E501

        number of unique namespaces this array is shared with  # noqa: E501

        :return: The share_count of this ArrayMetadata.  # noqa: E501
        :rtype: float
        """
        return self._share_count

    @share_count.setter
    def share_count(self, share_count):
        """Sets the share_count of this ArrayMetadata.

        number of unique namespaces this array is shared with  # noqa: E501

        :param share_count: The share_count of this ArrayMetadata.  # noqa: E501
        :type: float
        """

        self._share_count = share_count

    @property
    def public_share(self):
        """Gets the public_share of this ArrayMetadata.  # noqa: E501

        Suggests if the array was shared to public by owner  # noqa: E501

        :return: The public_share of this ArrayMetadata.  # noqa: E501
        :rtype: bool
        """
        return self._public_share

    @public_share.setter
    def public_share(self, public_share):
        """Sets the public_share of this ArrayMetadata.

        Suggests if the array was shared to public by owner  # noqa: E501

        :param public_share: The public_share of this ArrayMetadata.  # noqa: E501
        :type: bool
        """

        self._public_share = public_share

    @property
    def tiledb_uri(self):
        """Gets the tiledb_uri of this ArrayMetadata.  # noqa: E501

        uri for access through TileDB cloud  # noqa: E501

        :return: The tiledb_uri of this ArrayMetadata.  # noqa: E501
        :rtype: str
        """
        return self._tiledb_uri

    @tiledb_uri.setter
    def tiledb_uri(self, tiledb_uri):
        """Sets the tiledb_uri of this ArrayMetadata.

        uri for access through TileDB cloud  # noqa: E501

        :param tiledb_uri: The tiledb_uri of this ArrayMetadata.  # noqa: E501
        :type: str
        """

        self._tiledb_uri = tiledb_uri

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
        if not isinstance(other, ArrayMetadata):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
