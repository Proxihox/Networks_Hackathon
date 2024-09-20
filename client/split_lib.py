import requests
import socket
import os

# Server configuration
HOST = '127.0.0.1'  # Server IP
PORT = 65432        # Server port

# Library file for both the functions
url = 'http://localhost:5000/'
url_upload = url + 'upload'
url_download = url + 'download/'
file_dir = './mem'

i=1

def split_store(file_name) :
    # Path to the file that you want to upload
    
    # Prepare the file data
    files = {'file': open(local_path+file_name, 'rb')} # client/mem/test.txt

    # Send the file via POST request
    try:
        if i==1:
            response = requests.post(url_upload, files=files) # http://localhost:5000/upload
            
            # Print the response from the server
            print(f'Status Code: {response.status_code}')
            print(f'Response: {response.json()}')
        else:
            file_path = file_dir+f'/{file_name}'
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
        i=1-i
    except Exception as e:
        print(f'An error occurred: {e}')

def split_fetch(file_name) :
    try:
        # Send a GET request to retrieve the file (streaming the response)
        response = requests.get(url_download+file_name, stream=True) # http://localhost:5000/download/test.txt

        # Check if the request was successful
        if response.status_code == 200:
            # Open the file in write-binary mode to save the downloaded content
            with open(local_path+file_name, 'wb') as file:
                # Write the response content to the file in chunks
                for chunk in response.iter_content(chunk_size=1024):  # 1KB chunks
                    if chunk:  # Filter out keep-alive chunks
                        file.write(chunk)
            print(f'File downloaded successfully and saved to {local_path+file_name}')
        else:
            print(f'Failed to download file. Status code: {response.status_code}')

    except Exception as e:
        print(f'An error occurred: {e}')

server_path = './https_server/mem/'
local_path = './client/mem/'
file_name = 'test.txt' 