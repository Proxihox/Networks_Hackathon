# Library file for both the functions
from h import upload, download
from t import upload_file, download_file
import os
import sys

addr = './client/mem/'

def split_store(file_name) :
    # Split store code
    i = 0
    with open(addr + file_name, "rb") as f:
	    while (bytes := f.read(1024)):
                  print(bytes)
                  words = file_name.split('.')     
                  f_name = words[0] + str(i) + '.' + words[1]
                  with open(addr + f_name, "wb") as binary_file:
                       binary_file.write(bytes)
                       binary_file.flush()  # Ensure the data is written to disk
                       os.fsync(binary_file.fileno())  # Force the write to disk
                       if (i % 2 == 0):
                            upload(f_name)
                       else:
                            upload_file(f_name)
                  i = i + 1
    pass

import os

def split_fetch(file_name):
    # Define the path for the actual file
    actual_file = addr + file_name

    # Remove the existing file if it exists
    if os.path.exists(actual_file):
        os.remove(actual_file)
        print(f'Removed existing file: {actual_file}')  # Debugging line

    # Open the actual file in append mode
    with open(actual_file, "ab") as f:  # Use "ab" for appending
        i = 0
        while True:
            words = file_name.split('.')
            f_name = words[0] + str(i) + '.' + words[1]
            
            # Check if the split file exists
            if os.path.exists(addr + f_name):  # Ensure to check the correct path
                if (i % 2 == 0):
                    download(f_name)
                else:
                    download_file(f_name)
                
                # Open the split file to read and append its contents
                with open(addr + f_name, "rb") as binary_file:
                    f.write(binary_file.read())  # Append the content
                
                print(f'Appended contents of {f_name} to {actual_file}')  # Debugging line
            else:
                print(f'{f_name} does not exist. Stopping fetch.')  # Debugging line
                break  # Break the loop if the file doesn't exist
            i += 1

