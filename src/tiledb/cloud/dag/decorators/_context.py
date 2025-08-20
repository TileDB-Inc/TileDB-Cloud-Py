"""Shared context variables for DAG decorators."""

from contextvars import ContextVar
from typing import Optional

from tiledb.cloud.dag import DAG

# context variable to hold the active (and potentially nested) DAG contexts.
_dag_context: ContextVar[Optional[DAG]] = ContextVar("current_dag")
