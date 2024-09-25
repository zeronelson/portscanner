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
    print(f"{Fore.RED}")
    target_info = target_name + ": " + target_ip
    if "-" in port:
        print("*" * 70)
        print(f"Scanning ({target_info}) for ports {port} ")
        print("*" * 70)
    elif "," in port:
        ports = port.split(",")
        if (len(ports) == 2):
            print("*" * 70)
            print(f"Scanning ({target_info}) for ports {ports[0]} and {ports[1]}")
            print("*" * 70)
        else:
            print("*" * 70)
            print(f"Scanning ({target_info}) for ports {port} ")
            print("*" * 70) 
    else:
        if int(port) > 0: 
            print("*" * 70)
            print(f"Scanning ({target_info}) for port {port} ")
            print("*" * 70)
        else: 
            print("*" * 70)
            print(f"Scanning ({target_info}) for ports 1-1065")
            print("*" * 70)

def displayScan():
    try:
        answer = socket.getservbyport(port)
        print(f"{Fore.GREEN}{port:4d}: Open {Style.RESET_ALL}  ({answer})")
    except(socket.error):
        print(f"{Fore.RED}{port:4d}: Closed ")   

if __name__ == '__main__':
    subprocess.call('clear', shell=True) # Clears screen
    print("""▗▄▄▖  ▗▄▖ ▗▄▄▖ ▗▄▄▄▖     ▗▄▄▖ ▗▄▄▖ ▗▄▖ ▗▖  ▗▖▗▖  ▗▖▗▄▄▄▖▗▄▄▖ 
▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌  █      ▐▌   ▐▌   ▐▌ ▐▌▐▛▚▖▐▌▐▛▚▖▐▌▐▌   ▐▌ ▐▌
▐▛▀▘ ▐▌ ▐▌▐▛▀▚▖  █       ▝▀▚▖▐▌   ▐▛▀▜▌▐▌ ▝▜▌▐▌ ▝▜▌▐▛▀▀▘▐▛▀▚▖
▐▌   ▝▚▄▞▘▐▌ ▐▌  █      ▗▄▄▞▘▝▚▄▄▖▐▌ ▐▌▐▌  ▐▌▐▌  ▐▌▐▙▄▄▖▐▌ ▐▌                                                                                                                                                                                 """)
    pool = Pool(processes=30)
    #target = input('Enter IPs/hostnames (separated by commas): ')
    #ports = input('Enter port(s) or 0 to skip (list with commas/range with dash): ')
    
    target = "target.com, walmart.com"
    ports = "1-3"
    
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
                print(f"{Fore.LIGHTRED_EX}\nTarget '{targetList[x]}' could not be located{Style.RESET_ALL}")
                sys.exit()

        # If target is a list and port is a range
        if ("-" in ports):
            portRange = ports.split("-")
            ports1 = ports
            for x in range(len(targetList)):
                target_ip =  returnTarget(targetList[x])
                banner(targetList[x], ports1, target_ip)
                ports = range(int(portRange[0]), int(portRange[1]) + 1)
                for port, status in pool.imap(scan, [(target_ip, int(port)) for port in ports]):
                    displayScan()

        # Else if target and port is a list
        else: 
            for x in range(len(targetList)):
                for y in range(len(portList)):
                    target_ip = returnTarget(targetList[x])
                    portString = ",".join(str(x) for x in portList)
                    banner(targetList[x],portString,target_ip)   
                    ports = range(int(min(portList)), int(max(portList))+1)
                    for port, status in pool.imap(scan, [(target_ip, int(port)) for port in ports]):
                        if (str(port) in portList):
                            displayScan()
                    break
    else:
        # If target is invalid
        if (returnTarget(target) == None):
            print(f"{Fore.LIGHTRED_EX}\nTarget '{target}' could not be located{Style.RESET_ALL}")
            sys.exit()

        if ("-" in ports):
            portRange = ports.split("-")

            if portRange[0] == "":
                print(f"{Fore.LIGHTRED_EX}\nCheck port input{Style.RESET_ALL}")
                sys.exit()
            
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
                
    print(f"{Fore.LIGHTRED_EX}\nExiting...{Style.RESET_ALL}")
