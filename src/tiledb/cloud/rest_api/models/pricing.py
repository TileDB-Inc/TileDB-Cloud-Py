# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.17.51
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from tiledb.cloud.rest_api.configuration import Configuration


class Pricing(object):
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
        "array_uuid": "str",
        "pricing_name": "str",
        "pricing_type": "PricingType",
        "product_name": "str",
        "product_statement_descriptor": "str",
        "product_unit_label": "PricingUnitLabel",
        "currency": "PricingCurrency",
        "aggregate_usage": "PricingAggregateUsage",
        "interval": "PricingInterval",
        "divided_by": "int",
        "charge": "float",
        "activated": "bool",
    }

    attribute_map = {
        "id": "id",
        "array_uuid": "array_uuid",
        "pricing_name": "pricing_name",
        "pricing_type": "pricing_type",
        "product_name": "product_name",
        "product_statement_descriptor": "product_statement_descriptor",
        "product_unit_label": "product_unit_label",
        "currency": "currency",
        "aggregate_usage": "aggregate_usage",
        "interval": "interval",
        "divided_by": "divided_by",
        "charge": "charge",
        "activated": "activated",
    }

    def __init__(
        self,
        id=None,
        array_uuid=None,
        pricing_name=None,
        pricing_type=None,
        product_name=None,
        product_statement_descriptor=None,
        product_unit_label=None,
        currency=None,
        aggregate_usage=None,
        interval=None,
        divided_by=None,
        charge=None,
        activated=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """Pricing - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._array_uuid = None
        self._pricing_name = None
        self._pricing_type = None
        self._product_name = None
        self._product_statement_descriptor = None
        self._product_unit_label = None
        self._currency = None
        self._aggregate_usage = None
        self._interval = None
        self._divided_by = None
        self._charge = None
        self._activated = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if array_uuid is not None:
            self.array_uuid = array_uuid
        if pricing_name is not None:
            self.pricing_name = pricing_name
        if pricing_type is not None:
            self.pricing_type = pricing_type
        if product_name is not None:
            self.product_name = product_name
        if product_statement_descriptor is not None:
            self.product_statement_descriptor = product_statement_descriptor
        if product_unit_label is not None:
            self.product_unit_label = product_unit_label
        if currency is not None:
            self.currency = currency
        if aggregate_usage is not None:
            self.aggregate_usage = aggregate_usage
        if interval is not None:
            self.interval = interval
        if divided_by is not None:
            self.divided_by = divided_by
        if charge is not None:
            self.charge = charge
        if activated is not None:
            self.activated = activated

    @property
    def id(self):
        """Gets the id of this Pricing.  # noqa: E501

        Unique ID of plan as defined by Stripe  # noqa: E501

        :return: The id of this Pricing.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Pricing.

        Unique ID of plan as defined by Stripe  # noqa: E501

        :param id: The id of this Pricing.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def array_uuid(self):
        """Gets the array_uuid of this Pricing.  # noqa: E501

        Unique ID of registered array  # noqa: E501

        :return: The array_uuid of this Pricing.  # noqa: E501
        :rtype: str
        """
        return self._array_uuid

    @array_uuid.setter
    def array_uuid(self, array_uuid):
        """Sets the array_uuid of this Pricing.

        Unique ID of registered array  # noqa: E501

        :param array_uuid: The array_uuid of this Pricing.  # noqa: E501
        :type: str
        """

        self._array_uuid = array_uuid

    @property
    def pricing_name(self):
        """Gets the pricing_name of this Pricing.  # noqa: E501

        Name of pricing  # noqa: E501

        :return: The pricing_name of this Pricing.  # noqa: E501
        :rtype: str
        """
        return self._pricing_name

    @pricing_name.setter
    def pricing_name(self, pricing_name):
        """Sets the pricing_name of this Pricing.

        Name of pricing  # noqa: E501

        :param pricing_name: The pricing_name of this Pricing.  # noqa: E501
        :type: str
        """

        self._pricing_name = pricing_name

    @property
    def pricing_type(self):
        """Gets the pricing_type of this Pricing.  # noqa: E501


        :return: The pricing_type of this Pricing.  # noqa: E501
        :rtype: PricingType
        """
        return self._pricing_type

    @pricing_type.setter
    def pricing_type(self, pricing_type):
        """Sets the pricing_type of this Pricing.


        :param pricing_type: The pricing_type of this Pricing.  # noqa: E501
        :type: PricingType
        """

        self._pricing_type = pricing_type

    @property
    def product_name(self):
        """Gets the product_name of this Pricing.  # noqa: E501

        Name of product  # noqa: E501

        :return: The product_name of this Pricing.  # noqa: E501
        :rtype: str
        """
        return self._product_name

    @product_name.setter
    def product_name(self, product_name):
        """Sets the product_name of this Pricing.

        Name of product  # noqa: E501

        :param product_name: The product_name of this Pricing.  # noqa: E501
        :type: str
        """

        self._product_name = product_name

    @property
    def product_statement_descriptor(self):
        """Gets the product_statement_descriptor of this Pricing.  # noqa: E501

        Extra information about a product which will appear on the credit card statement of the customer  # noqa: E501

        :return: The product_statement_descriptor of this Pricing.  # noqa: E501
        :rtype: str
        """
        return self._product_statement_descriptor

    @product_statement_descriptor.setter
    def product_statement_descriptor(self, product_statement_descriptor):
        """Sets the product_statement_descriptor of this Pricing.

        Extra information about a product which will appear on the credit card statement of the customer  # noqa: E501

        :param product_statement_descriptor: The product_statement_descriptor of this Pricing.  # noqa: E501
        :type: str
        """

        self._product_statement_descriptor = product_statement_descriptor

    @property
    def product_unit_label(self):
        """Gets the product_unit_label of this Pricing.  # noqa: E501


        :return: The product_unit_label of this Pricing.  # noqa: E501
        :rtype: PricingUnitLabel
        """
        return self._product_unit_label

    @product_unit_label.setter
    def product_unit_label(self, product_unit_label):
        """Sets the product_unit_label of this Pricing.


        :param product_unit_label: The product_unit_label of this Pricing.  # noqa: E501
        :type: PricingUnitLabel
        """

        self._product_unit_label = product_unit_label

    @property
    def currency(self):
        """Gets the currency of this Pricing.  # noqa: E501


        :return: The currency of this Pricing.  # noqa: E501
        :rtype: PricingCurrency
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this Pricing.


        :param currency: The currency of this Pricing.  # noqa: E501
        :type: PricingCurrency
        """

        self._currency = currency

    @property
    def aggregate_usage(self):
        """Gets the aggregate_usage of this Pricing.  # noqa: E501


        :return: The aggregate_usage of this Pricing.  # noqa: E501
        :rtype: PricingAggregateUsage
        """
        return self._aggregate_usage

    @aggregate_usage.setter
    def aggregate_usage(self, aggregate_usage):
        """Sets the aggregate_usage of this Pricing.


        :param aggregate_usage: The aggregate_usage of this Pricing.  # noqa: E501
        :type: PricingAggregateUsage
        """

        self._aggregate_usage = aggregate_usage

    @property
    def interval(self):
        """Gets the interval of this Pricing.  # noqa: E501


        :return: The interval of this Pricing.  # noqa: E501
        :rtype: PricingInterval
        """
        return self._interval

    @interval.setter
    def interval(self, interval):
        """Sets the interval of this Pricing.


        :param interval: The interval of this Pricing.  # noqa: E501
        :type: PricingInterval
        """

        self._interval = interval

    @property
    def divided_by(self):
        """Gets the divided_by of this Pricing.  # noqa: E501

        Group of n product unit labels  # noqa: E501

        :return: The divided_by of this Pricing.  # noqa: E501
        :rtype: int
        """
        return self._divided_by

    @divided_by.setter
    def divided_by(self, divided_by):
        """Sets the divided_by of this Pricing.

        Group of n product unit labels  # noqa: E501

        :param divided_by: The divided_by of this Pricing.  # noqa: E501
        :type: int
        """

        self._divided_by = divided_by

    @property
    def charge(self):
        """Gets the charge of this Pricing.  # noqa: E501

        Price in cents (decimal) per unitlabel  # noqa: E501

        :return: The charge of this Pricing.  # noqa: E501
        :rtype: float
        """
        return self._charge

    @charge.setter
    def charge(self, charge):
        """Sets the charge of this Pricing.

        Price in cents (decimal) per unitlabel  # noqa: E501

        :param charge: The charge of this Pricing.  # noqa: E501
        :type: float
        """

        self._charge = charge

    @property
    def activated(self):
        """Gets the activated of this Pricing.  # noqa: E501

        If pricing is activated  # noqa: E501

        :return: The activated of this Pricing.  # noqa: E501
        :rtype: bool
        """
        return self._activated

    @activated.setter
    def activated(self, activated):
        """Sets the activated of this Pricing.

        If pricing is activated  # noqa: E501

        :param activated: The activated of this Pricing.  # noqa: E501
        :type: bool
        """

        self._activated = activated

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
        if not isinstance(other, Pricing):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Pricing):
            return True

        return self.to_dict() != other.to_dict()
