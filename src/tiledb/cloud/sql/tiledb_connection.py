from tiledb.cloud.sql.tiledb_cursor import Cursor


class TileDBConnection:
    def cursor(self):
        return Cursor()

    def commit(self):
        # Commit must work, even if it doesn't do anything
        # No rollback method due to no transaction support
        pass

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass
