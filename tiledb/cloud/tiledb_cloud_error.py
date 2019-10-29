class TileDBClientError(BaseException):
  pass

def check_exc(exc):
  internal_err_msg = '[InternalError: failed to parse or message missing from ApiException]'

  if not isinstance(exc, BaseException):
    raise Exception(internal_err_msg)

  try:
    body = json.loads(exc.body)
    new_exc = TileDBClientError(body['message'])
  except:
    raise Exception(internal_err_msg) from exc

  return new_exc