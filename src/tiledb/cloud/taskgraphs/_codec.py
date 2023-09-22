# This file is only here for testing compatibility purposes.
# Nothing in it should be used outside of tests.
import base64


def b64_str(val: bytes) -> str:
    return base64.b64encode(val).decode("ascii")
