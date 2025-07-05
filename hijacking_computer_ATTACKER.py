import socket

server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip = '127.0.0.1'
port = 12345
server_sock.bind((ip,port))
server_sock.listen()
print("listening for connection")
client_sock , addres = server_sock.accept()
print("connection from ", addres)
while True:
    mesage = client_sock.recv(1024).decode()
    print(mesage)
