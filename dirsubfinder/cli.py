# dirsubfinder/cli.py
#!/usr/bin/env python3
"""
CLI Interface for DirSubFinder
Made by Vimal Bijalwan
"""

import argparse
import sys
import signal
import time
from pathlib import Path
from typing import Optional
import logging

from . import __version__, __author__
from .subdomains import SubdomainEnumerator
from .directories import DirectoryEnumerator
from .http import HTTPChecker
from .output import OutputManager
from .utils import (
    validate_domain, 
    normalize_domain, 
    setup_logging,
    print_banner,
    print_summary,
    Colors,
    StatusSymbols
)


def setup_argparse() -> argparse.ArgumentParser:
    """Setup command line argument parser"""
    parser = argparse.ArgumentParser(
        description="DirSubFinder - Professional Subdomain & Directory Enumeration Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --target example.com
  python main.py --target example.com --output ./results --threads 20
  python main.py --target example.com --wordlist custom.txt --json
  python main.py --target example.com --quiet --threads 30

Made by Vimal Bijalwan
        """
    )
    
    parser.add_argument(
        "--target",
        "-t",
        required=True,
        help="Target domain to enumerate (e.g., example.com)"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        default="./output",
        help="Output directory for results (default: ./output)"
    )
    
    parser.add_argument(
        "--threads",
        "-T",
        type=int,
        default=10,
        help="Number of concurrent threads (default: 10)"
    )
    
    parser.add_argument(
        "--wordlist",
        "-w",
        default=None,
        help="Custom wordlist file path for directory enumeration"
    )
    
    parser.add_argument(
        "--json",
        "-j",
        action="store_true",
        help="Output results in JSON format"
    )
    
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress verbose output"
    )
    
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"DirSubFinder v{__version__} - Made by {__author__}"
    )
    
    parser.add_argument(
        "--timeout",
        type=int,
        default=5,
        help="Request timeout in seconds (default: 5)"
    )
    
    parser.add_argument(
        "--no-http",
        action="store_true",
        help="Skip HTTP/HTTPS availability checking"
    )
    
    return parser


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print(f"\n{Colors.YELLOW}[!] Interrupted by user. Cleaning up...{Colors.RESET}")
    sys.exit(0)


def main():
    """Main entry point for the CLI tool"""
    # Setup signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Parse arguments
    parser = setup_argparse()
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(quiet=args.quiet)
    
    # Print banner
    if not args.quiet:
        print_banner()
        print(f"{Colors.CYAN}Target:{Colors.RESET} {args.target}\n")
    
    try:
        # Validate and normalize target
        domain = normalize_domain(args.target)
        if not validate_domain(domain):
            print(f"{Colors.RED}[!] Invalid domain: {args.target}{Colors.RESET}")
            sys.exit(1)
        
        # Create output directory
        output_dir = Path(args.output) / domain
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        http_checker = HTTPChecker(timeout=args.timeout)
        subdomain_enum = SubdomainEnumerator(
            domain=domain,
            threads=args.threads,
            http_checker=http_checker,
            quiet=args.quiet
        )
        dir_enum = DirectoryEnumerator(
            domain=domain,
            threads=args.threads,
            http_checker=http_checker,
            wordlist_path=args.wordlist,
            quiet=args.quiet
        )
        output_manager = OutputManager(output_dir)
        
        results = {
            "target": domain,
            "subdomains": [],
            "directories": [],
            "total_subdomains": 0,
            "total_directories": 0,
            "reachable_hosts": []
        }
        
        # Enumerate subdomains
        if not args.quiet:
            print(f"{StatusSymbols.INFO} Enumerating subdomains...")
        
        subdomains = subdomain_enum.enumerate()
        results["subdomains"] = subdomains
        results["total_subdomains"] = len(subdomains)
        
        # Check reachable hosts
        if not args.no_http:
            if not args.quiet:
                print(f"\n{StatusSymbols.INFO} Checking HTTP/HTTPS availability...")
            results["reachable_hosts"] = http_checker.check_multiple(
                [f"http://{sub}" for sub in subdomains] +
                [f"https://{sub}" for sub in subdomains]
            )
        
        # Enumerate directories
        if not args.quiet:
            print(f"\n{StatusSymbols.INFO} Enumerating directories...")
        
        directories = dir_enum.enumerate()
        results["directories"] = directories
        results["total_directories"] = len(directories)
        
        # Save results
        if args.json:
            output_manager.save_json(results)
        else:
            output_manager.save_txt(results)
        
        # Print summary
        if not args.quiet:
            print_summary(results, output_dir)
        else:
            # Print minimal summary for quiet mode
            print(f"Subdomains: {results['total_subdomains']}, Directories: {results['total_directories']}")
            print(f"Results saved to: {output_dir}")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Interrupted by user{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}[!] Error: {str(e)}{Colors.RESET}")
        logging.error(f"Error occurred: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
