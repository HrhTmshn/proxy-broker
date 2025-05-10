# Changelog

## [v_0.2.0] - 2025-05-10
### Changed
- Project structure was refactored: logic moved to `core.py` inside a new `proxybroker` package, and entry point created as `main.py`.
- Replaced positional args with argparse-based CLI, supporting multiple new flags.
- Introduced throttling logic with `queue_quota` and `coeff_delay` to manage validation rate.

### Fixed
- Proper timeout and exception handling added using `asyncio.TimeoutError` and `aiohttp.ClientError`.

### Improved
- Refined header-checking mechanism with a set of forbidden keys.
- Improved printed output with `colorama` for better visibility in terminal.
- Now prints execution time and clearly indicates where output files are saved.

## [v_0.1.0] - 2024-08-15
### Added
- Implemented asynchronous proxy validation using aiohttp, significantly improving the speed of proxy checking.
- Added a limit argument (limit=<number>) to control the number of valid proxies returned.
- Introduced additional checks on proxy headers to ensure that the proxy does not pass the user's IP or indicate that a proxy is being used. Proxies failing this check are discarded.
- Improved uniqueness of the proxy list by eliminating duplicates after fetching from multiple sources.

## [v_0.0.0] - 2024-08-15
### Init
- Initial commit. Set up project structure, added basic files and initial configuration.