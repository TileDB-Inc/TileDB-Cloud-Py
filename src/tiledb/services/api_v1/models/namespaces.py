from enum import Enum


class NamespaceActions(str, Enum):
    READ = "read"
    WRITE = "write"
    CREATE = "create"
    DELETE = "delete"
    EDIT = "edit"
    READ_ARRAY_LOGS = "read_array_logs"
    READ_JOB_LOGS = "read_job_logs"
    READ_OBJECT_LOGS = "read_object_logs"
    RUN_JOB = "run_job"
    DELETE_ORGANIZATION = "delete_organization"
    EDIT_ORGANIZATION = "edit_organization"
    EDIT_BILLING = "edit_billing"
