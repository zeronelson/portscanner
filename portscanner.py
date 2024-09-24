import socket
import subprocess
import sys
from multiprocessing import Pool
from colorama import Fore, Style
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

def scan(arg):
    target_ip, port = arg
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(.1)
    try:
        sock.connect((target_ip, port))
        sock.close()
        return port, True
    except (socket.timeout, socket.error):
        return port, False
    
def returnTarget(target):
    try: 
        socket.inet_aton(target)
        return target
    except:
        try:
            return socket.gethostbyname(target)
        except:
            return None

def banner(target_name, port, target_ip):
    print("\n")
    print(f"{Fore.RED}")
    print(target_name)
    target_info = target_name + ": " + target_ip
    if "-" in port:
        print("*" * 60)
        # TODO - How to display hostname
        print(f"Scanning host ({target_info}) for ports {port} ")
        print("*" * 60)
    elif "," in port:
        # TODO - Can delineate ports 
        print("*" * 60)
        print(f"Scanning host ({target_ip}) for ports {port} ")
        print("*" * 60)
    else:
        if int(port) > 0: 
            print("*" * 60)
            print(f"Scanning host ({target_ip}) for port {port} ")
            print("*" * 60)
        else: 
            print("*" * 60)
            print(f"Scanning host ({target_ip}) for ports 1-1065")
            print("*" * 60)

def displayScan():
    try:
        answer = socket.getservbyport(port)
        print(f"{Fore.GREEN}{port:4d}: Open {Style.RESET_ALL}  ({answer})")
    except(socket.error):
        print(f"{Fore.RED}{port:4d}: Closed ")   

if __name__ == '__main__':
    subprocess.call('clear', shell=True) # Clears screen
    '''print("""
        ██████╗  ██████╗ ██████╗ ████████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
        ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
        ██████╔╝██║   ██║██████╔╝   ██║       ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
        ██╔═══╝ ██║   ██║██╔══██╗   ██║       ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
        ██║     ╚██████╔╝██║  ██║   ██║       ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
        ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝       ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝                                                                                                    
""")'''
    pool = Pool(processes=30)
    #target = input('Enter IPs/hostnames (separated by commas): ')
    ports = input('Enter port(s) or 0 to skip (list with commas/range with dash): ')
    
    target = "target.com"
    
    if (ports == ""):
        ports = "0-200"

    # If input is a list
    if ("," in target or "," in ports):
        # Split by comma and strip string for processing
        targetList, portList = target.split(","), ports.split(",")
        targetList, portList = [s.strip() for s in targetList], [s.strip() for s in portList]
        
        # Validate target IP was found
        for x in range(len(targetList)):
            if returnTarget(targetList[x]) == None:
                print(f"{Fore.LIGHTRED_EX}Target '{targetList[x]}' could not be located{Style.RESET_ALL}")
                sys.exit()

        # If target is a list and port is a range
        if ("-" in ports):
            portRange = ports.split("-")
            ports1 = ports
            for x in range(len(targetList)):
                banner(targetList[x], ports1, returnTarget(targetList[x]))
                ports = range(int(portRange[0]), int(portRange[1]) + 1)
                for port, status in pool.imap(scan, [(target_ip, int(port)) for port in ports]):
                    displayScan()

        # Else if target and port is a list
        else:
            # Remove invalid port from list 
            for x in range(len(portList)):
                if (int(portList[x]) > 66036 or int(portList[x]) < 0):
                    print(f"{Fore.LIGHTRED_EX}Port '{portList[x]}' removed from list{Style.RESET_ALL}")
                    portList.pop(x)
                   
            for x in range(len(targetList)):
                    for y in range(len(portList)):
                        target_ip = returnTarget(targetList[x])
                        portString = ",".join(str(element) for element in portList)
                        banner(targetList[x], portString,target_ip)   
                        ports = range(int(min(portList)), int(max(portList))+1)
                        for port, status in pool.imap(scan, [(target_ip, int(port)) for port in ports]):
                            if (str(port) in portList):
                                displayScan()
    else:
        # If target is invalid
        if (returnTarget(target) == None):
            print(f"{Fore.LIGHTRED_EX}Target '{target}' could not be located{Style.RESET_ALL}")
            sys.exit()

        

        if ("-" in ports):
            portRange = ports.split("-")
            print(portRange)
            target_ip = returnTarget(target.strip())
            banner(target, ports,target_ip)
            ports = range(int(portRange[0]), int(portRange[1]) + 1)
            for port, status in pool.imap(scan, [(target_ip, int(port)) for port in ports]):
                    displayScan()   

        # Single target and port     
        else:
            target_ip = returnTarget(target.strip())
            banner(target, ports, target_ip)
            for port, status in pool.imap(scan, [(target_ip, int(ports)) for ports in ports]):
                displayScan()
                  