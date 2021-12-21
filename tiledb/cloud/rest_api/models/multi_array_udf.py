# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.2.19
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from tiledb.cloud.rest_api.configuration import Configuration


class MultiArrayUDF(object):
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
        "udf_info_name": "str",
        "language": "UDFLanguage",
        "version": "str",
        "image_name": "str",
        "_exec": "str",
        "exec_raw": "str",
        "result_format": "ResultFormat",
        "task_name": "str",
        "argument": "str",
        "stored_param_uuids": "list[str]",
        "store_results": "bool",
        "ranges": "QueryRanges",
        "subarray": "UDFSubarray",
        "buffers": "list[str]",
        "arrays": "list[UDFArrayDetails]",
        "timeout": "int",
    }

    attribute_map = {
        "udf_info_name": "udf_info_name",
        "language": "language",
        "version": "version",
        "image_name": "image_name",
        "_exec": "exec",
        "exec_raw": "exec_raw",
        "result_format": "result_format",
        "task_name": "task_name",
        "argument": "argument",
        "stored_param_uuids": "stored_param_uuids",
        "store_results": "store_results",
        "ranges": "ranges",
        "subarray": "subarray",
        "buffers": "buffers",
        "arrays": "arrays",
        "timeout": "timeout",
    }

    def __init__(
        self,
        udf_info_name=None,
        language=None,
        version=None,
        image_name=None,
        _exec=None,
        exec_raw=None,
        result_format=None,
        task_name=None,
        argument=None,
        stored_param_uuids=None,
        store_results=None,
        ranges=None,
        subarray=None,
        buffers=None,
        arrays=None,
        timeout=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """MultiArrayUDF - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._udf_info_name = None
        self._language = None
        self._version = None
        self._image_name = None
        self.__exec = None
        self._exec_raw = None
        self._result_format = None
        self._task_name = None
        self._argument = None
        self._stored_param_uuids = None
        self._store_results = None
        self._ranges = None
        self._subarray = None
        self._buffers = None
        self._arrays = None
        self._timeout = None
        self.discriminator = None

        if udf_info_name is not None:
            self.udf_info_name = udf_info_name
        if language is not None:
            self.language = language
        if version is not None:
            self.version = version
        if image_name is not None:
            self.image_name = image_name
        if _exec is not None:
            self._exec = _exec
        if exec_raw is not None:
            self.exec_raw = exec_raw
        if result_format is not None:
            self.result_format = result_format
        if task_name is not None:
            self.task_name = task_name
        if argument is not None:
            self.argument = argument
        if stored_param_uuids is not None:
            self.stored_param_uuids = stored_param_uuids
        if store_results is not None:
            self.store_results = store_results
        if ranges is not None:
            self.ranges = ranges
        if subarray is not None:
            self.subarray = subarray
        if buffers is not None:
            self.buffers = buffers
        if arrays is not None:
            self.arrays = arrays
        if timeout is not None:
            self.timeout = timeout

    @property
    def udf_info_name(self):
        """Gets the udf_info_name of this MultiArrayUDF.  # noqa: E501

        name of UDFInfo to run, format is {namespace}/{udf_name}. Can not be used with exec  # noqa: E501

        :return: The udf_info_name of this MultiArrayUDF.  # noqa: E501
        :rtype: str
        """
        return self._udf_info_name

    @udf_info_name.setter
    def udf_info_name(self, udf_info_name):
        """Sets the udf_info_name of this MultiArrayUDF.

        name of UDFInfo to run, format is {namespace}/{udf_name}. Can not be used with exec  # noqa: E501

        :param udf_info_name: The udf_info_name of this MultiArrayUDF.  # noqa: E501
        :type: str
        """

        self._udf_info_name = udf_info_name

    @property
    def language(self):
        """Gets the language of this MultiArrayUDF.  # noqa: E501


        :return: The language of this MultiArrayUDF.  # noqa: E501
        :rtype: UDFLanguage
        """
        return self._language

    @language.setter
    def language(self, language):
        """Sets the language of this MultiArrayUDF.


        :param language: The language of this MultiArrayUDF.  # noqa: E501
        :type: UDFLanguage
        """

        self._language = language

    @property
    def version(self):
        """Gets the version of this MultiArrayUDF.  # noqa: E501

        Type-specific version  # noqa: E501

        :return: The version of this MultiArrayUDF.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this MultiArrayUDF.

        Type-specific version  # noqa: E501

        :param version: The version of this MultiArrayUDF.  # noqa: E501
        :type: str
        """

        self._version = version

    @property
    def image_name(self):
        """Gets the image_name of this MultiArrayUDF.  # noqa: E501

        Docker image name to use for UDF  # noqa: E501

        :return: The image_name of this MultiArrayUDF.  # noqa: E501
        :rtype: str
        """
        return self._image_name

    @image_name.setter
    def image_name(self, image_name):
        """Sets the image_name of this MultiArrayUDF.

        Docker image name to use for UDF  # noqa: E501

        :param image_name: The image_name of this MultiArrayUDF.  # noqa: E501
        :type: str
        """

        self._image_name = image_name

    @property
    def _exec(self):
        """Gets the _exec of this MultiArrayUDF.  # noqa: E501

        Type-specific executable text  # noqa: E501

        :return: The _exec of this MultiArrayUDF.  # noqa: E501
        :rtype: str
        """
        return self.__exec

    @_exec.setter
    def _exec(self, _exec):
        """Sets the _exec of this MultiArrayUDF.

        Type-specific executable text  # noqa: E501

        :param _exec: The _exec of this MultiArrayUDF.  # noqa: E501
        :type: str
        """

        self.__exec = _exec

    @property
    def exec_raw(self):
        """Gets the exec_raw of this MultiArrayUDF.  # noqa: E501

        optional raw text to store of serialized function, used for showing in UI  # noqa: E501

        :return: The exec_raw of this MultiArrayUDF.  # noqa: E501
        :rtype: str
        """
        return self._exec_raw

    @exec_raw.setter
    def exec_raw(self, exec_raw):
        """Sets the exec_raw of this MultiArrayUDF.

        optional raw text to store of serialized function, used for showing in UI  # noqa: E501

        :param exec_raw: The exec_raw of this MultiArrayUDF.  # noqa: E501
        :type: str
        """

        self._exec_raw = exec_raw

    @property
    def result_format(self):
        """Gets the result_format of this MultiArrayUDF.  # noqa: E501


        :return: The result_format of this MultiArrayUDF.  # noqa: E501
        :rtype: ResultFormat
        """
        return self._result_format

    @result_format.setter
    def result_format(self, result_format):
        """Sets the result_format of this MultiArrayUDF.


        :param result_format: The result_format of this MultiArrayUDF.  # noqa: E501
        :type: ResultFormat
        """

        self._result_format = result_format

    @property
    def task_name(self):
        """Gets the task_name of this MultiArrayUDF.  # noqa: E501

        name of task, optional  # noqa: E501

        :return: The task_name of this MultiArrayUDF.  # noqa: E501
        :rtype: str
        """
        return self._task_name

    @task_name.setter
    def task_name(self, task_name):
        """Sets the task_name of this MultiArrayUDF.

        name of task, optional  # noqa: E501

        :param task_name: The task_name of this MultiArrayUDF.  # noqa: E501
        :type: str
        """

        self._task_name = task_name

    @property
    def argument(self):
        """Gets the argument of this MultiArrayUDF.  # noqa: E501

        Argument(s) to pass to UDF function, tuple or list of args/kwargs which can be in native or JSON format  # noqa: E501

        :return: The argument of this MultiArrayUDF.  # noqa: E501
        :rtype: str
        """
        return self._argument

    @argument.setter
    def argument(self, argument):
        """Sets the argument of this MultiArrayUDF.

        Argument(s) to pass to UDF function, tuple or list of args/kwargs which can be in native or JSON format  # noqa: E501

        :param argument: The argument of this MultiArrayUDF.  # noqa: E501
        :type: str
        """

        self._argument = argument

    @property
    def stored_param_uuids(self):
        """Gets the stored_param_uuids of this MultiArrayUDF.  # noqa: E501

        The UUIDs of stored input parameters (passed in a language-specific format within \"argument\") to be retrieved from the server-side cache. Serialized in standard hex format with no {}.  # noqa: E501

        :return: The stored_param_uuids of this MultiArrayUDF.  # noqa: E501
        :rtype: list[str]
        """
        return self._stored_param_uuids

    @stored_param_uuids.setter
    def stored_param_uuids(self, stored_param_uuids):
        """Sets the stored_param_uuids of this MultiArrayUDF.

        The UUIDs of stored input parameters (passed in a language-specific format within \"argument\") to be retrieved from the server-side cache. Serialized in standard hex format with no {}.  # noqa: E501

        :param stored_param_uuids: The stored_param_uuids of this MultiArrayUDF.  # noqa: E501
        :type: list[str]
        """

        self._stored_param_uuids = stored_param_uuids

    @property
    def store_results(self):
        """Gets the store_results of this MultiArrayUDF.  # noqa: E501

        store results for later retrieval  # noqa: E501

        :return: The store_results of this MultiArrayUDF.  # noqa: E501
        :rtype: bool
        """
        return self._store_results

    @store_results.setter
    def store_results(self, store_results):
        """Sets the store_results of this MultiArrayUDF.

        store results for later retrieval  # noqa: E501

        :param store_results: The store_results of this MultiArrayUDF.  # noqa: E501
        :type: bool
        """

        self._store_results = store_results

    @property
    def ranges(self):
        """Gets the ranges of this MultiArrayUDF.  # noqa: E501


        :return: The ranges of this MultiArrayUDF.  # noqa: E501
        :rtype: QueryRanges
        """
        return self._ranges

    @ranges.setter
    def ranges(self, ranges):
        """Sets the ranges of this MultiArrayUDF.


        :param ranges: The ranges of this MultiArrayUDF.  # noqa: E501
        :type: QueryRanges
        """

        self._ranges = ranges

    @property
    def subarray(self):
        """Gets the subarray of this MultiArrayUDF.  # noqa: E501


        :return: The subarray of this MultiArrayUDF.  # noqa: E501
        :rtype: UDFSubarray
        """
        return self._subarray

    @subarray.setter
    def subarray(self, subarray):
        """Sets the subarray of this MultiArrayUDF.


        :param subarray: The subarray of this MultiArrayUDF.  # noqa: E501
        :type: UDFSubarray
        """

        self._subarray = subarray

    @property
    def buffers(self):
        """Gets the buffers of this MultiArrayUDF.  # noqa: E501

        List of buffers to fetch (attributes + dimensions). Deprecated; please set arrays with `UDFArrayDetails`.  # noqa: E501

        :return: The buffers of this MultiArrayUDF.  # noqa: E501
        :rtype: list[str]
        """
        return self._buffers

    @buffers.setter
    def buffers(self, buffers):
        """Sets the buffers of this MultiArrayUDF.

        List of buffers to fetch (attributes + dimensions). Deprecated; please set arrays with `UDFArrayDetails`.  # noqa: E501

        :param buffers: The buffers of this MultiArrayUDF.  # noqa: E501
        :type: list[str]
        """

        self._buffers = buffers

    @property
    def arrays(self):
        """Gets the arrays of this MultiArrayUDF.  # noqa: E501

        Array ranges/buffer into to run UDF on  # noqa: E501

        :return: The arrays of this MultiArrayUDF.  # noqa: E501
        :rtype: list[UDFArrayDetails]
        """
        return self._arrays

    @arrays.setter
    def arrays(self, arrays):
        """Sets the arrays of this MultiArrayUDF.

        Array ranges/buffer into to run UDF on  # noqa: E501

        :param arrays: The arrays of this MultiArrayUDF.  # noqa: E501
        :type: list[UDFArrayDetails]
        """

        self._arrays = arrays

    @property
    def timeout(self):
        """Gets the timeout of this MultiArrayUDF.  # noqa: E501

        UDF-type timeout in seconds (default: 900)  # noqa: E501

        :return: The timeout of this MultiArrayUDF.  # noqa: E501
        :rtype: int
        """
        return self._timeout

    @timeout.setter
    def timeout(self, timeout):
        """Sets the timeout of this MultiArrayUDF.

        UDF-type timeout in seconds (default: 900)  # noqa: E501

        :param timeout: The timeout of this MultiArrayUDF.  # noqa: E501
        :type: int
        """

        self._timeout = timeout

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
        if not isinstance(other, MultiArrayUDF):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MultiArrayUDF):
            return True

        return self.to_dict() != other.to_dict()
