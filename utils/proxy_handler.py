"""
ProxyChecker Module

This module provides functionality for checking and managing proxies.

Usage:
1. Import the ProxyChecker class:
   from proxy_checker import ProxyChecker

2. Create an instance of ProxyChecker with the path to your replacement proxy file:
   checker = ProxyChecker("replacement_proxies.txt")

3. Use the check_and_replace_proxy method to check a proxy and get a working one:
   working_proxy = checker.check_and_replace_proxy("user:pass@ip:port", "https://example.com")

The module will check the given proxy, and if it doesn't work, it will return a working
replacement proxy from the replacement file. The returned proxy will be removed from
the replacement file.
"""

import requests
from typing import Optional

from data.config import PROXY_TIMEOUT_FOR_CHECKER

class ProxyChecker:
    """
    A class for checking and managing proxies.

    Attributes:
        replacement_file (str): Path to the file containing replacement proxies.
    """

    def __init__(self, replacement_file: str):
        """
        Initialize the ProxyChecker with the replacement proxy file.

        Args:
            replacement_file (str): Path to the file containing replacement proxies.
        """
        self.replacement_file = replacement_file
        self.replacement_proxies = self.load_proxies(replacement_file)

    @staticmethod
    def load_proxies(file_path: str) -> list:
        """Load proxies from a file."""
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]

    @staticmethod
    def format_proxy(proxy: str) -> dict:
        """Format the proxy string into a dictionary for requests library."""
        parts = proxy.split('@')
        auth, ip_port = parts[0], parts[1]
        username, password = auth.split(':')
        ip, port = ip_port.split(':')
        return {
            "http": f"http://{username}:{password}@{ip}:{port}",
            "https": f"http://{username}:{password}@{ip}:{port}"
        }

    def check_connection(self, url: str, proxy: str, timeout: int = PROXY_TIMEOUT_FOR_CHECKER) -> bool:
        """Check if a proxy can connect to the specified URL."""
        formatted_proxy = self.format_proxy(proxy)
        try:
            response = requests.get(url, proxies=formatted_proxy, timeout=timeout)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def get_replacement_proxy(self) -> Optional[str]:
        """Get a replacement proxy from the replacement file."""
        if not self.replacement_proxies:
            return None
        proxy = self.replacement_proxies.pop()
        self.update_replacement_file()
        return proxy

    def update_replacement_file(self):
        """Update the replacement proxy file after removing a proxy."""
        with open(self.replacement_file, 'w') as file:
            for proxy in self.replacement_proxies:
                file.write(f"{proxy}\n")

    def check_and_replace_proxy(self, proxy: str, url: str) -> Optional[str]:
        """
        Check a proxy and replace it if necessary.

        Args:
            proxy (str): The proxy to check in format "user:pass@ip:port".
            url (str): The URL to test the proxy against.

        Returns:
            Optional[str]: A working proxy (either the original or a replacement),
                        or None if no working proxy is found.
        """
        if self.check_connection(url, proxy):
            return proxy
        
        while True:
            replacement_proxy = self.get_replacement_proxy()
            if not replacement_proxy:
                return None
            
            if self.check_connection(url, replacement_proxy):
                # Double-check the replacement proxy
                if self.check_connection(url, replacement_proxy):
                    return replacement_proxy
                else:
                    # If the second check fails, continue the loop to get another replacement
                    continue

# The following code will only run if this file is executed directly
if __name__ == "__main__":
    checker = ProxyChecker("bera420kodiakFaucet/data/proxies_replacement.txt")
    test_proxy = ""
    test_url = "https://www.faucet.kodiak.finance/"
    
    result = checker.check_and_replace_proxy(test_proxy, test_url)
    if result:
        print(f"Working proxy: {result}")
    else:
        print("No working proxy found.")