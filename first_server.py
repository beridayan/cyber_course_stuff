import socket
import os
import time
server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip = '127.0.0.1'
port = 12345
server_sock.bind((ip,port))
server_sock.listen()
print("listening for connection")
client_sock , addres = server_sock.accept()
print("connection from ", addres)
time.sleep(0.2)
name = client_sock.recv(1024).decode()
time.sleep(0.2)
file_data = client_sock.recv(4096)
with open(os.path.join('C:\\Users\\berid\\Downloads\\first\\',name),'wb') as f:
    f.write(file_data)
print(" file saved in ",'C:\\Users\\berid\\Downloads\\first\\',name)