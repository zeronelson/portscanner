import socket
import subprocess
import sys
import re
from multiprocessing import Pool

def isValidTarget(target):
    ipPattern = '^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$'
    ipMatch = bool(re.match(ipPattern, target))     
    hnPattern = '^[A-Za-z0-9]+\.[Agit -Za-z]+$'
    hnMatch = bool(re.match(hnPattern, target))

    if ipMatch or hnMatch:
       return True
    else: 
        return False
    
def checkList(targetList, portList):
    if not isValidTarget(targetList) and (int(portList) > 65536):
        print("\n\033[4m Check your target(s) and port(s)...")
        subprocess.Popen('color 0F', shell=True)
        sys.exit()
    if  isValidTarget(targetList) == False:
        print(f"\nCheck your target(s)... {targetList} is not a valid target")
        subprocess.Popen('color 0F', shell=True)
        sys.exit()    
    if int(portList) >  65536:
        print(f"\nCheck your port(s)... {portList} is not a valid port")
        subprocess.Popen('color 0F', shell=True)
        sys.exit()

def scan(arg):
    target_ip, port = arg
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        sock.connect((target_ip, port))
        sock.close()
        return port, True
    except (socket.timeout, socket.error):
        return port, False
    
def findTarget(target):
    givenData = target
    ipPattern = '^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$'
    ipMatch = bool(re.match(ipPattern, givenData))     
    hnPattern = '^[A-Za-z0-9]+\.[A-Za-z]+$'
    hnMatch = bool(re.match(hnPattern, givenData))

    count = 0
    if ipMatch:
        return givenData
    if hnMatch:
        target_ip = socket.gethostbyname(givenData)
        return target_ip

    while not ipMatch and not hnMatch:
        if count == 0:
            print(">>> Invalid hostname or IP")
        count += 1
        if count == 2:
            print(">>> One more chance")
        if count == 3:
            print("Exiting...")
            subprocess.Popen('color 0F', shell=True)
            sys.exit()
        givenData = input("Enter full hostname or IP: ")
        ipMatch = bool(re.match(ipPattern, givenData))
        hnMatch = bool(re.match(hnPattern, givenData))

        if ipMatch:
            target_ip = givenData 
            return target_ip
        if hnMatch:
            target_ip = socket.gethostbyname(givenData)
            return target_ip

def banner(port, target_ip):
    print("\n")
    if int(port) > 0: 
        print("*" * 52)
        print(f"Scanning remote host ({target_ip}) for port {port} ")
        print("*" * 52)
    else: 
        print("*" * 52)
        print(f"Scanning remote host ({target_ip}) for ports 1-1065")
        print("*" * 52)


if __name__ == '__main__':
    subprocess.call('cls', shell=True) # Clears screen
    subprocess.Popen('color 4', shell=True) # Change color
    print("""
        ██████╗  ██████╗ ██████╗ ████████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
        ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
        ██████╔╝██║   ██║██████╔╝   ██║       ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
        ██╔═══╝ ██║   ██║██╔══██╗   ██║       ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
        ██║     ╚██████╔╝██║  ██║   ██║       ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
        ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝       ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝                                                                                                    
""")
    ports = range(1, 1065)
    pool = Pool(processes=10)
    target = input('Enter IPs/hostnames (separated by commas): ')
    ports = input('Enter port(s) or 0 to skip (separated by commas): ')

    if ("," in target and ports) or ("," in target or "," in ports):
        targetList = target.split(",")
        portList = ports.split(",")
        targetList = [s.strip() for s in targetList]
        portList = [s.strip() for s in portList]
        if len(targetList) > len(portList):
            for x in range(len(targetList)):
                for y in range(len(portList)):
                    checkList(targetList[x], portList[y])
                    target_ip = findTarget(targetList[x])
                    banner(portList[y],target_ip)
                    for port, status in pool.imap(scan, [(target_ip, int(portList[y])) for port in ports]):
                        print(port, ':', 'Open' if status else 'Closed')
                        break
        elif len(targetList) < len(portList):
            for x in range(len(portList)):
                for y in range(len(targetList)):
                    checkList(targetList[y], portList[x])
                    target_ip = findTarget(targetList[y])
                    banner(portList[x],target_ip)
                    for port, status in pool.imap(scan, [(target_ip, int(portList[x])) for port in ports]):
                        print(port, ':', 'Open' if status else 'Closed')
                        break
        else:
            for x in range(len(targetList)):
                for y in range(len(portList)):
                    checkList(targetList[x], portList[y])
                    target_ip = findTarget(targetList[x])
                    banner(portList[y],target_ip)
                    for port, status in pool.imap(scan, [(target_ip, int(portList[y]))]):
                        print(port, ':', 'Open' if status else 'Closed')
                        break
    else:
        target = target.strip()
        if int(ports) != 0: 
            checkList(target, ports)
            target_ip = findTarget(target)
            banner(ports, target_ip)
            for port, status in pool.imap(scan, [(target_ip, int(ports)) for port in ports]):
                print(port, ':', 'Open' if status else 'Closed')
                break
        else:
            checkList(target, ports)
            target_ip = findTarget(target)
            banner(ports, target_ip)
            ports = range(1, 1065)
            for port, status in pool.imap(scan, [(target_ip, port) for port in ports]):
                print(port, ':', 'Open' if status else 'Closed')
    print("\n")
    subprocess.Popen('color 0F', shell=True) # Change color
