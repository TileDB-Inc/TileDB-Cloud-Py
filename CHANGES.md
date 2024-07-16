# Changes

## Next (YYYY-MM-DD)

New features:

- Add a tiledb.cloud.asset module with functions that allow management of
  assets of any type. This module is exported from tiledb.cloud (gh-566,
  gh-577).

Bug fixes:

- Ensure that boolean recursive parameters in tiledb.cloud.asset and
  tiledb.cloud.groups are converted to "true" or "false" before server requests
  are made (gh-).
