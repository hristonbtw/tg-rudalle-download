import os
import python_socks
import random
def get_proxy():
    with open(f'proxies.txt') as file:
        proxy_list = file.read().split('\n')
        chosen_proxy = random.choice(proxy_list)
        proxy_type = 'http'
        if proxy_type.lower() == 'socks5':
            proxy = chosen_proxy.split(':')
            if len(proxy) == 2:
                ip = proxy[0]
                port = int(proxy[1])
                return python_socks.ProxyType.SOCKS5, ip, port
            ip = proxy[0]
            port = int(proxy[1])
            username = proxy[2]
            password = proxy[3]
            return python_socks.ProxyType.SOCKS5, ip, port, True, username, password

        else:
            proxy = chosen_proxy.split(':')
            if len(proxy) == 2:
                ip = proxy[0]
                port = int(proxy[1])
                return python_socks.ProxyType.HTTP, ip, port
            ip = proxy[0]
            port = int(proxy[1])
            username = proxy[2]
            password = proxy[3]
            return python_socks.ProxyType.HTTP, ip, port, True, username, password