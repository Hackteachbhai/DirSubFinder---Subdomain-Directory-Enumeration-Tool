# dirsubfinder/utils.py
"""
Utility functions for DirSubFinder
Made by Vimal Bijalwan
"""

import re
import logging
import sys
from typing import Optional
from datetime import datetime


class Colors:
    """ANSI color codes for terminal output"""
    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class StatusSymbols:
    """Status symbols for terminal output"""
    SUCCESS = "[+]"
    INFO = "[*]"
    ERROR = "[-]"
    WARNING = "[!]"
    QUESTION = "[?]"


def print_banner():
    """Print the tool banner"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗
║                                                          ║
║   ██████╗ ██╗██████╗ ███████╗██╗   ██╗██████╗ ███████╗  ║
║   ██╔══██╗██║██╔══██╗██╔════╝██║   ██║██╔══██╗██╔════╝  ║
║   ██║  ██║██║██████╔╝███████╗██║   ██║██████╔╝█████╗    ║
║   ██║  ██║██║██╔══██╗╚════██║██║   ██║██╔══██╗██╔══╝    ║
║   ██████╔╝██║██║  ██║███████║╚██████╔╝██████╔╝██║       ║
║   ╚═════╝ ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝       ║
║                                                          ║
║   Subdomain & Directory Enumeration Tool                 ║
║   Made by Vimal Bijalwan                                 ║
║   Version 1.0.0                                         ║
║                                                          ║
╚══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)


def print_summary(results: dict, output_dir: str):
    """
    Print a summary of the scan results
    
    Args:
        results: Results dictionary
        output_dir: Output directory path
    """
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 50}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}SUMMARY{Colors.RESET}")
    print(f"{Colors.CYAN}{'-' * 50}{Colors.RESET}")
    print(f"{Colors.WHITE}Target:{Colors.RESET} {results['target']}")
    print(f"{Colors.WHITE}Subdomains Found:{Colors.RESET} {Colors.GREEN}{results['total_subdomains']}{Colors.RESET}")
    print(f"{Colors.WHITE}Directories Found:{Colors.RESET} {Colors.GREEN}{results['total_directories']}{Colors.RESET}")
    print(f"{Colors.WHITE}Reachable Hosts:{Colors.RESET} {len(results.get('reachable_hosts', []))}")
    print(f"{Colors.WHITE}Results:{Colors.RESET} {output_dir}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'=' * 50}{Colors.RESET}\n")


def validate_domain(domain: str) -> bool:
    """
    Validate domain name format
    
    Args:
        domain: Domain to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Simple domain validation
    pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return bool(re.match(pattern, domain))


def normalize_domain(domain: str) -> str:
    """
    Normalize domain name
    
    Args:
        domain: Domain to normalize
        
    Returns:
        Normalized domain
    """
    # Remove protocol if present
    domain = re.sub(r'^https?://', '', domain)
    # Remove path if present
    domain = domain.split('/')[0]
    # Remove trailing dot if present
    domain = domain.rstrip('.')
    # Convert to lowercase
    return domain.lower()


def setup_logging(quiet: bool = False):
    """
    Setup logging configuration
    
    Args:
        quiet: If True, reduce logging verbosity
    """
    level = logging.ERROR if quiet else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Disable verbose logging from third-party libraries
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)


def progress_bar(current: int, total: int, width: int = 40) -> str:
    """
    Create a progress bar string
    
    Args:
        current: Current progress
        total: Total items
        width: Width of the progress bar
        
    Returns:
        Progress bar string
    """
    if total == 0:
        return "[" + " " * width + "] 0%"
    
    percentage = current / total
    filled = int(percentage * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {int(percentage * 100)}%"
