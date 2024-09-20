
import os
import requests
import socket


CHUNK_SIZE = 1024
HTTPS_SERVER_URL = "http://127.0.0.1:5001" 
TCP_SERVER_IP = "'127.0.0.1'" 
TCP_SERVER_PORT = 65432  

def split_store(file):
    with open(file, 'rb') as f:
        chunk_num = 0
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
        
            if chunk_num % 2 == 0:  
                chunk = f"HTTPS{chunk_num}".encode() + chunk + f"{chunk_num}SPTTH".encode()
                upload_helper1_https(chunk, f"{file}_chunk_{chunk_num}")
            else: 
                chunk = f"TCP{chunk_num}".encode() + chunk + f"{chunk_num}PCT".encode()
                upload_helper2_tcp(chunk, f"{file}_chunk_{chunk_num}")
            
            chunk_num += 1

def split_fetch(file):
    chunk_num = 0
    with open(file, 'wb') as f:
        while True:
            try:
                if chunk_num % 2 == 0: 
                    chunk = fetch_https_helper3(f"{file}_chunk_{chunk_num}")
                else:  
                    chunk = fetch_tcp_helper4(f"{file}_chunk_{chunk_num}")

                if not chunk:
                    break
                cleaned_chunk = clean_chunk(chunk, chunk_num)
                f.write(cleaned_chunk)
                chunk_num += 1
            except Exception as e:
                print(f"Error fetching chunk {chunk_num}: {e}")
                break

def upload_helper1_https(chunk, chunk_filename):
    url = f"{HTTPS_SERVER_URL}/upload"
    files = {'file': (chunk_filename, chunk)}
    
    try:
        response = requests.post(url, files=files)
        response.raise_for_status()
        print(f"Chunk {chunk_filename} uploaded to HTTPS server.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to upload chunk {chunk_filename} to HTTPS server: {e}")

def upload_helper2_tcp(chunk, chunk_filename):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((TCP_SERVER_IP, TCP_SERVER_PORT))
            s.sendall("upload".encode().ljust(1024)) 
            s.sendall(chunk_filename.encode().ljust(1024))  
            s.sendall(str(len(chunk)).encode().ljust(1024))  
            s.sendall(chunk) 
            print(f"Chunk {chunk_filename} uploaded to TCP server.")
    except Exception as e:
        print(f"Failed to upload chunk {chunk_filename} to TCP server: {e}")

def fetch_https_helper3(chunk_filename):
    url = f"{HTTPS_SERVER_URL}/download/{chunk_filename}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Chunk {chunk_filename} fetched from HTTPS server.")
        return response.content
    except requests.exceptions.RequestException as err:
        print(f"Failed to fetch chunk {chunk_filename} from HTTPS server: {err}")
        return None

def fetch_tcp_helper4(chunk_filename):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((TCP_SERVER_IP, TCP_SERVER_PORT))
            s.sendall("download".encode().ljust(1024)) 
            s.sendall(chunk_filename.encode().ljust(1024))  

            file_size = int(s.recv(1024).decode().strip())  
            chunk_data = s.recv(file_size)  
            print(f"Chunk {chunk_filename} fetched from TCP server.")
            return chunk_data
    except Exception as err:
        print(f"Failed to fetch chunk {chunk_filename} from TCP server: {err}")
        return None

def clean_chunk(chunk, chunk_num):
    if chunk_num % 2 == 0:
        header = f"HTTPS{chunk_num}".encode()
        footer = f"{chunk_num}SPTTH".encode()
    else:  
        header = f"TCP{chunk_num}".encode()
        footer = f"{chunk_num}PCT".encode()
    
    return chunk[len(header):-len(footer)]
