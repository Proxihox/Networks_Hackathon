import socket
import os
import sys

# Server configuration
HOST = '127.0.0.1'  # Server IP
PORT = 65432        # Server port

file_dir = './mem'

def upload_file(file_name):
    file_path = file_name
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            client_socket.sendall(b'upload'.ljust(1024))  # Send operation type
            
            # Send file name and file size
            client_socket.sendall(file_name.encode().ljust(1024))
            client_socket.sendall(str(file_size).encode().ljust(1024))

            # Send the entire file in one go
            with open(file_path, 'rb') as file:
                client_socket.sendall(file.read())  # Read and send the file
            print(f"File '{file_name}' uploaded.")
    else:
        print(f"File '{file_name}' not found.")

def download_file(file_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(b'download'.ljust(1024))  # Send operation type

        # Send file name
        client_socket.sendall(file_name.encode().ljust(1024))

        # Receive the file size
        file_size = int(client_socket.recv(1024).decode().strip())

        # Receive the entire file in one go
        file_data = client_socket.recv(file_size)

        # Save the file
        file_path = f'./{file_name}'
        with open(file_path, 'wb') as file:
            file.write(file_data)
        print(f"File '{file_name}' downloaded.")

