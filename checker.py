import sys
import socket


if len(sys.argv) not in [2, 3]:
    print("You are missing the arguments!")
    print("Please input the server's address, it can be ip address or the domain name (requiered) ")
    print("Please input the server's port (value between 1 65535 and ) (optional)")
    exit(1)

ipAddr = sys.argv[1]

try:
    if len(sys.argv) == 3:
        port = int(sys.argv[2])
        assert ((int(port) >= 1) and (int(port) <= 65535))
    else:
        port = 80
except AssertionError:
    print("The port number is not valid!!")
    exit(2)

h_initial = "HEAD / HTTP/1.0\r\n Host:"
h_final = "\r\nConnection: close\r\n\r\n"
encoder = "utf-8"
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    mySocket.connect((ipAddr, int(port)))
except socket.timeout:
    print("The connection has been timeout!")
    exit(3)
except socket.gaierror:
    print("The ip address or the name of the Http server is not valid! ")
    exit(4)

mySocket.send(bytes(h_initial, encoder) +
              bytes(ipAddr, encoder) + bytes(h_final, encoder))

reply = mySocket.recv(100).decode("utf-8")
mySocket.shutdown(socket.SHUT_RDWR)
mySocket.close()
print(reply)
print(reply[:reply.find("\r")])
