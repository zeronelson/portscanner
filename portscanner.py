import socket
import subprocess
import sys
from multiprocessing import Pool
from colorama import Fore, Style
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

def isValidTarget(target):
    try: 
        socket.inet_aton(target)
        return True
    except:
        return True
   
def isValidList(targetList, portList):
    if not isValidTarget(targetList) and (int(portList) > 65536):
        print(f"\n{Fore.LIGHTRED_EX} Check your target(s) and port(s)...{Style.RESET_ALL}")
        sys.exit()
    if  isValidTarget(targetList) == False:
        print(f"\n{Fore.LIGHTRED_EX}Check your target(s)... '{targetList}' is not a valid target{Style.RESET_ALL}")
        sys.exit()    
    if int(portList) >  65536:
        print(f"\n{Fore.LIGHTRED_EX}Check your port(s)... '{portList}' is not a valid port{Style.RESET_ALL}")
        sys.exit()

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
    
def validateTarget(target):
    try: 
        socket.inet_aton(target)
        return target
    except:
        try:
            return socket.gethostbyname(target)
        except:
            return None

def banner(port, target_ip):
    print("\n")
    print(f"{Fore.RED}")
    if "-" in port:
        print("*" * 55)
        # TODO - How to display hostname
        print(f"Scanning remote host ({target_ip}) for ports {port} ")
        print("*" * 55)
    elif "," in port:
        # TODO - Can delineate ports 
        print("*" * 55)
        print(f"Scanning remote host ({target_ip}) for ports {port} ")
        print("*" * 55)
    '''else:
        if int(port) > 0: 
            print("*" * 55)
            print(f"Scanning remote host ({target_ip}) for port {port} ")
            print("*" * 55)
        else: 
            print("*" * 55)
            print(f"Scanning remote host ({target_ip}) for ports 1-1065")
            print("*" * 55)'''

def displayScan():
    try:
        answer = socket.getservbyport(port)
        print(f"{Fore.GREEN}{port:4d}: Open {Style.RESET_ALL}  ({answer})")
    except(socket.error):
        print(f"{Fore.RED}{port:4d}: Closed ")   

if __name__ == '__main__':
    subprocess.call('clear', shell=True) # Clears screen
    #subprocess.Popen('color 4', shell=True) # Change color
    '''print("""
        ██████╗  ██████╗ ██████╗ ████████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
        ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
        ██████╔╝██║   ██║██████╔╝   ██║       ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
        ██╔═══╝ ██║   ██║██╔══██╗   ██║       ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
        ██║     ╚██████╔╝██║  ██║   ██║       ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
        ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝       ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝                                                                                                    
""")'''
    pool = Pool(processes=10)
    #target = input('Enter IPs/hostnames (separated by commas): ')
    #ports = input('Enter port(s) or 0 to skip (list with commas/range with dash): ')
    
    target = "target.com, walmart.com"
    ports = "1-3"

    # If input is a list
    if ("," in target or "," in ports):
        # Split by comma and strip string for processing
        targetList, portList = target.split(","), ports.split(",")
        targetList, portList = [s.strip() for s in targetList], [s.strip() for s in portList]
        
        # Validate target exists
        for x in range(len(targetList)):
            target_ip = validateTarget(targetList[x])
            if target_ip == None:
                print(f"{Fore.LIGHTRED_EX}Target '{targetList[x]}' could not be located{Style.RESET_ALL}")
                sys.exit()

        if ("-" in ports):
            portRange = ports.split("-")
            ports1 = ports
            for x in range(len(targetList)):
                #isValidList(targetList[x],portRange[0])
                #target_ip = validateTarget(targetList[x])
                banner(ports1,target_ip)
                ports = range(int(portRange[0]), int(portRange[1]) + 1)
                for port, status in pool.imap(scan, [(target_ip, int(port)) for port in ports]):
                    displayScan()
        else:
            for x in range(len(targetList)):
                    for y in range(len(portList)):
                        isValidList(targetList[y], portList[y])
                        target_ip = validateTarget(targetList[x])
                        portString = ",".join(str(element) for element in portList)
                        banner(portString,target_ip)   
                        ports = range(int(min(portList)), int(max(portList))+1)
                        # Loop through range, but only print the ports requested by the user
                        for port, status in pool.imap(scan, [(target_ip, int(port)) for port in ports]):
                            if (str(port) in portList):
                                displayScan()
                        break
    else:
        if ("-" in ports):
            target = target.strip()
            portRange = ports.split("-")
            isValidList(target,portRange[0])
            target_ip = validateTarget(target)
            banner(ports,target_ip)
            ports = range(int(portRange[0]), int(portRange[1]) + 1)
            for port, status in pool.imap(scan, [(target_ip, int(port)) for port in ports]):
                    displayScan()        
        else:
            target = target.strip()
            if int(ports) != 0: 
                target_ip = validateTarget(target)
                isValidList(target, ports)
                banner(ports, target_ip)
                for port, status in pool.imap(scan, [(target_ip, int(ports)) for port in ports]):
                    displayScan()
                    break         
            else:
                isValidList(target, ports)
                target_ip = validateTarget(target)
                banner(ports, target_ip)
                ports = range(1, 1065)
                for port, status in pool.imap(scan, [(target_ip, port) for port in ports]):
                    displayScan()
                        
    print(f"\n{Fore.WHITE}{Style.NORMAL}")