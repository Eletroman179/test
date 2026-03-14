import socket

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

print("I hacked into yocur pc i know your ip addr")
print("it is\n")

print("Your Computer Name is:", hostname)
print("Your Computer IP Address is:", IPAddr)
