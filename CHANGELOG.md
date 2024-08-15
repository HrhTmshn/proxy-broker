# Changelog

## [v_0.1.0] - 2024-08-15
### Added
- Implemented asynchronous proxy validation using aiohttp, significantly improving the speed of proxy checking.
- Added a limit argument (limit=<number>) to control the number of valid proxies returned.
- Introduced additional checks on proxy headers to ensure that the proxy does not pass the user's IP or indicate that a proxy is being used. Proxies failing this check are discarded.
- Improved uniqueness of the proxy list by eliminating duplicates after fetching from multiple sources.

## [v_0.0.0] - 2024-08-15
### Init
- Initial commit. Set up project structure, added basic files and initial configuration.