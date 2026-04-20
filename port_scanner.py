import socket

YELLOW_BOLD = "\033[0;33m\033[1m"
BOLD = "\033[1m"
RESET = "\033[0m"

def scan(host="0.0.0.0", start=1, end=1024):
    print(f"{YELLOW_BOLD}==> {RESET}{BOLD}Scanning {host} ports {start}-{end}...{RESET}")
    open_ports = []

    for port in range(start, end + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((host, port))
        if result == 0:
            open_ports.append(port)
            print(f"{YELLOW_BOLD}==> {RESET}{BOLD}Open port found: {port}{RESET}")
        sock.close()

    if not open_ports:
        print(f"{YELLOW_BOLD}==> {RESET}{BOLD}No open ports detected on {host}, continuing to scan...{RESET}")
    else:
        print(f"{YELLOW_BOLD}==> {RESET}{BOLD}Scan complete. Open ports: {open_ports}{RESET}")

if __name__ == "__main__":
    scan("0.0.0.0")
