# DB API 2.0 Connector

This package features the TileDB-Cloud-PythonDB connector, which aligns with the Python DB API 2.0 specification. It offers a convenient way for Python developers to connect to TileDB-Cloud and perform all necessary operations.
This can also be seen as an alternative to a JDBC or ODBC driver.

## Usage

```python
from tiledb.cloud.sql.tiledb_connection import TileDBConnection

connection = TileDBConnection()
cursor = connection.cursor()
cursor.execute("SELECT * from `tiledb://TileDB-Inc/quickstart_dense`")

row = cursor.fetchone()
while row:
    print(row)
    row = cursor.fetchone()

print(cursor.description())

```
