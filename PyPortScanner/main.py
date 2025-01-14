import socket
import ipaddress

class Port_Scanner():
    def __init__(self, targets):
        self.targets = targets
        self.start_port = 1
        self.end_port = 65536
                

    def scan_port(self, port, ip):
        try:
            sock = socket.socket()
            sock.settimeout(0.5)
            sock.connect((ip, port))
            try:
                banner = sock.recv(1024)
                print(f"Open Port {port}: {banner.decode()}")
            except:
                print(f"Open Port {port}")

        except:
            print(f"Port {port} Closed")

    def multiple_ports(self, *args):
        ip = self.targets

        if args:
            pass

        for port in range(self.start_port, (self.end_port + 1)):
            self.scan_port(port, ip)

    def single_port(self, port):
        think = 0


targets = input('Enter Target/s To Scan (split multiple targets with "," Can also enter CIDR notation): ')
port_type = input("Would you like to scan: \n1) A port range \n2) A single port \n3)All Ports\n")

scanner = Port_Scanner(targets)

if port_type == "1":
    port_range_to_scan = input("Please enter the port range ex 1-22: ")
    range = port_range_to_scan.split("-")
    #scanner.multiple_ports(range) BROKEN

elif port_type == "2":
    port_to_scan = int(input("Enter the port to be scanned: "))
    scanner.single_port(port_to_scan)

else:
    print("Scanning ports  1-65535")
    scanner.multiple_ports()

