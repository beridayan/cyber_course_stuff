import socket
import time
import os
server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip = '127.0.0.1'
port = 12345
file_name = 'secret_message.jpg' 

file_path = os.path.join('C:\\Users\\berid\\Downloads\\',file_name)
server_sock.connect((ip,port))
server_sock.send(file_name.encode())
time.sleep(0.2)
with open(file_path,'rb') as f :
    while True:
        bytes = f.read(4096)
        if not bytes:
            break
        server_sock.sendall(bytes)
print("file sent")