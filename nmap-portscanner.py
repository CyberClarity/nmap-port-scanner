import nmap
import sys
import json
import os
from datetime import datetime

def scan_target(target, ports="1-1024"):
    scanner = nmap.PortScanner()
    print(f"Scanning {target}...")
    scanner.scan(target, ports, arguments="-sV -T4 --script vuln,vulners")

    report = {"target": target, "scanned_at": datetime.now().isoformat(), "hosts": []}

    for host in scanner.all_hosts():
        host_data = {
            "ip": host,
            "state": scanner[host].state(),
            "open_ports": []
        }
        for proto in scanner[host].all_protocols():
            for port in scanner[host][proto].keys():
                info = scanner[host][proto][port]

                port_entry = {
                    "port": port,
                    "protocol": proto,
                    "service": info.get("name", ""),
                    "version": info.get("version", ""),
                    "vulnerabilities": []
                }

                script_results = info.get("script", {})
                for script_name in script_results.keys():
                    port_entry["vulnerabilities"].append(script_name)

                host_data["open_ports"].append(port_entry)
        report["hosts"].append(host_data)

    return report

def print_summary(report):
    print("\n" + "="*60)
    print("VULNERABILITY SUMMARY")
    print("="*60)
    for host in report["hosts"]:
        for port in host["open_ports"]:
            label = f"{host['ip']}:{port['port']} ({port['service']} {port['version']})"
            if port["vulnerabilities"]:
                print(f"[!] {label}")
                for script_name in port["vulnerabilities"]:
                    print(f"    - {script_name}")
            else:
                print(f"[ ] {label} - no known issues flagged")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    result = scan_target(target)

    print_summary(result)

    os.makedirs("examples", exist_ok=True)
    with open("examples/sample_output.json", "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nFull report saved to examples/sample_output.json")
