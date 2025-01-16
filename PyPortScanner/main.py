import socket
import ipaddress

class Port_Scanner():
    def __init__(self, targets):
        self.targets = targets
        self.start_port = 1
        self.end_port = 65536

        self.ip_convert()

    def ip_convert(self):

        target_lst = list()

        if type(self.targets) == list:
            for target in targets:
                try:
                    ipaddress.ip_address(target)
                except ValueError:
                    print(f"{self.targets} is an invalid IP Address")
                else:
                    target_lst.append(target)
            self.targets = target_lst

        elif "/" in self.targets:
            for addr in ipaddress.IPv4Network(self.targets):
                target_lst.append(addr)
            self.targets = target_lst

        elif "," in self.targets:
            ip = self.targets.split(",")
            for target in ip:
                try:
                    ipaddress.ip_address(target)
                except ValueError:
                    print(f"{self.targets} is an invalid IP Address")
                else:
                    target_lst.append(target)
            self.targets = target_lst
        else:
            try:
                ipaddress.ip_address(self.targets)
            except ValueError:
                print(f"{self.targets} is an invalid IP Address")

    def scan_port(self, port, ip):
        try:
            print(f"Scanning host {ip} on port {port}")
            sock = socket.socket()
            sock.settimeout(0.5)
            sock.connect((ip, port))
            try:
                banner = sock.recv(1024)
                print(f"Open Port {port}: {banner.decode()}")
            except:
                print(f"Open Port {port}")

        except:
            pass

    def multiple_ports(self, *args):

        if args:
            ports = args[0]
            self.start_port = int(ports[0])
            self.end_port = int(ports[1])

        if type(self.targets) == list:

            for target in self.targets:

                for port in range(self.start_port, (self.end_port + 1)):
                    self.scan_port(port, target)
        else:
            for port in range(self.start_port, self.end_port + 1):
                self.scan_port(port, self.targets)

    def single_port(self, port):

        if type(self.targets) == list:

            for target in self.targets:
                self.scan_port(port, target)
        else:
            self.scan_port(port, self.targets)


targets = input('Enter Target/s To Scan (split multiple targets with "," Can also enter CIDR notation): ')
port_type = input("Would you like to scan: \n1) A port range \n2) A single port \n3)All Ports\n")

scanner = Port_Scanner(targets)

if port_type == "1":
    port_range_to_scan = input("Please enter the port range ex 1-22: ")
    ranges = port_range_to_scan.split("-")
    scanner.multiple_ports(ranges)

elif port_type == "2":
    port_to_scan = int(input("Enter the port to be scanned: "))
    scanner.single_port(port_to_scan)

else:
    print("Scanning ports  1-65535")
    scanner.multiple_ports()

