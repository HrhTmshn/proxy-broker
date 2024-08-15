import aiohttp
import asyncio
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import sys
import requests
from datetime import datetime


MAX_VALID_PROXIES = 100


def save_list_to_file(path):
    def intercept_result(function):
        def wrapper(*args, **kwargs):
            resault = function(*args, **kwargs)
            save_list = '\n'.join(resault)
            with open(path, 'w') as file:
                file.write(save_list)
            return resault
        return wrapper
    return intercept_result


@save_list_to_file('proxy.txt')
def get_proxylist(urls):
    with requests.Session() as session:
        user = UserAgent().random
        session.headers.update({'user-agent': user})
        response = session.get(urls[0])
        soup = BeautifulSoup(response.text, 'lxml')
        textarea = soup.find('textarea', class_='form-control').text
        proxy_list = textarea.splitlines()[3:]
        response = session.get(urls[1])
        proxy_list += response.text.splitlines()
        proxy_list = list(set(proxy_list))
    return proxy_list


def get_ip(url):
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    data = soup.find('pre').text.strip().splitlines()
    ip = data[0].split()[1]
    return ip


async def get_ip_headers_async(session, url, index_proxy, proxy, queue_quota=20, coeff_delay=20):
    try:
        await asyncio.sleep(index_proxy//queue_quota/coeff_delay)
        async with session.get(url, proxy=f'http://{proxy}', timeout=5) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            data = soup.find('pre').text.strip().splitlines()
            headers = {}
            for line in data[2:]:
                k, v = line.split(' = ')
                headers[k] = v
    except Exception:
        headers = None
    return proxy, headers


async def get_valid_proxies(url, proxy_base, my_ip):
    bad_headers_set = {
        'VIA', 'PROXY-CONNECTION', 'X-FORWARDED', 'X-FORWARDED-FOR',
        'FORWARDED', 'FORWARDED-FOR', 'FORWARDED-FOR-IP', 'CLIENT-IP'
    }
    valid_proxies = []

    limit = int(next((arg.split('=')[1] for arg in sys.argv if arg.startswith(
        'limit')), f'{len(proxy_base)}'))

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        tasks = [get_ip_headers_async(session, url, index_proxy, proxy)
                 for index_proxy, proxy in enumerate(proxy_base)]

        results = await asyncio.gather(*tasks)

        for ip, headers in results:
            if ip and (not ip.startswith(my_ip)) and headers:
                headers_set = {k.upper() for k in headers.keys()}
                if not (headers_set & bad_headers_set):
                    valid_proxies.append(ip)
                    limit -= 1
                    if limit <= 0:
                        break
    return valid_proxies


async def main():
    proxy_judge_url = 'https://pool.proxyspace.pro/judge.php'
    if '-upb' in sys.argv:
        urls = [
            'https://free-proxy-list.net/',
            'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt'
        ]
        proxy_base = get_proxylist(urls)
    else:
        with open('proxy.txt') as f:
            proxy_base = f.read().strip().split('\n')

    my_ip = get_ip(proxy_judge_url)

    start = datetime.now()
    valid_proxies = await get_valid_proxies(proxy_judge_url, proxy_base, my_ip)
    with open('valid_proxies.txt', 'w') as file:
        file.write('\n'.join(valid_proxies))
    print(datetime.now()-start)

if __name__ == '__main__':
    asyncio.run(main())
