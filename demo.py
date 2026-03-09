#!/usr/bin/env python3
"""
Guardian - Interactive Demo
Shows how guardian_standalone.py works when executed via IEX
"""

def demo_windows_powershell():
    """Demo: Windows PowerShell execution"""
    demo = """
═══════════════════════════════════════════════════════════════════════════════
DEMO: Windows PowerShell - IEX Execution
═══════════════════════════════════════════════════════════════════════════════

Administrator: C:\\Users\\Admin> 
iex(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/your-username/Guardian/main/guardian_standalone.py')

[*] Downloading...
[+] Starting Guardian...

🛡️  Guardian DFIR CLI - Forensic toolkit (no dependencies)
Type 'help' for commands.

(guardian) sysinfo
os: Windows
platform: Windows-10-10.0.19044-SP1
python: 3.11.0

(guardian) processes
Image                | PID       | Session Name     | Session# | Mem Usage
svchost.exe          | 512       | Services         | 0        | 4,200 K
explorer.exe         | 1024      | Console          | 1        | 125,432 K
python.exe           | 2048      | Console          | 1        | 32,456 K
...

(guardian) network
Protocol  Local Address               Remote Address               State           PID     
TCP       127.0.0.1:54321            10.0.0.1:443                 ESTABLISHED     2048    
TCP       192.168.1.100:52341        93.184.216.34:443            ESTABLISHED     512     
...

(guardian) snapshot full
Snapshot taken at 2026-03-09T15:45:23.654321
Type: full
Data captures: processes, network, software, system, firewall, scheduled_tasks

(guardian) export snapshot_20260309_154523.json
✓ Snapshots exported to snapshot_20260309_154523.json

(guardian) exit
Exiting Guardian DFIR CLI...

Administrator: C:\\Users\\Admin>
[*] Forensics completed in 47 seconds
[*] JSON file created with full system snapshot

═══════════════════════════════════════════════════════════════════════════════
"""
    print(demo)


def demo_linux_bash():
    """Demo: Linux Bash execution"""
    demo = """
═══════════════════════════════════════════════════════════════════════════════
DEMO: Linux Bash - IEX Execution (via curl)
═══════════════════════════════════════════════════════════════════════════════

$ curl https://raw.githubusercontent.com/your-username/Guardian/main/guardian_standalone.py | python3

[*] Downloading...
[+] Starting Guardian...

🛡️  Guardian DFIR CLI - Forensic toolkit (no dependencies)
Type 'help' for commands.

(guardian) sysinfo
os: Linux
platform: Linux-6.1.0-28-generic-x86_64-with-glibc2.35
python: 3.10.12

(guardian) processes
USER       PID     %CPU %MEM    VSZ   RSS COMM
root         1     0.0  0.1  20232 10156 systemd
root        10     0.0  0.0  55480  5432 kthreadd
root       500     0.1  0.3 1025624 45632 snapd
admin     1500     1.2  1.8 3152456 295000 firefox
...

(guardian) network
State   Recv-Q Send-Q Local Address State     
LISTEN      0   4096  127.0.0.53:53 LISTEN    
LISTEN      0   4096  0.0.0.0:22    LISTEN    
ESTAB       0      0  192.168.1.100:45621 ESTAB
...

(guardian) snapshot full
Snapshot taken at 2026-03-09T15:47:12.345678
Type: full
Data captures: processes, network, software, system, firewall, scheduled_tasks

(guardian) export forensics_$(date +%s).json
✓ Snapshots exported to forensics_1741509632.json

(guardian) run "netstat -tlnp | grep LISTEN"
tcp    0   0 127.0.0.53:53   0.0.0.0:*   LISTEN  450/systemd-resolve
tcp    0   0 0.0.0.0:22      0.0.0.0:*   LISTEN  512/sshd
[exit:0]

(guardian) exit
Exiting Guardian DFIR CLI...

$ ls -lh forensics_*.json
-rw-r--r-- 1 admin admin 312K Mar  9 15:47 forensics_1741509632.json

═══════════════════════════════════════════════════════════════════════════════
"""
    print(demo)


def demo_server_deployment():
    """Demo: Self-hosted server deployment"""
    demo = """
═══════════════════════════════════════════════════════════════════════════════
DEMO: Self-Hosted Deployment
═══════════════════════════════════════════════════════════════════════════════

Terminal 1 - Run the server:
$ python3 server.py 0.0.0.0 8080

🛡️  Guardian DFIR CLI Server Started
┌─ Listening on: 0.0.0.0:8080
├─ Windows (PowerShell):
│  iex(New-Object Net.WebClient).DownloadString('http://192.168.1.50:8080/guardian')
├─ Linux/macOS (Bash):
│  curl http://192.168.1.50:8080/guardian | python3
└─ Info endpoint: http://192.168.1.50:8080/info

═════════════════════════════════════════════════════════════════════════════════

Terminal 2 - From another system:
$ curl http://192.168.1.50:8080/guardian | python3

🛡️  Guardian DFIR CLI - Forensic toolkit (no dependencies)
Type 'help' for commands.

(guardian) snapshot full
Snapshot taken at 2026-03-09T15:50:00.123456
Type: full
Data captures: processes, network, software, system, firewall, scheduled_tasks

(guardian) export analysis.json
✓ Snapshots exported to analysis.json

(guardian) exit

═════════════════════════════════════════════════════════════════════════════════

Server Terminal - Shows requests:
[+] Served Guardian Python to 192.168.1.101
[+] Served Guardian Python to 192.168.1.102
[+] Served Guardian Python to 192.168.1.103

═════════════════════════════════════════════════════════════════════════════════
"""
    print(demo)


def demo_automated_collection():
    """Demo: Automated multi-system collection"""
    demo = """
═══════════════════════════════════════════════════════════════════════════════
DEMO: Automated Forensic Collection (Bash Script)
═══════════════════════════════════════════════════════════════════════════════

$ cat collect_forensics.sh
#!/bin/bash
# Collect forensics from production servers

GUARDIAN_URL="https://raw.githubusercontent.com/your-username/Guardian/main/guardian_standalone.py"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
EVIDENCE_DIR="/evidence"

for server in web01 web02 app01 db01; do
    echo "[*] Collecting from $server..."
    
    ssh root@$server << EOF
curl -s $GUARDIAN_URL | python3 << 'COMMANDS'
snapshot full
export /tmp/forensics_${server}_${TIMESTAMP}.json
exit
COMMANDS

# Transfer evidence
scp /tmp/forensics_${server}_${TIMESTAMP}.json collector@evidence:$EVIDENCE_DIR/
rm -f /tmp/forensics_*.json
EOF
done

echo "[+] Collection complete"

═════════════════════════════════════════════════════════════════════════════════

Running the script:
$ bash collect_forensics.sh

[*] Collecting from web01...
[+] Downloading Guardian... [downloaded 20KB]
[+] Executing... 
[+] Collected forensics_web01_20260309_155000.json
[+] Transferred to evidence server

[*] Collecting from web02...
[+] Downloading Guardian... [downloaded 20KB]
[+] Executing...
[+] Collected forensics_web02_20260309_155002.json
[+] Transferred to evidence server

[*] Collecting from app01...
[+] Downloading Guardian... [downloaded 20KB]
[+] Executing...
[+] Collected forensics_app01_20260309_155004.json
[+] Transferred to evidence server

[*] Collecting from db01...
[+] Downloading Guardian... [downloaded 20KB]
[+] Executing...
[+] Collected forensics_db01_20260309_155006.json
[+] Transferred to evidence server

[+] Collection complete

$ ls -la /evidence/
forensics_web01_20260309_155000.json  (318 KB)
forensics_web02_20260309_155002.json  (325 KB)
forensics_app01_20260309_155004.json  (312 KB)
forensics_db01_20260309_155006.json   (341 KB)

═════════════════════════════════════════════════════════════════════════════════
"""
    print(demo)


def show_menu():
    """Show demo menu"""
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                    🛡️  GUARDIAN DFIR CLI - IEX DEMOS 🛡️                      ║
║                                                                               ║
║                    Remote Forensic Analysis Toolkit                          ║
║                    Execute Anywhere with One Command                         ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Available Demos:

1. Windows PowerShell - IEX Execution (Interactive)
2. Linux Bash - IEX Execution (Interactive)
3. Self-Hosted Server Deployment
4. Automated Multi-System Collection

Or press 'q' to quit, 'all' to run all demos

Choose: """)


if __name__ == '__main__':
    import sys
    
    demos = {
        '1': ('Windows PowerShell Demo', demo_windows_powershell),
        '2': ('Linux Bash Demo', demo_linux_bash),
        '3': ('Server Deployment Demo', demo_server_deployment),
        '4': ('Automated Collection Demo', demo_automated_collection),
    }
    
    if len(sys.argv) > 1:
        choice = sys.argv[1].lower()
    else:
        show_menu()
        choice = input().strip().lower()
    
    if choice == 'all':
        for title, demo_func in demos.values():
            print(f"\n{'='*80}")
            print(f"{title}")
            print(f"{'='*80}\n")
            demo_func()
            input("\nPress Enter to continue...")
    elif choice in demos:
        demos[choice][1]()
    elif choice != 'q':
        print("Invalid choice")
    
    print("\nFor real execution, use:")
    print("  Windows: iex(New-Object Net.WebClient).DownloadString('https://...')")
    print("  Linux:   curl https://... | python3")
