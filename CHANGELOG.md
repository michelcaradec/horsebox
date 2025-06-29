# Change Log

*All notable changes to "horsebox" will be documented in this file.*  
*The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).*

## Known Issues

*NA*

## [Unreleased]

*NA*

## [0.6.0] - 2025-06-29

### Added

- New collector `pdf`, to process PDF documents.

### Changed

- The collection of the file by the file system collectors has been improved to support file patterns and names.

### Fixed

- The date of last modification of the files were not properly propagated by the file system collectors.
- Early exit when normalizing empty strings.
- Improve the display of the enumeration based values (string `txt` vs enumeration name `Format.TXT`).

## [0.5.0] - 2025-06-25

### Added

- New collector `guess`, to identify the best collector to use.
- Use of [Tox](https://tox.wiki/) for tests with multiple interpreters.

### Changed

- Return of the exit code `-1` on error.

## [0.4.0] - 2025-06-11

### Added

- Store build arguments to the index metadata.
- New command `refresh` to refresh an index.

### Fixed

- Improve index existence check.

## [0.3.0] - 2025-06-04

### Added

- Configuration `HB_TOP_MIN_CHARS` to set the minimum number of characters of a top keyword.

## [0.2.0] - 2025-05-24

### Added

- Support to [JSON Lines](https://jsonlines.org/) files with the collector `raw`.
- Change log document (`CHANGELOG.md`).

## [0.1.5] - 2025-05-20

### Fixed

- Restrict Click version under 8.2.0 - version 8.2.0 breaks the `is_flag` option - (#4).

## [0.1.4] - 2025-05-20

### Fixed

- Fix the use of enumerations with the type `Choice` of Click (#2).

## [0.1.3] - 2025-05-08

### Changed

- Extend the Python interpreter support to version 3.13.

## [0.1.2] - 2025-05-08

### Added

- Initial release.
