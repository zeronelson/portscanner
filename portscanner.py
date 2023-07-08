import socket
import subprocess
import sys 
import re
from datetime import datetime

def scanPorts(remServerIP):
    startTime = datetime.now()
    try:
        for port in range(1,1065):
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
        sys.exit()

    except socket.gaierror:
        print("Oops, hostname could not be resolved.")
        sys.exit()

    except socket.error:
        print("Couldn't connect to server")
        sys.exit()

    endTime = datetime.now()

    time = endTime - startTime

    print(f"\nElapsed Time: {time}")

def checkPort(remServerIP, port):
    startTime = datetime.now()
    try:
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
        sys.exit()

    except socket.gaierror:
        print("Oops, hostname could not be resolved.")
        sys.exit()

    except socket.error:
        print("Couldn't connect to server")
        sys.exit()

    endTime = datetime.now()

    time = endTime - startTime

    print(f"\nElapsed Time: {time}")

def getTarget():
    givenData = input("Enter hostname or IP to scan: ")
    ipPattern = '^(?:(25[0-5]|(?:2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}$'
    result = re.match(ipPattern, givenData)
    if result:
        remServerIP = (givenData)
    else:
        remServerIP = socket.gethostbyname(givenData)
    return remServerIP

def getPort():
    port = int(input("Scan for particular port (Enter 0 or port number): "))
    return port

def banner(port):
    if port: 
        print("*" * 50)
        print(f"Scanning remote host ({remServerIP}) for port {port} ")
        print("*" * 50)
    else: 
        print("*" * 50)
        print(f"Scanning remote host ({remServerIP}) ")
        print("*" * 50)

def scan(port):
    if port != 0:
        banner(port) 
        checkPort(remServerIP, port)
    else:
        banner(port)
        scanPorts(remServerIP)

subprocess.call('cls', shell=True) # Clears screen

remServerIP = getTarget() 
port = int(getPort())
scan(port)

