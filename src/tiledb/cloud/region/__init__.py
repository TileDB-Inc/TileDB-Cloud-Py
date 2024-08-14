class AWS:
    """
    The AWS cloud regions that are currently supported.

    US_EAST_1 = North America, United States (Virginia)

    US_WEST_2 = North America, United States (Oregon)

    EU_WEST_1 = Europe, Ireland

    EU_WEST_2 = Europe, London

    AP_SOUTHEAST_1 = Asia, Singapore
    """

    US_EAST_1 = "https://us-east-1.aws.api.tiledb.com"
    US_WEST_2 = "https://us-west-2.aws.api.tiledb.com"
    EU_WEST_1 = "https://eu-west-1.aws.api.tiledb.com"
    EU_WEST_2 = "https://eu-west-2.aws.api.tiledb.com"
    AP_SOUTHEAST_1 = "https://ap-southeast-1.aws.api.tiledb.com"


__all__ = ("AWS",)
