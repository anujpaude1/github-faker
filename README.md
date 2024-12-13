# GitHub Faker

GitHub Faker is a Python project designed to automate profile views using proxies. It fetches, cleans, and validates proxy lists from various sources and uses them to send requests to a specified URL.

## Features

- Fetches proxy lists from multiple sources.
- Cleans and validates proxies.
- Uses valid proxies to automate profile views.
- Supports HTTP, HTTPS, SOCKS4, and SOCKS5 proxies.

## Requirements

- Python 3.7+
- `aiohttp`
- `aiohttp-socks`
- `gitpython`

Install the required packages using:
```sh
pip install -r requirements.txt
```

## Usage

1. **Fetch and Validate Proxies:**

    Run the `cleanProxy.py` script to fetch, clean, and validate proxies:
    ```sh
    python cleanProxy.py
    ```

    This will save the valid proxies to `valid_http.txt`, `valid_https.txt`, `valid_socks4.txt`, and `valid_socks5.txt`.

2. **Automate Profile Views:**

    Run the `profileViews.py` script to start sending requests using the valid proxies:
    ```sh
    python profileViews.py
    ```

## File Structure

- `cleanProxy.py`: Script to fetch, clean, and validate proxies.
- `profileViews.py`: Script to automate profile views using valid proxies.
- `requirements.txt`: List of required Python packages.
- `valid_http.txt`, `valid_https.txt`, `valid_socks4.txt`, `valid_socks5.txt`: Files containing valid proxies.
- `.gitignore`: Git ignore file to exclude unnecessary files from the repository.

## License

This project is licensed under the MIT License.

## Disclaimer

This project is for educational purposes only. Use it responsibly and do not violate any terms of service.
