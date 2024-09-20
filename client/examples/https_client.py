import requests

# The URL of the Flask server
url = 'http://localhost:5001/'
url_upload = url + 'upload'
url_download = url + 'download/'

def upload(file_name):
    # Path to the file that you want to upload
    
    # Prepare the file data
    files = {'file': open(local_path+file_name, 'rb')}

    # Send the file via POST request
    try:
        response = requests.post(url_upload, files=files)
        
        # Print the response from the server
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.json()}')
        
    except Exception as e:
        print(f'An error occurred: {e}')

def download(file_name):

    try:
        # Send a GET request to retrieve the file (streaming the response)
        response = requests.get(url_download+file_name, stream=True)

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
# upload(file_name)
# download(file_name)