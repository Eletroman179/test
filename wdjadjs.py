import socket
import requests

def get_ip():
    r = requests.get("https://api.ipify.org?format=json")
    return r.json()["ip"]

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
public_ip = get_ip()

print("\n\nI hacked into yocur pc i know your ip addr")
print("it is\n")

print("Your Computer Name is:", hostname)
print("Your Computer IP Address is:", IPAddr) # I did't but if he sees this cool
print("Your Public facing IP Address is:", public_ip)
