# Proxy Broker

A Python-based script that collects free proxies from various sources, checks their availability, and outputs a text file with the working proxies.

#### Stack:

- [Python](https://www.python.org/downloads/)
- [aiohttp](https://docs.aiohttp.org/)
- [Requests](https://docs.python-requests.org/)
- [fake_useragent](https://pypi.org/project/fake-useragent/)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [lxml](https://pypi.org/project/lxml/)

## Local Developing

All actions should be executed from the source directory of the project and only after installing all requirements.

1. Firstly, create and activate a new virtual environment:
   ```bash
   python3.7 -m venv venv
   .\venv\Scripts\activate
   ```

2. Install packages:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Run the script:
   ```bash
   python main.py [-upb] [limit=<number>]
   ```

   - `-upb`: Update the proxy list by fetching fresh proxies from the sources.
   - `limit=<number>`: Limit the number of valid proxies returned.

## Output

The script will generate two text files in the same directory:

   - `proxy.txt`: A list of all collected proxies.
   - `valid_proxies.txt`: A list of working proxies that passed all checks.