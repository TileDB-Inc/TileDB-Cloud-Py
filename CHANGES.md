# Changes

## v0.12.27 (2024-09-25)

The key feature of this release is a workaround for a regression introduced in tiledb version 0.32 (gh-656).

## v0.12.26 (2024-09-17)

This release fixes a type hinting bug introduced in version 0.12.25 (#647).

## v0.12.25 (2024-09-16)

New features:

- Assets of a namespace can be listed in a paged fashion (gh-642).

Bug fixes:

- A race condition in SOMA ingestion and registration has been fixed (gh-643).
- Large file uploads are made more reliable by navigating redirects before uploading (gh-645).

## v0.12.24 (2024-09-12)

New features:

- A new tiledb.cloud.vcf module provides methods for splitting multisample VCFs (gh-616).
- SOMA ingestion now allows the option to set a name for registration that may be different from the source file name (gh-640).

Bug fixes:

- File upload now uses the proper Files API endpoint instead of Notebooks API endpoint (gh-634).
- Handling of unsorted VCF files has been improved (gh-636).
- Broken organization invitation has been fixed (gh-637).

## v0.12.23 (2024-08-09)

New features:

- Registration of assets, arrays, groups, notebooks, etc, can use a destination tiledb URI instead of namespace and name (gh-627).

Bug fixes:

- SOMA ingestion access credentials can now be passed using a more reliable acn argument (gh-630).
