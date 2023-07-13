import socket
import re
import subprocess
import sys

def startSock():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print('*'*52)
    msg = "Current User"
    print("                   Current User\n            ")
    print(f"Hostname: {hostname}   IP Address: {ip}")
    print('*'*52)
    sock.close()

def findTarget(target):
    ipPattern = '^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$'
    ipMatch = bool(re.match(ipPattern, target))     
    hnPattern = '^[A-Za-z0-9]+\.[Agit -Za-z]+$'
    hnMatch = bool(re.match(hnPattern, target))
    count = 0

    if ipMatch:
        print(target)
        target = str(target)
        hostname = socket.gethostbyaddr(target)
        print(f"\nHostname: {hostname[0]}")
    if hnMatch:
        print(target.capitalize())
        ip = socket.gethostbyname(target)
        print(f"\nIP: {ip}")

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
        target = input("Enter full hostname or IP: ")
        ipMatch = bool(re.match(ipPattern, target))
        hnMatch = bool(re.match(hnPattern, target))

        if ipMatch:
            print(target)
            hostname = socket.gethostbyaddr(target)
            print(f"\nHostname: {hostname}")
        if hnMatch:
            print(target.capitalize())
            ip = socket.gethostbyname(target)
            print(f"\nIP: {ip}")
    print('*'*52)

def multipleTargets(targetList):
    for x in range(len(targetList)):    
       findTarget(targetList[x])


subprocess.call('cls', shell=True)
startSock()


print("\n*** You may entire a single target or multiple targets separated by a comma ***\n")
target = input("Enter target(s): ")
print("\n")
print('*'*52)

if "," in target:
    targetList = target.split(",")
    targetList = [s.strip() for s in targetList]
    multipleTargets(targetList)
else:
    findTarget(target)
    