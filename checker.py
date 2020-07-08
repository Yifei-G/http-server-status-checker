import sys
import socket

# If the argument is less than 2 or more 3, then raise error and finish
# the program
if len(sys.argv) not in [2, 3]:
    print("You are missing the arguments!")
    print("Please input the server's address, it can be ip address or the domain name (requiered) ")
    print("Please input the server's port (value between 1 65535 and ) (optional)")
    exit(1)

ipAddr = sys.argv[1]

try:
    if len(sys.argv) == 3:
        port = int(sys.argv[2])
        # be sure that the port number is between 1 and 65535
        assert ((int(port) >= 1) and (int(port) <= 65535))
    else:
        port = 80
except AssertionError:
    print("The port number is not valid!!")
    exit(2)
# preparing the http header
h_initial = "HEAD / HTTP/1.0\r\n Host:"
# explicitly tell the server to close the connection
h_final = "\r\nConnection: close\r\n\r\n"
encoder = "utf-8"
# build my socket
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # connecting to the server using the socket object
    mySocket.connect((ipAddr, int(port)))
except socket.timeout:
    print("The connection has been timeout!")
    exit(3)
except socket.gaierror:
    print("The ip address or the name of the Http server is not valid! ")
    exit(4)

# if the connection is successful, then send the data to the server
mySocket.send(bytes(h_initial, encoder) +
              bytes(ipAddr, encoder) + bytes(h_final, encoder))

# expecting the respose from the server, decode it using utf-8
reply = mySocket.recv(100).decode("utf-8")
# close the socket
mySocket.shutdown(socket.SHUT_RDWR)
mySocket.close()
# print the http status code on the terminal
print(reply[:reply.find("\r")])
