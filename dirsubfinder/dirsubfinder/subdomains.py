# dirsubfinder/subdomains.py
"""
Subdomain enumeration module for DirSubFinder
Made by Vimal Bijalwan
"""

import dns.resolver
import dns.exception
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional
import logging
import time

from .utils import Colors, StatusSymbols


class SubdomainEnumerator:
    """Enumerate subdomains using DNS resolution"""
    
    # Default common subdomains to check
    DEFAULT_SUBDOMAINS = [
        "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", 
        "webdisk", "ns2", "cpanel", "whm", "autodiscover", "autoconfig", "m",
        "imap", "test", "ns", "blog", "pop3", "dev", "www2", "admin", "forum",
        "news", "vpn", "ns3", "mail2", "new", "mysql", "old", "lists", "support",
        "mobile", "mx", "static", "docs", "beta", "shop", "sql", "secure", "demo",
        "cp", "calendar", "wiki", "web", "media", "email", "images", "img",
        "download", "dns", "piwik", "stats", "dashboard", "portal", "manage",
        "start", "info", "apps", "video", "srv", "account", "members", "login",
        "cdn", "host", "server", "ftp2", "help", "oracle", "crm", "cloud",
        "remote", "git", "api", "mssql", "vps", "store", "app", "staging"
    ]
    
    def __init__(
        self, 
        domain: str, 
        threads: int = 10,
        http_checker: Optional['HTTPChecker'] = None,
        quiet: bool = False
    ):
        """
        Initialize subdomain enumerator
        
        Args:
            domain: Target domain
            threads: Number of concurrent threads
            http_checker: HTTPChecker instance for availability checking
            quiet: Suppress verbose output
        """
        self.domain = domain
        self.threads = threads
        self.http_checker = http_checker
        self.quiet = quiet
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 2
        self.resolver.lifetime = 2
        self.found_subdomains = []
        
    def _resolve_subdomain(self, subdomain: str) -> Optional[str]:
        """
        Resolve a subdomain to check if it exists
        
        Args:
            subdomain: Subdomain to resolve
            
        Returns:
            Resolved IP or None if not found
        """
        try:
            full_domain = f"{subdomain}.{self.domain}"
            answers = self.resolver.resolve(full_domain, 'A')
            if answers:
                return str(answers[0])
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, 
                dns.resolver.Timeout, dns.exception.DNSException):
            pass
        return None
    
    def _check_subdomain(self, subdomain: str) -> Optional[Dict]:
        """
        Check a single subdomain
        
        Args:
            subdomain: Subdomain to check
            
        Returns:
            Dict with subdomain info or None if not found
        """
        full_domain = f"{subdomain}.{self.domain}"
        ip = self._resolve_subdomain(subdomain)
        
        if ip:
            result = {
                "subdomain": full_domain,
                "ip": ip
            }
            
            # Check HTTP/HTTPS if available
            if self.http_checker:
                http_result = self.http_checker.check(f"http://{full_domain}")
                if http_result:
                    result["http_status"] = http_result.get("status")
                    result["http_url"] = http_result.get("url")
                
                https_result = self.http_checker.check(f"https://{full_domain}")
                if https_result:
                    result["https_status"] = https_result.get("status")
                    result["https_url"] = https_result.get("url")
            
            if not self.quiet:
                status = f" [{result.get('http_status', 'N/A')}]" if result.get('http_status') else ""
                print(f"{Colors.GREEN}{StatusSymbols.SUCCESS} Found: {full_domain} ({ip}){status}{Colors.RESET}")
            
            return result
        
        return None
    
    def enumerate(self) -> List[Dict]:
        """
        Enumerate all subdomains
        
        Returns:
            List of found subdomains with their details
        """
        found = []
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            # Submit all tasks
            future_to_subdomain = {
                executor.submit(self._check_subdomain, sub): sub 
                for sub in self.DEFAULT_SUBDOMAINS
            }
            
            # Process completed tasks
            for future in as_completed(future_to_subdomain):
                result = future.result()
                if result:
                    found.append(result)
                    self.found_subdomains.append(result)
        
        return found
