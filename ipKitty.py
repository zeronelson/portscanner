import socket
import re
import subprocess
import sys

subprocess.call('cls', shell=True)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
print('*'*52)
msg = "Current User"
print("                   Current User\n            ")
print(f"Hostname: {hostname}   IP Address: {ip}")
print('*'*52)
sock.close()

option = input("\nEnter IP or Hostname: ")

ipPattern = '^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$'
ipMatch = bool(re.match(ipPattern, option))     
hnPattern = '^[A-Za-z0-9]+\.[A-Za-z]+$'
hnMatch = bool(re.match(hnPattern, option))

count = 0
if ipMatch:
    hostname = socket.gethostbyaddr(option)
    print(f"\nHostname: {hostname}")
if hnMatch:
    ip = socket.gethostbyname(option)
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
    option = input("Enter full hostname or IP: ")
    ipMatch = bool(re.match(ipPattern, option))
    hnMatch = bool(re.match(hnPattern, option))

    if ipMatch:
        hostname = socket.gethostbyaddr(option)
        print(f"\nHostname: {hostname}")
    if hnMatch:
        ip = socket.gethostbyname(option)
        print(f"\nIP: {ip}")
print('*'*52)


