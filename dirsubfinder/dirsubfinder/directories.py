# dirsubfinder/directories.py
"""
Directory enumeration module for DirSubFinder
Made by Vimal Bijalwan
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional
import requests
from pathlib import Path
import logging

from .utils import Colors, StatusSymbols


class DirectoryEnumerator:
    """Enumerate common web directories and paths"""
    
    # Default common directories to check
    DEFAULT_DIRECTORIES = [
        "admin", "login", "api", "wp-admin", "wp-content", "wp-includes",
        "images", "css", "js", "assets", "static", "media", "uploads",
        "download", "docs", "documentation", "help", "support", "blog",
        "news", "products", "services", "about", "contact", "team",
        "careers", "jobs", "partners", "clients", "portfolio", "gallery",
        "events", "tickets", "registration", "signup", "signin", "logout",
        "profile", "settings", "dashboard", "panel", "console", "adminpanel",
        "cpanel", "whm", "webmail", "mail", "exchange", "owa", "remote",
        "vpn", "ssh", "ftp", "sftp", "database", "mysql", "phpmyadmin",
        "phpinfo", "server-status", "server-info", "cgi-bin", "cgi-bin",
        "php", "asp", "jsp", "config", "conf", "backup", "temp", "tmp",
        "logs", "error", "test", "demo", "stage", "staging", "dev",
        "development", "qa", "uat", "production", "live", "beta", "alpha"
    ]
    
    def __init__(
        self,
        domain: str,
        threads: int = 10,
        http_checker: Optional['HTTPChecker'] = None,
        wordlist_path: Optional[str] = None,
        quiet: bool = False
    ):
        """
        Initialize directory enumerator
        
        Args:
            domain: Target domain
            threads: Number of concurrent threads
            http_checker: HTTPChecker instance for HTTP requests
            wordlist_path: Path to custom wordlist
            quiet: Suppress verbose output
        """
        self.domain = domain
        self.threads = threads
        self.http_checker = http_checker
        self.quiet = quiet
        
        # Load wordlist
        self.directories = self._load_wordlist(wordlist_path)
        
    def _load_wordlist(self, wordlist_path: Optional[str]) -> List[str]:
        """
        Load wordlist from file or use default
        
        Args:
            wordlist_path: Path to custom wordlist
            
        Returns:
            List of directories to check
        """
        if wordlist_path and Path(wordlist_path).exists():
            try:
                with open(wordlist_path, 'r') as f:
                    directories = [line.strip() for line in f if line.strip()]
                    if not self.quiet:
                        print(f"{StatusSymbols.INFO} Loaded {len(directories)} directories from {wordlist_path}")
                    return directories
            except Exception as e:
                logging.error(f"Error loading wordlist: {e}")
                if not self.quiet:
                    print(f"{Colors.YELLOW}[!] Error loading wordlist, using default{Colors.RESET}")
        
        return self.DEFAULT_DIRECTORIES
    
    def _check_directory(self, directory: str) -> Optional[Dict]:
        """
        Check a single directory
        
        Args:
            directory: Directory path to check
            
        Returns:
            Dict with directory info or None if not found
        """
        url = f"https://{self.domain}/{directory}"
        
        try:
            response = requests.get(
                url,
                timeout=5,
                allow_redirects=True,
                verify=False,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            # Consider 200, 301, 302, 403 as "found"
            if response.status_code in [200, 301, 302, 403, 401, 307, 308]:
                result = {
                    "path": f"/{directory}",
                    "url": url,
                    "status_code": response.status_code,
                    "content_length": len(response.content) if response.content else 0
                }
                
                if not self.quiet:
                    status_color = Colors.GREEN if response.status_code == 200 else Colors.YELLOW
                    print(f"{status_color}{StatusSymbols.SUCCESS} Found: /{directory} (Status: {response.status_code}){Colors.RESET}")
                
                return result
            
        except requests.exceptions.RequestException:
            pass
        
        return None
    
    def enumerate(self) -> List[Dict]:
        """
        Enumerate all directories
        
        Returns:
            List of found directories with their details
        """
        found = []
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            # Submit all tasks
            future_to_dir = {
                executor.submit(self._check_directory, dir): dir 
                for dir in self.directories
            }
            
            # Process completed tasks
            for future in as_completed(future_to_dir):
                result = future.result()
                if result:
                    found.append(result)
        
        return found
