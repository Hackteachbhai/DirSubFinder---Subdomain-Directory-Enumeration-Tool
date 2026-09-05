# dirsubfinder/output.py
"""
Output management module for DirSubFinder
Made by Vimal Bijalwan
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import logging


class OutputManager:
    """Manage output file generation"""
    
    def __init__(self, output_dir: Path):
        """
        Initialize output manager
        
        Args:
            output_dir: Directory to save output files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def save_json(self, results: Dict) -> Path:
        """
        Save results in JSON format
        
        Args:
            results: Results dictionary
            
        Returns:
            Path to saved file
        """
        filename = self.output_dir / f"{results['target']}_{self.timestamp}.json"
        
        # Add metadata
        output = {
            "metadata": {
                "target": results["target"],
                "timestamp": self.timestamp,
                "tool": "DirSubFinder",
                "version": "1.0.0",
                "author": "Vimal Bijalwan"
            },
            "summary": {
                "total_subdomains": results["total_subdomains"],
                "total_directories": results["total_directories"],
                "reachable_hosts": len(results.get("reachable_hosts", []))
            },
            "subdomains": results["subdomains"],
            "directories": results["directories"],
            "reachable_hosts": results.get("reachable_hosts", [])
        }
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        logging.info(f"Saved JSON results to {filename}")
        return filename
    
    def save_txt(self, results: Dict) -> Path:
        """
        Save results in TXT format
        
        Args:
            results: Results dictionary
            
        Returns:
            Path to saved file
        """
        filename = self.output_dir / f"{results['target']}_{self.timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write(f"DirSubFinder - Scan Results\n")
            f.write(f"Made by Vimal Bijalwan\n")
            f.write(f"Target: {results['target']}\n")
            f.write(f"Scan Date: {self.timestamp}\n")
            f.write("=" * 60 + "\n\n")
            
            # Subdomains
            f.write(f"SUBODOMAINS FOUND ({results['total_subdomains']}):\n")
            f.write("-" * 40 + "\n")
            for sub in results["subdomains"]:
                line = f"  {sub['subdomain']} -> {sub['ip']}"
                if sub.get('http_status'):
                    line += f" (HTTP: {sub['http_status']})"
                if sub.get('https_status'):
                    line += f" (HTTPS: {sub['https_status']})"
                f.write(line + "\n")
            f.write("\n")
            
            # Reachable hosts
            if results.get("reachable_hosts"):
                f.write(f"REACHABLE HOSTS ({len(results['reachable_hosts'])}):\n")
                f.write("-" * 40 + "\n")
                for host in results["reachable_hosts"]:
                    f.write(f"  {host['url']} (Status: {host['status']})\n")
                f.write("\n")
            
            # Directories
            f.write(f"DIRECTORIES FOUND ({results['total_directories']}):\n")
            f.write("-" * 40 + "\n")
            for dir in results["directories"]:
                f.write(f"  {dir['path']} -> {dir['url']} (Status: {dir['status_code']})\n")
            f.write("\n")
            
            # Summary
            f.write("=" * 60 + "\n")
            f.write("SUMMARY\n")
            f.write("-" * 40 + "\n")
            f.write(f"Target: {results['target']}\n")
            f.write(f"Subdomains Found: {results['total_subdomains']}\n")
            f.write(f"Directories Found: {results['total_directories']}\n")
            f.write(f"Reachable Hosts: {len(results.get('reachable_hosts', []))}\n")
            f.write("=" * 60 + "\n")
        
        logging.info(f"Saved TXT results to {filename}")
        return filename
