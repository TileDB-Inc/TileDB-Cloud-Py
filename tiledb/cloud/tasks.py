from . import client
from . import tiledb_cloud_error
from . import cloudarray
from .rest_api import ApiException as GenApiException

import datetime

last_task_id = None

def task(id=None):
  """
  Fetch a single array task
  :param str id: id to lookup, if unset will use the id of the last array task run in the current python session
  :return task : object with task details
  """

  if id is None and last_task_id is None:
    raise Exception("id parameter can not be None and there is no last run task")
  elif id is None and last_task_id is not None:
    id = last_task_id

  api_instance = client.get_tasks_api()

  try:
    return api_instance.task_id_get(id=id)

  except GenApiException as exc:
    raise tiledb_cloud_error.check_exc(exc) from None


def tasks(namespace=None, array=None, start=None, end=datetime.datetime.utcnow(), status=None):
  """
  Fetch all tasks a user has access too
  :param str namespace: optional filter by namespace
  :param str array: optional limit tasks to specific array
  :param datetime start: optional start time for listing of tasks, defaults to 7 days ago
  :param datetime end: optional end time for listing of tasks defaults to now
  :param str status: optional filter on status can be one of ['FAILED', 'RUNNING', 'COMPLETED']
  :return:
  """
  api_instance = client.get_tasks_api()

  if end is not None:
    if not isinstance(end, datetime.datetime):
      raise Exception("end must be datetime object")
    end = datetime.datetime.timestamp(end)

  if start is not None:
    if not isinstance(start, datetime.datetime):
      raise Exception("start must be datetime object")
    start = datetime.datetime.timestamp(start)

  if status is not None and status != "FAILED" and status != "RUNNING" and status != "COMPLETED":
    raise Exception("status must be one of ['FAILED', 'RUNNING', 'COMPLETED']")

  if array is not None:
    (namespace, array) = cloudarray.split_uri(array)

  try:
    return api_instance.tasks_get(namespace=namespace, array=array, start=start, end=end, status=status)

  except GenApiException as exc:
    raise tiledb_cloud_error.check_exc(exc) from None
