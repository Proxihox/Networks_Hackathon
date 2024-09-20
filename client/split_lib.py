import requests
import socket

# Constants
CHUNK_SIZE = 1024
HTTPS_SERVER_URL = "http://127.0.0.1:5000/upload"  # Adjust according to your HTTP server setup
HTTPS_DOWNLOAD_URL = "http://127.0.0.1:5000/download"
TCP_SERVER_HOST = "127.0.0.1"  # Adjust according to your TCP server setup
TCP_SERVER_PORT = 65432
USERNAME = "admin"
PASSWORD = "password"

def send_chunk_via_https(chunk_data, chunk_name):
    files = {'file': (chunk_name, chunk_data)}
    response = requests.post(HTTPS_SERVER_URL, files=files, auth=(USERNAME, PASSWORD))
    return response.status_code == 200

def send_chunk_via_tcp(chunk_data, chunk_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TCP_SERVER_HOST, TCP_SERVER_PORT))
        s.sendall(b'{"username": "admin", "password": "password"}'.ljust(1024))  # Send credentials
        s.sendall(b'upload'.ljust(1024))
        # Send the file name and chunk data
        s.sendall(chunk_name.encode().ljust(1024))  # Send file name (padded)
        s.sendall(str(len(chunk_data)).encode().ljust(1024))  # Send file size
        s.sendall(chunk_data)  # Send actual chunk data
        # Expecting no response from the server (simple confirmation)
        return True

def receive_chunk_via_https(chunk_name):
    response = requests.get(f"{HTTPS_DOWNLOAD_URL}/{chunk_name}", auth=(USERNAME, PASSWORD))
    if response.status_code == 200:
        return response.content
    return None

def receive_chunk_via_tcp(chunk_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TCP_SERVER_HOST, TCP_SERVER_PORT))
        s.sendall(b'{"username": "admin", "password": "password"}'.ljust(1024))  # Send credentials
        # Send the operation (download)
        s.sendall(b'download'.ljust(1024))
        # Send the file name to download
        s.sendall(chunk_name.encode().ljust(1024))  # Send file name (padded)
        # Receive the file size
        file_size = int(s.recv(1024).decode().strip())
        if file_size > 0:
            # Receive the chunk data
            chunk_data = s.recv(file_size)
            return chunk_data
    return None

def split_store(file_name):
    with open(file_name, 'rb') as f:
        chunk_num = 0
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break

            # Prepare chunk name and data
            chunk_name = f"chunk_{chunk_num}"
            chunk_data = f"server{1 if chunk_num % 2 == 0 else 2}{chunk_num}".encode() + chunk + f"{chunk_num}{'revres1' if chunk_num % 2 == 0 else 'revres2'}".encode()

            # Alternate sending chunks to HTTPS and TCP server
            if chunk_num % 2 == 0:
                success = send_chunk_via_https(chunk_data, chunk_name)
                if not success:
                    print(f"Failed to send chunk {chunk_num} to HTTPS server.")
            else:
                success = send_chunk_via_tcp(chunk_data, chunk_name)
                if not success:
                    print(f"Failed to send chunk {chunk_num} to TCP server.")

            chunk_num += 1

def split_fetch(file_name):
    with open(file_name, 'wb') as f:
        chunk_num = 0

        while True:
            chunk_name = f"chunk_{chunk_num}"

            # Alternate fetching chunks from HTTPS and TCP server
            if chunk_num % 2 == 0:
                chunk_data = receive_chunk_via_https(chunk_name)
            else:
                chunk_data = receive_chunk_via_tcp(chunk_name)

            if not chunk_data:
                break

            # Strip the headers/footers from the chunk data
            chunk_start_marker = len(f"server{1 if chunk_num % 2 == 0 else 2}{chunk_num}".encode())
            chunk_end_marker = len(f"{chunk_num}{'revres1' if chunk_num % 2 == 0 else 'revres2'}".encode())
            actual_chunk = chunk_data[chunk_start_marker:-chunk_end_marker]

            # Write the actual chunk to the file
            f.write(actual_chunk)
            chunk_num += 1
