# dirsubfinder/http.py
"""
HTTP checking module for DirSubFinder
Made by Vimal Bijalwan
"""

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional
import logging
import time
from urllib.parse import urlparse

from .utils import Colors, StatusSymbols


class HTTPChecker:
    """Check HTTP/HTTPS availability and status codes"""
    
    def __init__(self, timeout: int = 5, max_workers: int = 10):
        """
        Initialize HTTP checker
        
        Args:
            timeout: Request timeout in seconds
            max_workers: Maximum concurrent workers
        """
        self.timeout = timeout
        self.max_workers = max_workers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.session.verify = False  # Disable SSL verification for testing
        
        # Suppress SSL warnings
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def check(self, url: str) -> Optional[Dict]:
        """
        Check a single URL
        
        Args:
            url: URL to check
            
        Returns:
            Dict with status info or None if not reachable
        """
        try:
            start_time = time.time()
            response = self.session.get(
                url, 
                timeout=self.timeout,
                allow_redirects=True,
                stream=True
            )
            response_time = time.time() - start_time
            
            # Check if it's a valid response
            if response.status_code < 400 or response.status_code in [401, 403, 404]:
                return {
                    "url": url,
                    "status": response.status_code,
                    "response_time": round(response_time, 3),
                    "content_length": len(response.content) if response.content else 0,
                    "server": response.headers.get('Server', 'Unknown')
                }
        except requests.exceptions.Timeout:
            logging.debug(f"Timeout checking {url}")
        except requests.exceptions.ConnectionError:
            logging.debug(f"Connection error checking {url}")
        except requests.exceptions.RequestException as e:
            logging.debug(f"Request error checking {url}: {e}")
        
        return None
    
    def check_multiple(self, urls: List[str]) -> List[Dict]:
        """
        Check multiple URLs concurrently
        
        Args:
            urls: List of URLs to check
            
        Returns:
            List of successful check results
        """
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_url = {
                executor.submit(self.check, url): url 
                for url in urls
            }
            
            for future in as_completed(future_to_url):
                result = future.result()
                if result:
                    results.append(result)
        
        return results
