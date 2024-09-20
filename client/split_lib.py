# Library file for both the functions
import requests
import os
import socket
from time import *

HOST = '127.0.0.1'  # Server IP
PORT = 65432        # Server port

def split_store(file_name) :
    # Split store code
    file = open('./client/mem/'+file_name, 'r')
    i=0
    while 1:
        chunk = file.read(1024)
        if chunk=='':
            break
        file_path='./client/mem/'+str(i)+file_name
        file_to_send=open(file_path,'w')
        file_to_send.write(chunk)
        file_to_send.close()
        if i%2==0:
            with open(file_path, 'rb') as file2:
                response = requests.post('http://localhost:5000/upload', files={'file': file2})
        else:
            file_size = os.path.getsize(file_path)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((HOST, PORT))
                client_socket.sendall(b'upload'.ljust(1024))
                
                client_socket.sendall((str(i)+file_name).encode().ljust(1024))
                client_socket.sendall(str(file_size).encode().ljust(1024))

                with open(file_path, 'rb') as file_to_send:
                    client_socket.sendall(file_to_send.read())
        i+=1
    file.close()
    pass

def split_fetch(file_name) :
    # Split fetch code'
    i=0
    file_path='./client/mem/'+file_name
    file_to_write=open(file_path,'w')
    file_to_write.close()
    file_to_write=open(file_path,'ab')
    cont=True
    while cont:
        if i%2==0:
            response = requests.get('http://localhost:5000/download/'+str(i)+file_name, stream=True)
            if response.status_code == 200:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file_to_write.write(chunk)
            else:
                cont=False
                break
        else:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((HOST, PORT))
                client_socket.sendall(b'download'.ljust(1024))  # Send operation type

                # Send file name
                client_socket.sendall((str(i)+file_name).encode().ljust(1024))
                
                # file not present
                if client_socket.recv(1024).decode().strip() == 'File not found':
                    cont=False
                    client_socket.close()
                    break

                # Receive the entire file in one go
                
                file_data = client_socket.recv(1024)
                # Save the file
                file_to_write.write(file_data)
        i+=1
    file_to_write.close()
    pass