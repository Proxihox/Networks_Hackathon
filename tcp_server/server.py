import socket
import os

# Server configuration
HOST = '127.0.0.1'  # Localhost (adjust as needed)
PORT = 65432        # Non-privileged port
UPLOAD_FOLDER = './tcp_server/mem'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def receive_file(conn):
    # Receive file name
    file_name = conn.recv(1024).decode().strip()  # Assuming the file name fits in 1024 bytes
    file_size = int(conn.recv(1024).decode())     # Assuming file size fits in 1024 bytes
    
    # Save the received file
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    with open(file_path, 'wb') as file:
        file_data = conn.recv(file_size)  # Receive the entire file in one go
        file.write(file_data)
    print(f"File '{file_name}' received and saved.")

def send_file(conn, file_name):
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    print("IMP",file_path)
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        
        # Send the file name and size
        #conn.send(file_name.encode().ljust(1024))  # Send file name (padded)
        conn.send(str(file_size).encode().ljust(1024))  # Send file size (padded)
        print("IMP2",file_path)
        # Send the file in one go
        with open(file_path, 'rb') as file:
            file_data = file.read()  # Read the entire file
            conn.sendall(file_data)  # Send the file in one go
        print(f"File '{file_name}' sent.")
    else:
        print(f"File '{file_name}' not found and not sent.")
        conn.send(b'File not found')

def handle_client(conn):
    try:
        # Receive operation type (upload or download)
        operation = conn.recv(1024).decode().strip()
        if operation == 'upload':
            receive_file(conn)
        elif operation == 'download':
            file_name = conn.recv(1024).decode().strip()  # Receive the file name
            send_file(conn, file_name)
        else:
            print("Unknown operation.")
    finally:
        conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f"Server listening on {HOST}:{PORT}...")
        while True:
            conn, addr = server_socket.accept()
            print(f"Connected by {addr}")
            handle_client(conn)

if __name__ == "__main__":
    start_server()
