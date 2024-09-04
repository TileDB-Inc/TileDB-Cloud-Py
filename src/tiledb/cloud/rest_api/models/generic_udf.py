# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API

    The version of the OpenAPI document: 2.17.51
    Generated by: https://openapi-generator.tech
"""


import pprint

from tiledb.cloud.rest_api.configuration import Configuration


class GenericUDF:
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
        "access_credentials_name": "str",
        "resource_class": "str",
        "_exec": "str",
        "exec_raw": "str",
        "argument": "str",
        "stored_param_uuids": "list[str]",
        "result_format": "ResultFormat",
        "task_name": "str",
        "store_results": "bool",
        "timeout": "int",
        "dont_download_results": "bool",
        "task_graph_uuid": "str",
        "client_node_uuid": "str",
    }

    attribute_map = {
        "udf_info_name": "udf_info_name",
        "language": "language",
        "version": "version",
        "image_name": "image_name",
        "access_credentials_name": "access_credentials_name",
        "resource_class": "resource_class",
        "_exec": "exec",
        "exec_raw": "exec_raw",
        "argument": "argument",
        "stored_param_uuids": "stored_param_uuids",
        "result_format": "result_format",
        "task_name": "task_name",
        "store_results": "store_results",
        "timeout": "timeout",
        "dont_download_results": "dont_download_results",
        "task_graph_uuid": "task_graph_uuid",
        "client_node_uuid": "client_node_uuid",
    }

    def __init__(
        self,
        udf_info_name=None,
        language=None,
        version=None,
        image_name=None,
        access_credentials_name=None,
        resource_class=None,
        _exec=None,
        exec_raw=None,
        argument=None,
        stored_param_uuids=None,
        result_format=None,
        task_name=None,
        store_results=None,
        timeout=None,
        dont_download_results=None,
        task_graph_uuid=None,
        client_node_uuid=None,
        local_vars_configuration=None,
    ):
        """GenericUDF - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._udf_info_name = None
        self._language = None
        self._version = None
        self._image_name = None
        self._access_credentials_name = None
        self._resource_class = None
        self.__exec = None
        self._exec_raw = None
        self._argument = None
        self._stored_param_uuids = None
        self._result_format = None
        self._task_name = None
        self._store_results = None
        self._timeout = None
        self._dont_download_results = None
        self._task_graph_uuid = None
        self._client_node_uuid = None
        self.discriminator = None

        if udf_info_name is not None:
            self.udf_info_name = udf_info_name
        if language is not None:
            self.language = language
        if version is not None:
            self.version = version
        if image_name is not None:
            self.image_name = image_name
        if access_credentials_name is not None:
            self.access_credentials_name = access_credentials_name
        if resource_class is not None:
            self.resource_class = resource_class
        if _exec is not None:
            self._exec = _exec
        if exec_raw is not None:
            self.exec_raw = exec_raw
        if argument is not None:
            self.argument = argument
        if stored_param_uuids is not None:
            self.stored_param_uuids = stored_param_uuids
        if result_format is not None:
            self.result_format = result_format
        if task_name is not None:
            self.task_name = task_name
        if store_results is not None:
            self.store_results = store_results
        if timeout is not None:
            self.timeout = timeout
        if dont_download_results is not None:
            self.dont_download_results = dont_download_results
        if task_graph_uuid is not None:
            self.task_graph_uuid = task_graph_uuid
        if client_node_uuid is not None:
            self.client_node_uuid = client_node_uuid

    @property
    def udf_info_name(self):
        """Gets the udf_info_name of this GenericUDF.

        name of UDFInfo to run, format is {namespace}/{udf_name}. Can not be used with exec

        :return: The udf_info_name of this GenericUDF.
        :rtype: str
        """
        return self._udf_info_name

    @udf_info_name.setter
    def udf_info_name(self, udf_info_name):
        """Sets the udf_info_name of this GenericUDF.

        name of UDFInfo to run, format is {namespace}/{udf_name}. Can not be used with exec

        :param udf_info_name: The udf_info_name of this GenericUDF.
        :type: str
        """

        self._udf_info_name = udf_info_name

    @property
    def language(self):
        """Gets the language of this GenericUDF.


        :return: The language of this GenericUDF.
        :rtype: UDFLanguage
        """
        return self._language

    @language.setter
    def language(self, language):
        """Sets the language of this GenericUDF.


        :param language: The language of this GenericUDF.
        :type: UDFLanguage
        """

        self._language = language

    @property
    def version(self):
        """Gets the version of this GenericUDF.

        Type-specific version

        :return: The version of this GenericUDF.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this GenericUDF.

        Type-specific version

        :param version: The version of this GenericUDF.
        :type: str
        """

        self._version = version

    @property
    def image_name(self):
        """Gets the image_name of this GenericUDF.

        Docker image name to use for UDF

        :return: The image_name of this GenericUDF.
        :rtype: str
        """
        return self._image_name

    @image_name.setter
    def image_name(self, image_name):
        """Sets the image_name of this GenericUDF.

        Docker image name to use for UDF

        :param image_name: The image_name of this GenericUDF.
        :type: str
        """

        self._image_name = image_name

    @property
    def access_credentials_name(self):
        """Gets the access_credentials_name of this GenericUDF.

        The name of the access credentials to use. if unset, no credentials will be configured in the environment.

        :return: The access_credentials_name of this GenericUDF.
        :rtype: str
        """
        return self._access_credentials_name

    @access_credentials_name.setter
    def access_credentials_name(self, access_credentials_name):
        """Sets the access_credentials_name of this GenericUDF.

        The name of the access credentials to use. if unset, no credentials will be configured in the environment.

        :param access_credentials_name: The access_credentials_name of this GenericUDF.
        :type: str
        """

        self._access_credentials_name = access_credentials_name

    @property
    def resource_class(self):
        """Gets the resource_class of this GenericUDF.

        The resource class to use for the UDF execution. Resource classes define resource limits for memory and CPUs. If this is empty, then the UDF will execute in the standard resource class of the TileDB Cloud provider.

        :return: The resource_class of this GenericUDF.
        :rtype: str
        """
        return self._resource_class

    @resource_class.setter
    def resource_class(self, resource_class):
        """Sets the resource_class of this GenericUDF.

        The resource class to use for the UDF execution. Resource classes define resource limits for memory and CPUs. If this is empty, then the UDF will execute in the standard resource class of the TileDB Cloud provider.

        :param resource_class: The resource_class of this GenericUDF.
        :type: str
        """

        self._resource_class = resource_class

    @property
    def _exec(self):
        """Gets the _exec of this GenericUDF.

        Type-specific executable text

        :return: The _exec of this GenericUDF.
        :rtype: str
        """
        return self.__exec

    @_exec.setter
    def _exec(self, _exec):
        """Sets the _exec of this GenericUDF.

        Type-specific executable text

        :param _exec: The _exec of this GenericUDF.
        :type: str
        """

        self.__exec = _exec

    @property
    def exec_raw(self):
        """Gets the exec_raw of this GenericUDF.

        optional raw text to store of serialized function, used for showing in UI

        :return: The exec_raw of this GenericUDF.
        :rtype: str
        """
        return self._exec_raw

    @exec_raw.setter
    def exec_raw(self, exec_raw):
        """Sets the exec_raw of this GenericUDF.

        optional raw text to store of serialized function, used for showing in UI

        :param exec_raw: The exec_raw of this GenericUDF.
        :type: str
        """

        self._exec_raw = exec_raw

    @property
    def argument(self):
        """Gets the argument of this GenericUDF.

        Argument(s) to pass to UDF function, tuple or list of args/kwargs which can be in native or JSON format

        :return: The argument of this GenericUDF.
        :rtype: str
        """
        return self._argument

    @argument.setter
    def argument(self, argument):
        """Sets the argument of this GenericUDF.

        Argument(s) to pass to UDF function, tuple or list of args/kwargs which can be in native or JSON format

        :param argument: The argument of this GenericUDF.
        :type: str
        """

        self._argument = argument

    @property
    def stored_param_uuids(self):
        """Gets the stored_param_uuids of this GenericUDF.

        The UUIDs of stored input parameters (passed in a language-specific format within \"argument\") to be retrieved from the server-side cache. Serialized in standard hex format with no {}.

        :return: The stored_param_uuids of this GenericUDF.
        :rtype: list[str]
        """
        return self._stored_param_uuids

    @stored_param_uuids.setter
    def stored_param_uuids(self, stored_param_uuids):
        """Sets the stored_param_uuids of this GenericUDF.

        The UUIDs of stored input parameters (passed in a language-specific format within \"argument\") to be retrieved from the server-side cache. Serialized in standard hex format with no {}.

        :param stored_param_uuids: The stored_param_uuids of this GenericUDF.
        :type: list[str]
        """

        self._stored_param_uuids = stored_param_uuids

    @property
    def result_format(self):
        """Gets the result_format of this GenericUDF.


        :return: The result_format of this GenericUDF.
        :rtype: ResultFormat
        """
        return self._result_format

    @result_format.setter
    def result_format(self, result_format):
        """Sets the result_format of this GenericUDF.


        :param result_format: The result_format of this GenericUDF.
        :type: ResultFormat
        """

        self._result_format = result_format

    @property
    def task_name(self):
        """Gets the task_name of this GenericUDF.

        name of task, optional

        :return: The task_name of this GenericUDF.
        :rtype: str
        """
        return self._task_name

    @task_name.setter
    def task_name(self, task_name):
        """Sets the task_name of this GenericUDF.

        name of task, optional

        :param task_name: The task_name of this GenericUDF.
        :type: str
        """

        self._task_name = task_name

    @property
    def store_results(self):
        """Gets the store_results of this GenericUDF.

        store results for later retrieval

        :return: The store_results of this GenericUDF.
        :rtype: bool
        """
        return self._store_results

    @store_results.setter
    def store_results(self, store_results):
        """Sets the store_results of this GenericUDF.

        store results for later retrieval

        :param store_results: The store_results of this GenericUDF.
        :type: bool
        """

        self._store_results = store_results

    @property
    def timeout(self):
        """Gets the timeout of this GenericUDF.

        UDF-type timeout in seconds (default: 900)

        :return: The timeout of this GenericUDF.
        :rtype: int
        """
        return self._timeout

    @timeout.setter
    def timeout(self, timeout):
        """Sets the timeout of this GenericUDF.

        UDF-type timeout in seconds (default: 900)

        :param timeout: The timeout of this GenericUDF.
        :type: int
        """

        self._timeout = timeout

    @property
    def dont_download_results(self):
        """Gets the dont_download_results of this GenericUDF.

        Set to true to avoid downloading the results of this UDF. Useful for intermediate nodes in a task graph where you will not be using the results of your function. Defaults to false (\"yes download results\").

        :return: The dont_download_results of this GenericUDF.
        :rtype: bool
        """
        return self._dont_download_results

    @dont_download_results.setter
    def dont_download_results(self, dont_download_results):
        """Sets the dont_download_results of this GenericUDF.

        Set to true to avoid downloading the results of this UDF. Useful for intermediate nodes in a task graph where you will not be using the results of your function. Defaults to false (\"yes download results\").

        :param dont_download_results: The dont_download_results of this GenericUDF.
        :type: bool
        """

        self._dont_download_results = dont_download_results

    @property
    def task_graph_uuid(self):
        """Gets the task_graph_uuid of this GenericUDF.

        If set, the ID of the log for the task graph that this was part of.

        :return: The task_graph_uuid of this GenericUDF.
        :rtype: str
        """
        return self._task_graph_uuid

    @task_graph_uuid.setter
    def task_graph_uuid(self, task_graph_uuid):
        """Sets the task_graph_uuid of this GenericUDF.

        If set, the ID of the log for the task graph that this was part of.

        :param task_graph_uuid: The task_graph_uuid of this GenericUDF.
        :type: str
        """

        self._task_graph_uuid = task_graph_uuid

    @property
    def client_node_uuid(self):
        """Gets the client_node_uuid of this GenericUDF.

        If set, the client-defined ID of the node within this task's graph.

        :return: The client_node_uuid of this GenericUDF.
        :rtype: str
        """
        return self._client_node_uuid

    @client_node_uuid.setter
    def client_node_uuid(self, client_node_uuid):
        """Sets the client_node_uuid of this GenericUDF.

        If set, the client-defined ID of the node within this task's graph.

        :param client_node_uuid: The client_node_uuid of this GenericUDF.
        :type: str
        """

        self._client_node_uuid = client_node_uuid

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
        if not isinstance(other, GenericUDF):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GenericUDF):
            return True

        return self.to_dict() != other.to_dict()
