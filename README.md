# Port Scanning & Vulnerability Detection with Nmap

## Objective
Learn active reconnaissance by identifying open ports, running services, and
known vulnerabilities on a target host, and automate the process with a
Python wrapper around Nmap.

This project builds on basic Nmap port scanning by adding Nmap's NSE
(Nmap Scripting Engine) vulnerability detection scripts, producing a clean,
readable vulnerability summary instead of raw scan output.

## Tools Used
- [Nmap](https://nmap.org/) — network scanner
- [python-nmap](https://pypi.org/project/python-nmap/) — Python wrapper for Nmap
- Nmap NSE scripts: `vuln` and `vulners` categories

## ⚠️ Legal & Ethical Notice
Only run this tool against systems you own or are explicitly authorized to
test (e.g. your own lab VM, Metasploitable, or a home network device you
control). Scanning systems without permission is illegal in most
jurisdictions.

## Setup

### 1. Install Nmap
```bash
# Debian/Ubuntu/Kali
sudo apt update && sudo apt install nmap -y

# macOS
brew install nmap
```

### 2. Install Python dependencies
```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install python-nmap
```

### 3. Set up a target
Use a system you own or a lab VM such as
[Metasploitable 2](https://sourceforge.net/projects/metasploitable/) running
in an isolated VirtualBox/VMware network.

## Usage
```bash
python3 nmap-portscanner.py <target-ip>

# Example
python3 nmap-portscanner.py 192.168.10.1
```

If you hit a permissions error on certain scan types, run with elevated
privileges:
```bash
sudo python3 nmap-portscanner.py 192.168.10.1
```

## How It Works
1. Runs an Nmap scan (`-sV -T4`) to detect open ports, services, and versions.
2. Runs Nmap's NSE `vuln` and `vulners` script categories against detected
   services to flag known vulnerabilities.
3. Parses the scan results into a clean Python dictionary.
4. Prints a terminal summary showing, per port, which NSE vulnerability
   scripts returned a hit.
5. Saves the full structured results (including raw NSE script output) to
   `examples/sample_output.json` for later reference.

## Sample Output

```
============================================================
VULNERABILITY SUMMARY
============================================================
[!] 192.168.10.1:21 (ftp 1.9.4)
    - vulners
[ ] 192.168.10.1:22 (ssh) - no known issues flagged
[ ] 192.168.10.1:23 (telnet) - no known issues flagged
[!] 192.168.10.1:53 (domain 2.80)
    - vulners
[!] 192.168.10.1:80 (tcpwrapped)
    - http-server-header
    - http-majordomo2-dir-traversal
    - http-vuln-cve2017-1001000
    - http-trane-info
    - http-dombased-xss
    - http-csrf
    - http-stored-xss
    - http-vuln-cve2010-0738
[!] 192.168.10.1:443 (tcpwrapped)
    - http-aspnet-debug
    - http-csrf
    - http-stored-xss
    - http-vuln-cve2014-3704
    - http-dombased-xss
    - ssl-poodle
```

Full JSON output (including raw NSE script details) is saved to
`examples/sample_output.json`.

## Project Structure
```
01-port-scanning-nmap/
├── README.md
├── nmap-portscanner.py
```

## What I Learned
- How to run and interpret Nmap service/version detection scans (`-sV`)
- How Nmap's scripting engine (NSE) extends scanning to vulnerability
  detection using the `vuln` and `vulners` script categories
- How to parse and structure raw scan data programmatically with
  `python-nmap`
- Why `tcpwrapped` doesn't always mean a service is unidentifiable, and how
  script probes can still surface useful findings on such ports
- The importance of filtering/summarizing tool output — raw NSE output is
  extremely verbose and needs post-processing to be useful in a report
