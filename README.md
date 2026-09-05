# DirSubFinder---Subdomain-Directory-Enumeration-Tool
DirSubFinder - Subdomain &amp; Directory Enumeration Tool
# 🔍 DirSubFinder

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Version-1.0.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <img src="https://img.shields.io/badge/Made%20by-Vimal%20Bijalwan-red.svg" alt="Made by Vimal Bijalwan">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg" alt="Platform">
</p>

<p align="center">
  <b>Professional Subdomain & Directory Enumeration Tool for Authorized Security Testing</b>
</p>

<p align="center">
  <b>🔒 For authorized security professionals and penetration testers only</b>
</p>

---

## 📋 Table of Contents

- [Overview](#-project-overview)
- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [CLI Options](#-cli-options)
- [Examples](#-examples)
- [Output Structure](#-output-structure)
- [Project Structure](#-project-structure)
- [Screenshots](#-screenshots)
- [Legal Disclaimer](#-legal-disclaimer)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📋 Project Overview

**DirSubFinder** is a professional-grade Python CLI tool designed for subdomain and directory enumeration during authorized security assessments. It helps security professionals and penetration testers discover potential attack vectors by identifying subdomains and common web directories on target domains.

### 🎯 Purpose

In the world of cybersecurity, reconnaissance is the first and most crucial phase of any security assessment. DirSubFinder automates this process by:

- Discovering subdomains that may host sensitive applications or services
- Finding hidden directories and endpoints that could contain vulnerabilities
- Providing a comprehensive overview of the target's attack surface
- Generating professional reports for documentation and further analysis

### 👨‍💻 Made by Vimal Bijalwan

---

## ✨ Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| 🎯 **Subdomain Discovery** | Enumerate common subdomains using DNS resolution |
| 📂 **Directory Enumeration** | Find common web directories and paths |
| 🌐 **HTTP/HTTPS Checking** | Verify availability and get status codes |
| ⚡ **Concurrent Scanning** | Fast scanning with configurable threads |
| 📊 **Multiple Output Formats** | Save results in TXT or JSON |
| 🎨 **Professional CLI** | Clean interface with colored output and progress indicators |

### Technical Features

- ✅ Validates and normalizes target domain input
- ✅ Configurable thread count for performance optimization
- ✅ Custom wordlist support for directory enumeration
- ✅ Rate limiting and configurable request timeouts
- ✅ Proper error handling and logging
- ✅ Ctrl+C graceful interruption
- ✅ No exploit execution or destructive actions
- ✅ HTTP/HTTPS availability checking with status codes
- ✅ Response time tracking
- ✅ Comprehensive result summaries

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning)

### Method 1: From Source (Recommended)

```bash
# Clone the repository
git clone https://github.com/vimalbijalwan/DirSubFinder.git
cd DirSubFinder

# Install dependencies
pip install -r requirements.txt

# Make main.py executable (Linux/Mac)
chmod +x main.py

# Verify installation
python main.py --version
