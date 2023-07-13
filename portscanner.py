import socket
import subprocess
import sys 
import re
from datetime import datetime

def scanOne(remServerIP, port):
    startTime = datetime.now()
    try:
        if port == 0:
            for port in range(1, 1065):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((remServerIP, port))
                sock.settimeout(0.1)
                sock.setblocking(1)
                if result == 0:
                    print(f"\nPort {port}:    Open")
                else:
                    print(f"\nPort {port}:    Closed")
                sock.close()
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((remServerIP, port))
            sock.settimeout(0.1)
            sock.setblocking(1)
            if result == 0:
                print(f"\nPort {port}:    Open")
            else:
                print(f"\nPort {port}:    Closed")
            sock.close()

    except KeyboardInterrupt:
        print("Oops, you pressed CTRL+C")
        subprocess.Popen('color 0F', shell=True)
        sys.exit()

    except socket.gaierror:
        print("Oops, hostname could not be resolved.")
        subprocess.Popen('color 0F', shell=True)
        sys.exit()

    except socket.error:
        print("Couldn't connect to server")
        subprocess.Popen('color 0F', shell=True)
        sys.exit()

    endTime = datetime.now()

    time = endTime - startTime

    print(f"\nElapsed Time: {time}")

def getPort():
    port = int(input("Scan for particular port (Enter 0 to skip): "))
    count = 0
    while port > 65536:
        if count == 0:
            print(">>> Invalid port")
        count += 1
        if count == 2:
            print(">>> One more chance")
        if count == 3:
            print("Exiting...")
            sys.exit()
        port = int(input("Scan for particular port (Enter 0 or port number): "))
    return port

def banner(port):
    print("\n")
    if int(port) > 0: 
        print("*" * 52)
        print(f"Scanning remote host ({remServerIP}) for port {port} ")
        print("*" * 52)
    else: 
        print("*" * 52)
        print(f"Scanning remote host ({remServerIP}) ")
        print("*" * 52)

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
        remServerIP = socket.gethostbyname(givenData)
        return remServerIP

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
            remServerIP = givenData 
            return remServerIP
        if hnMatch:
            remServerIP = socket.gethostbyname(givenData)
            return remServerIP
        
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

def isValidTarget(target):
    ipPattern = '^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$'
    ipMatch = bool(re.match(ipPattern, target))     
    hnPattern = '^[A-Za-z0-9]+\.[Agit -Za-z]+$'
    hnMatch = bool(re.match(hnPattern, target))
    count = 0

    if ipMatch or hnMatch:
       return True
    else: 
        return False

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

target = input("Enter IPs/hostnames: ")
targetPorts = input("Enter port(s) or 0 to skip: ")

if ("," in target and targetPorts) or ("," in target or targetPorts):
    targetList = target.split(",")
    portList = targetPorts.split(",")
    targetList = [s.strip() for s in targetList]
    portList = [s.strip() for s in portList]
    if len(targetList) > len(portList):
        for x in range(len(targetList)):
            for y in range(len(portList)):
                checkList(targetList[x], portList[y])
                remServerIP = findTarget(targetList[x])
                banner(portList[y])
                scanOne(remServerIP, int(portList[y]))
    elif len(targetList) < len(portList):
        for x in range(len(portList)):
            for y in range(len(targetList)):
                checkList(targetList[y], portList[x])
                remServerIP = findTarget(targetList[y])
                banner(portList[x])
                scanOne(remServerIP, int(portList[x]))
    else:
        for x in range(len(targetList)):
            for y in range(len(portList)):
                checkList(targetList[x], portList[y])
                remServerIP = findTarget(targetList[x])
                banner(portList[y])
                scanOne(remServerIP, int(portList[y]))
else:
    checkList(target, targetPorts)
    print("WE SHOULD BE HERE")
    remServerIP = findTarget(target)
    banner(targetPorts)
    scanOne(remServerIP, int(targetPorts))

print("""
            █████████████████████████
            ███████           ███████
            ███████           ███████
            ██                     ██
            ██                     ██
            ██                     ██
            ██                     ██
            ██    █   █   █   █    ██
            ██    █   █   █   █    ██
            ██    █   █   █   █    ██
            █████████████████████████
      """)
subprocess.Popen('color 0F', shell=True) # Change color

