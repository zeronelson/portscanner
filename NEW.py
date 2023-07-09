import socket
import subprocess
import sys 
import re
import os
from datetime import datetime

def getTarget():
    try:
        print("""
        ██████╗  ██████╗ ██████╗ ████████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
        ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
        ██████╔╝██║   ██║██████╔╝   ██║       ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
        ██╔═══╝ ██║   ██║██╔══██╗   ██║       ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
        ██║     ╚██████╔╝██║  ██║   ██║       ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
        ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝       ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
                                                                                                        
        """)
        givenData = input("Enter full hostname or IP to scan: ")
        remServerIP = 0
        ipPattern = '^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$'
        ipMatch = bool(re.match(ipPattern, givenData))
        
        hnPattern = '^[A-Za-z0-9]+\.[A-Za-z]+$'
        hnMatch = bool(re.match(hnPattern, givenData))

        count = 0
        while not ipMatch and not hnMatch:
            if count == 0:
                print("Invalid hostname or IP")

            givenData = input("Enter full hostname or IP: ")
            ipMatch = bool(re.match(ipPattern, givenData))
            hnMatch = bool(re.match(hnPattern, givenData))
            
            if ipMatch:
                remServerIP = givenData 
                print(f"IP: {remServerIP}")
                return remServerIP
                
            if hnMatch:
                remServerIP = socket.gethostbyname(givenData)
                print(f"IP: {remServerIP}")
                return remServerIP
            
            count += 1
            if count == 2:
                 print("One more chance")
            if count == 3:
                print("Exiting...")
                sys.exit()
    except KeyboardInterrupt:
            print("\nExiting...")
            subprocess.Popen('color 0F', shell=True)
            sys.exit()

    

def getPort():
    try:
        port = int(input("Scan for particular port (Enter 0 or port number): "))
        return port
    except KeyboardInterrupt:
                print("\nOops, you pressed CTRL+C")
                subprocess.Popen('color 0F', shell=True)
                sys.exit()

def banner(port):
    print("\n")
    if port: 
        print("*" * 50)
        print(f"Scanning remote host ({remServerIP}) for port ({port}) ")
        print("*" * 50)
    else: 
        print("*" * 50)
        print(f"Scanning remote host ({remServerIP}) ")
        print("*" * 50)

def scanMultiple(remServerIP):
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

def scanOne(remServerIP, port):
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

def scan(port):
    if port != 0:
        banner(port) 
        scanOne(remServerIP, port)
    else:
        banner(port)
        scanMultiple(remServerIP)

subprocess.Popen('color 4', shell=True)
subprocess.call('cls', shell=True) # Clears screen
remServerIP = getTarget() 
port = int(getPort())
scan(port)
subprocess.Popen('color 0F', shell=True)

