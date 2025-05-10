import asyncio
from asyncio import TimeoutError
from aiohttp import ClientSession, TCPConnector, ClientError
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pathlib import Path
from colorama import init as colorama_init, Fore
from datetime import datetime


class ProxyBroker:
    def __init__(
            self,
            should_refresh_proxies: bool = True,
            limit: int = None,
            proxyfile_name: str = 'proxy.txt',
            valid_proxiesfile_name: str = 'valid_proxies.txt',
            queue_quota:int = 20,
            coeff_delay:int = 20,
            timeout:int = 5
        ):
        self.proxyfile_path = Path(proxyfile_name)
        self.valid_proxiesfile_path = Path(valid_proxiesfile_name)
        self.should_refresh_proxies = should_refresh_proxies
        self.limit = limit
        self.queue_quota = queue_quota
        self.coeff_delay = coeff_delay
        self.timeout = timeout

        self.url_for_my_ip = 'https://pool.proxyspace.pro/judge.php'
        self.bad_headers_set = {
            'VIA', 'PROXY-CONNECTION', 'X-FORWARDED', 'X-FORWARDED-FOR',
            'FORWARDED', 'FORWARDED-FOR', 'FORWARDED-FOR-IP', 'CLIENT-IP'
        }

        colorama_init(autoreset=True)

    def _save_list_to_file(self, data_list: list, file_path: Path):
        save_list = '\n'.join(data_list)
        with file_path.open('w', encoding="utf-8") as file:
            file.write(save_list)

        print(f"{Fore.LIGHTCYAN_EX}File {file_path.name} saved to: {file_path.absolute()}")

    def _get_my_ip(self):
        response = requests.get(self.url_for_my_ip)
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find('pre').text.strip().splitlines()
        self.my_ip = data[0].split()[1]
        print(f"{Fore.LIGHTYELLOW_EX}Your IP: {self.my_ip}")

    def _get_proxylist(self):
        self.proxy_list = []
        if self.proxyfile_path.exists():
            with self.proxyfile_path.open('r', encoding='utf-8') as f:
                self.proxy_list = f.read().strip().split('\n')
            
            if self.should_refresh_proxies == False:
                return

        with requests.Session() as session:
            user = UserAgent().random
            session.headers.update({'user-agent': user})
            
            print(f"{Fore.LIGHTMAGENTA_EX}Proxy List before parse: {len(self.proxy_list)} proxy")

            url = 'https://free-proxy-list.net/'
            response = session.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            textarea = soup.find('textarea', class_='form-control').text
            self.proxy_list += textarea.splitlines()[3:]

            url = 'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt'
            response = session.get(url)
            self.proxy_list += response.text.splitlines()
            
        self.proxy_list = list(set(self.proxy_list))
        print(f"{Fore.LIGHTGREEN_EX}Proxy List after parse: {len(self.proxy_list)} proxy")
        
        self._save_list_to_file(self.proxy_list, self.proxyfile_path)

    async def _get_ip_headers_async(
            self,
            session:ClientSession,
            index_proxy:int,
            proxy:str
        ) -> tuple:
        try:
            if self.queue_quota and self.coeff_delay:
                await asyncio.sleep((index_proxy//self.queue_quota)/self.coeff_delay)
            async with session.get(
                self.url_for_my_ip,
                proxy=f'http://{proxy}',
                timeout=self.timeout
            ) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')
                data = soup.find('pre').text.strip().splitlines()
                headers = {}
                for line in data[2:]:
                    k, v = line.split(' = ')
                    headers[k] = v
        except (ClientError, TimeoutError):
            headers = None
        return proxy, headers
    
    async def _get_valid_proxies(self):
        self.valid_proxies = []

        if self.limit == None:
            self.limit = len(self.proxy_list)
        elif self.limit <= 0:
            return

        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            tasks = [self._get_ip_headers_async(session, index_proxy, proxy)
                     for index_proxy, proxy in enumerate(self.proxy_list)]

            results = await asyncio.gather(*tasks)
            
            for proxy, headers in results:
                if proxy and (not proxy.startswith(self.my_ip)) and headers:
                    headers_set = {k.upper() for k in headers.keys()}
                    if not (headers_set & self.bad_headers_set):
                        self.valid_proxies.append(proxy)
                        self.limit -= 1
                        if self.limit <= 0:
                            break
            print(f"{Fore.LIGHTMAGENTA_EX}Valid proxies List: {len(self.valid_proxies)} proxy")

        self._save_list_to_file(self.valid_proxies, self.valid_proxiesfile_path)

    def run(self):
        start = datetime.now()

        self._get_my_ip()        
        self._get_proxylist()
        asyncio.run(self._get_valid_proxies())

        duration = datetime.now()-start
        print(f"{Fore.LIGHTMAGENTA_EX}Execution time: {duration.total_seconds():.2f} sec")