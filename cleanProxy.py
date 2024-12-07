import aiohttp
import asyncio
import os
import shutil
from aiohttp_socks import ProxyConnector

# URLs to get proxy lists
proxy_urls = {
    'http': [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/http.txt",
        "https://raw.githubusercontent.com/proxifly/free-proxy-list/refs/heads/main/proxies/protocols/http/data.txt",
        "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/http.txt",
        "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/refs/heads/main/proxies/http.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/refs/heads/master/http.txt",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/refs/heads/KangProxy/http/http.txt",
        "https://raw.githubusercontent.com/yemixzy/proxy-list/refs/heads/main/proxies/http.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/refs/heads/master/http.txt",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    ],
    'https': [
        "https://raw.githubusercontent.com/proxifly/free-proxy-list/refs/heads/main/proxies/protocols/https/data.txt",
        "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/https.txt",
        "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/refs/heads/main/proxies/https.txt",
        "https://github.com/mmpx12/proxy-list/raw/refs/heads/master/https.txt",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/refs/heads/KangProxy/https/https.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/refs/heads/master/https.txt",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=10000&country=all&ssl=all&anonymity=all"
    ],
    'socks4': [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/proxifly/free-proxy-list/refs/heads/main/proxies/protocols/socks4/data.txt",
        "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/socks4.txt",
        "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/refs/heads/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/refs/heads/master/socks4.txt",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/refs/heads/KangProxy/socks4/socks4.txt",
        "https://raw.githubusercontent.com/yemixzy/proxy-list/refs/heads/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/refs/heads/master/socks4.txt",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all&ssl=all&anonymity=all"
    ],
    'socks5': [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/proxifly/free-proxy-list/refs/heads/main/proxies/protocols/socks5/data.txt",
        "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/socks5.txt",
        "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/refs/heads/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/refs/heads/master/socks5.txt",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/refs/heads/KangProxy/socks5/socks5.txt",
        "https://raw.githubusercontent.com/yemixzy/proxy-list/refs/heads/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/refs/heads/master/socks5.txt",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all&ssl=all&anonymity=all"
    ]
}

# URL to validate proxies
test_url = "https://httpbin.org/ip"

# Headers to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

# Load proxies from a URL
async def get_proxies(url, proxy_type):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                proxies = await response.text()
                return [proxy.strip() for proxy in proxies.splitlines()]
            else:
                print(f"Failed to fetch proxies from {url}")
    return []

# Fetch all proxies from the URLs
async def get_all_proxies():
    all_proxies = {'http': [], 'https': [], 'socks4': [], 'socks5': []}
    tasks = []
    
    for proxy_type, urls in proxy_urls.items():
        for url in urls:
            tasks.append(get_proxies(url, proxy_type))

    results = await asyncio.gather(*tasks)

    idx = 0
    for proxy_type, urls in proxy_urls.items():
        for _ in urls:
            all_proxies[proxy_type].extend(results[idx])
            idx += 1

    return all_proxies

# Clean proxies to remove any headers like http://, https://, socks4://, socks5://
def clean_proxies(all_proxies):
    cleaned_proxies = {'http': [], 'https': [], 'socks4': [], 'socks5': []}
    for proxy_type, proxies in all_proxies.items():
        for proxy in proxies:
            cleaned_proxy = proxy.replace("http://", "").replace("https://", "").replace("socks4://", "").replace("socks5://", "")
            cleaned_proxies[proxy_type].append(cleaned_proxy)
    return cleaned_proxies

# Save all fetched proxies to a file
def save_all_proxies(all_proxies):
    with open("all_proxies.txt", "w") as file:
        for proxy_type, proxies in all_proxies.items():
            file.write(f"{proxy_type.upper()} Proxies:\n")
            for proxy in proxies:
                file.write(f"{proxy}\n")
            file.write("\n")
    print("All proxies saved to all_proxies.txt")

# Validate a single proxy by making a request to the test URL
async def check_proxy(proxy, proxy_type):
    try:
        if proxy_type == 'http' or proxy_type == 'https':
            proxy_url = f"http://{proxy}"
            async with aiohttp.ClientSession() as session:
                async with session.get(test_url, headers=headers, proxy=proxy_url, ssl=False) as response:
                    print(f"Proxy {proxy} Response: {response.status}")
                    if response.status == 200:
                        return True
        else:
            proxy_url = f"{proxy_type}://{proxy}"
            connector = ProxyConnector.from_url(proxy_url)
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(test_url, headers=headers, ssl=False) as response:
                    print(f"Proxy {proxy} Response: {response.status}")
                    if response.status == 200:
                        return True

    except Exception as e:
        with open("log.txt", "a") as log_file:
            log_file.write(f"Proxy {proxy} ({proxy_type}) failed: {str(e)}\n")
    return False

# Validate proxies and return only the valid ones
async def clean_and_validate_proxies(all_proxies):
    cleaned_proxies = clean_proxies(all_proxies)
    valid_proxies = {'http': [], 'https': [], 'socks4': [], 'socks5': []}
    
    tasks = []
    for proxy_type, proxies in cleaned_proxies.items():
        for proxy in proxies:
            tasks.append(check_proxy(proxy, proxy_type))

    results = await asyncio.gather(*tasks)

    idx = 0
    for proxy_type, proxies in cleaned_proxies.items():
        for proxy in proxies:
            if results[idx]:
                valid_proxies[proxy_type].append(proxy)
            idx += 1
    
    return valid_proxies

# Save the valid proxies to separate files
def save_valid_proxies(valid_proxies):
    with open("valid_http.txt", "w") as http_file, \
         open("valid_https.txt", "w") as https_file, \
         open("valid_socks4.txt", "w") as socks4_file, \
         open("valid_socks5.txt", "w") as socks5_file:

        for proxy in valid_proxies['http']:
            http_file.write(f"{proxy}\n")
        for proxy in valid_proxies['https']:
            https_file.write(f"{proxy}\n")
        for proxy in valid_proxies['socks4']:
            socks4_file.write(f"{proxy}\n")
        for proxy in valid_proxies['socks5']:
            socks5_file.write(f"{proxy}\n")

    print(f"Validation complete. Valid proxies saved.")

# Main function to get and clean proxies
async def main():
    print("Fetching proxies...")
    all_proxies = await get_all_proxies()
    print("Proxies fetched. Saving all proxies...")
    save_all_proxies(all_proxies)
    
    print("Cleaning and validating proxies...")
    valid_proxies = await clean_and_validate_proxies(all_proxies)
    
    print("Proxies validated.")
    save_valid_proxies(valid_proxies)

# Run the script
if __name__ == "__main__":
    asyncio.run(main())