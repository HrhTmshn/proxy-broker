# Proxy Broker

A Python-based script that collects free proxies from various sources, checks their availability, and outputs a text file with the working proxies.

#### Stack:

- [Python](https://www.python.org/downloads/)
- [Requests](https://docs.python-requests.org/en/latest/)
- [urllib3](https://pypi.org/project/urllib3/)
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
   python main.py 
   ```

## Output

The script will generate a text file containing a list of working proxies in the same directory.