# Proxy Broker

A Python-based script that collects free proxies from various sources, checks their availability, and outputs a text file with the working proxies.

#### Stack:

- [Python 3.7.9](https://www.python.org/downloads/)
- [aiohttp](https://docs.aiohttp.org/)
- [Requests](https://docs.python-requests.org/)
- [fake_useragent](https://pypi.org/project/fake-useragent/)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [lxml](https://pypi.org/project/lxml/)
- [colorama](https://pypi.org/project/colorama/)

## Local Developing

All actions should be executed from the source directory of the project and only after installing all requirements.

1. Firstly, create and activate a new virtual environment:
   ```bash
   python -m venv .\venv           # Default
   py -3.7 -m venv .\venv          # If Python 3.7 is installed separately
   .\venv\Scripts\activate
   ```

2. Install packages:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Run the script:
   ```bash
   python main.py [--no-refresh] [--limit <number>] [--queue-quota <int>] [--coeff-delay <int>] [--timeout <sec>]
   ```

   - `--no-refresh`: Skip downloading new proxies and use existing `proxy.txt`.
   - `--limit`: Maximum number of valid proxies to collect.
   - `--queue-quota`: Number of proxies processed in one batch before delaying.
   - `--coeff-delay`: Throttling factor to avoid overloading servers.
   - `--timeout`: Timeout in seconds for checking each proxy.

## Output

Two text files will be created in the current directory:

   - `proxy.txt`: List of all collected proxies.
   - `valid_proxies.txt`: Proxies that passed all validation checks (IP masking + no bad headers).