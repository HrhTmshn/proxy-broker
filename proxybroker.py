import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import sys


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
    return proxy_list


def get_ip_headers(url, proxy=None):
    if proxy:
        proxies = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
    else:
        proxies = None
    try:
        response = requests.get(url=url, proxies=proxies, timeout=2)
    except Exception:
        headers = None
    else:
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find('pre').text.strip().splitlines()
        ip = data[0].split()[1]
        headers = {}
        for line in data[2:]:
            k, v = line.split(' = ')
            headers[k] = v
    return (proxy, headers) if proxy else ip


@save_list_to_file('valid_proxies.txt')
def get_valid_proxies(url, proxy_base, my_ip):
    bad_headers_set = {
        'VIA', 'PROXY-CONNECTION', 'X-FORWARDED', 'X-FORWARDED-FOR',
        'FORWARDED', 'FORWARDED-FOR', 'FORWARDED-FOR-IP', 'CLIENT-IP'
    }
    valid_proxies = []
    for proxy in proxy_base:
        ip, headers = get_ip_headers(url, proxy)
        if (not ip.startswith(my_ip)) and headers:
            headers_set = {k.upper() for k in headers.keys()}
            if headers_set & bad_headers_set:
                continue
            valid_proxies.append(ip)
    return valid_proxies


def main():
    proxy_judge_url = 'https://pool.proxyspace.pro/judge.php'

    if 'update_proxy_file' in sys.argv:
        urls = [
            'https://free-proxy-list.net/',
            'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt'
        ]
        proxy_base = get_proxylist(urls)
    else:
        with open('proxy.txt') as f:
            proxy_base = f.read().strip().split('\n')

    my_ip = get_ip_headers(proxy_judge_url)

    _ = get_valid_proxies(proxy_judge_url, proxy_base, my_ip)


if __name__ == '__main__':
    main()
