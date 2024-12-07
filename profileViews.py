import aiohttp
import asyncio
import random
from aiohttp_socks import SocksConnector,ProxyConnector

# URL to send requests to
url = "https://camo.githubusercontent.com/f2f1fb08fd0b8de640f486ee90d8541b8cd51ba0d180433d207668d06a0d80d0/68747470733a2f2f6b6f6d617265762e636f6d2f67687076632f3f757365726e616d653d616e756a706175646531266c6162656c3d50726f66696c65253230766965777326636f6c6f723d306537356236267374796c653d666c6174"
# url = "https://camo.githubusercontent.com/d2496cacaa813e840bb90610bf0d08ff16e776603a5a13903c91d66f69f6f46a/68747470733a2f2f6b6f6d617265762e636f6d2f67687076632f3f757365726e616d653d667579616c61736d6974266c6162656c3d50726f66696c65253230766965777326636f6c6f723d306537356236267374796c653d666c6174"
# Headers to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

# Load validated proxies from files
def load_valid_proxies():
    valid_http = load_proxies("valid_http.txt")
    valid_socks4 = load_proxies("valid_socks4.txt")
    valid_socks5 = load_proxies("valid_socks5.txt")
    return [(proxy, 'http') for proxy in valid_http] + \
           [(proxy, '4') for proxy in valid_socks4] + \
           [(proxy, '5') for proxy in valid_socks5]

def load_proxies(file_path):
    try:
        with open(file_path, "r") as file:
            return [proxy.strip() for proxy in file.readlines()]
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []

async def make_request_loop(proxy, proxy_type):
    """
    Loop requests through a single proxy.
    """
    while True:
        try:
            if proxy_type == 'http' or proxy_type == 'https':
                proxy_url = f"http://{proxy}"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers, proxy=proxy_url, ssl=False) as response:
                        print(f"Proxy {proxy} Response: {response.status}")
            else:
                proxy_url = f"socks{proxy_type}://{proxy}"
                connector = ProxyConnector.from_url(proxy_url)
                async with aiohttp.ClientSession(connector=connector) as session:
                    async with session.get(url, headers=headers,ssl=False) as response:
                        print(f"Proxy {proxy} Response: {response.status}")
        except Exception as e:
            print(f"Request through proxy {proxy} failed: {e}")

async def main():
    # Load proxies
    valid_proxies = load_valid_proxies()
    if not valid_proxies:
        print("No valid proxies found. Exiting.")
        return

    # Create tasks for each proxy
    tasks = []
    for proxy, proxy_type in valid_proxies:
        tasks.append(make_request_loop(proxy, proxy_type))  # Loop requests for each proxy

    # Run all tasks concurrently
    await asyncio.gather(*tasks)

# Run the script
if __name__ == "__main__":
    asyncio.run(main())
