"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.2.19
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from tiledb.cloud.rest_api.exceptions import ApiAttributeError
from tiledb.cloud.rest_api.model_utils import ApiTypeError  # noqa: F401
from tiledb.cloud.rest_api.model_utils import ModelComposed
from tiledb.cloud.rest_api.model_utils import ModelNormal
from tiledb.cloud.rest_api.model_utils import ModelSimple
from tiledb.cloud.rest_api.model_utils import cached_property
from tiledb.cloud.rest_api.model_utils import change_keys_js_to_python
from tiledb.cloud.rest_api.model_utils import convert_js_args_to_python_args
from tiledb.cloud.rest_api.model_utils import date
from tiledb.cloud.rest_api.model_utils import datetime
from tiledb.cloud.rest_api.model_utils import file_type
from tiledb.cloud.rest_api.model_utils import none_type
from tiledb.cloud.rest_api.model_utils import validate_get_composed_info

from ..model_utils import OpenApiModel


def lazy_import():
    from tiledb.cloud.rest_api.model.pricing_aggregate_usage import (
        PricingAggregateUsage,
    )
    from tiledb.cloud.rest_api.model.pricing_currency import PricingCurrency
    from tiledb.cloud.rest_api.model.pricing_interval import PricingInterval
    from tiledb.cloud.rest_api.model.pricing_type import PricingType
    from tiledb.cloud.rest_api.model.pricing_unit_label import PricingUnitLabel

    globals()["PricingAggregateUsage"] = PricingAggregateUsage
    globals()["PricingCurrency"] = PricingCurrency
    globals()["PricingInterval"] = PricingInterval
    globals()["PricingType"] = PricingType
    globals()["PricingUnitLabel"] = PricingUnitLabel


class Pricing(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {}

    validations = {}

    @cached_property
    def additional_properties_type():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded
        """
        lazy_import()
        return (
            bool,
            date,
            datetime,
            dict,
            float,
            int,
            list,
            str,
            none_type,
        )  # noqa: E501

    _nullable = False

    @cached_property
    def openapi_types():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        lazy_import()
        return {
            "id": (str,),  # noqa: E501
            "array_uuid": (str,),  # noqa: E501
            "pricing_name": (str,),  # noqa: E501
            "pricing_type": (PricingType,),  # noqa: E501
            "product_name": (str,),  # noqa: E501
            "product_statement_descriptor": (str,),  # noqa: E501
            "product_unit_label": (PricingUnitLabel,),  # noqa: E501
            "currency": (PricingCurrency,),  # noqa: E501
            "aggregate_usage": (PricingAggregateUsage,),  # noqa: E501
            "interval": (PricingInterval,),  # noqa: E501
            "divided_by": (int,),  # noqa: E501
            "charge": (float,),  # noqa: E501
            "activated": (bool,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None

    attribute_map = {
        "id": "id",  # noqa: E501
        "array_uuid": "array_uuid",  # noqa: E501
        "pricing_name": "pricing_name",  # noqa: E501
        "pricing_type": "pricing_type",  # noqa: E501
        "product_name": "product_name",  # noqa: E501
        "product_statement_descriptor": "product_statement_descriptor",  # noqa: E501
        "product_unit_label": "product_unit_label",  # noqa: E501
        "currency": "currency",  # noqa: E501
        "aggregate_usage": "aggregate_usage",  # noqa: E501
        "interval": "interval",  # noqa: E501
        "divided_by": "divided_by",  # noqa: E501
        "charge": "charge",  # noqa: E501
        "activated": "activated",  # noqa: E501
    }

    read_only_vars = {}

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, *args, **kwargs):  # noqa: E501
        """Pricing - a model defined in OpenAPI

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            id (str): Unique ID of plan as defined by Stripe. [optional]  # noqa: E501
            array_uuid (str): Unique ID of registered array. [optional]  # noqa: E501
            pricing_name (str): Name of pricing. [optional]  # noqa: E501
            pricing_type (PricingType): [optional]  # noqa: E501
            product_name (str): Name of product. [optional]  # noqa: E501
            product_statement_descriptor (str): Extra information about a product which will appear on the credit card statement of the customer. [optional]  # noqa: E501
            product_unit_label (PricingUnitLabel): [optional]  # noqa: E501
            currency (PricingCurrency): [optional]  # noqa: E501
            aggregate_usage (PricingAggregateUsage): [optional]  # noqa: E501
            interval (PricingInterval): [optional]  # noqa: E501
            divided_by (int): Group of n product unit labels. [optional]  # noqa: E501
            charge (float): Price in cents (decimal) per unitlabel. [optional]  # noqa: E501
            activated (bool): If pricing is activated. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop("_check_type", True)
        _spec_property_naming = kwargs.pop("_spec_property_naming", False)
        _path_to_item = kwargs.pop("_path_to_item", ())
        _configuration = kwargs.pop("_configuration", None)
        _visited_composed_classes = kwargs.pop("_visited_composed_classes", ())

        self = super(OpenApiModel, cls).__new__(cls)

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments."
                % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        for var_name, var_value in kwargs.items():
            if (
                var_name not in self.attribute_map
                and self._configuration is not None
                and self._configuration.discard_unknown_keys
                and self.additional_properties_type is None
            ):
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self

    required_properties = set(
        [
            "_data_store",
            "_check_type",
            "_spec_property_naming",
            "_path_to_item",
            "_configuration",
            "_visited_composed_classes",
        ]
    )

    @convert_js_args_to_python_args
    def __init__(self, *args, **kwargs):  # noqa: E501
        """Pricing - a model defined in OpenAPI

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            id (str): Unique ID of plan as defined by Stripe. [optional]  # noqa: E501
            array_uuid (str): Unique ID of registered array. [optional]  # noqa: E501
            pricing_name (str): Name of pricing. [optional]  # noqa: E501
            pricing_type (PricingType): [optional]  # noqa: E501
            product_name (str): Name of product. [optional]  # noqa: E501
            product_statement_descriptor (str): Extra information about a product which will appear on the credit card statement of the customer. [optional]  # noqa: E501
            product_unit_label (PricingUnitLabel): [optional]  # noqa: E501
            currency (PricingCurrency): [optional]  # noqa: E501
            aggregate_usage (PricingAggregateUsage): [optional]  # noqa: E501
            interval (PricingInterval): [optional]  # noqa: E501
            divided_by (int): Group of n product unit labels. [optional]  # noqa: E501
            charge (float): Price in cents (decimal) per unitlabel. [optional]  # noqa: E501
            activated (bool): If pricing is activated. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop("_check_type", True)
        _spec_property_naming = kwargs.pop("_spec_property_naming", False)
        _path_to_item = kwargs.pop("_path_to_item", ())
        _configuration = kwargs.pop("_configuration", None)
        _visited_composed_classes = kwargs.pop("_visited_composed_classes", ())

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments."
                % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        for var_name, var_value in kwargs.items():
            if (
                var_name not in self.attribute_map
                and self._configuration is not None
                and self._configuration.discard_unknown_keys
                and self.additional_properties_type is None
            ):
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(
                    f"`{var_name}` is a read-only attribute. Use `from_openapi_data` to instantiate "
                    f"class with read only attributes."
                )
