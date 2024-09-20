# Library file for both the functions
import threading
import requests
import socket
import os
import io
import math


def split_store(file_name) :
    ## the server url, host for the tcp connection , http connection
    url = 'http://127.0.0.1:5000/upload'
    host = '127.0.0.1'
    port = 65432


    # Split store code
    

    file_size = os.stat(file_name).st_size #computing filesize

    chunks = math.ceil(file_size/1024) #computing the number of chunks

    ##sending the first file (containing metadata)(number of chunks) and the size of the file
    #filename = "f_"
    filename = file_name.split('/')[-1]
    fileN = f"{filename}_"
    file_content = f"{chunks} {file_size}"
    
    with open(fileN, "wb") as chunkfile:
        chunkfile.write(file_content.encode())
    
    files = {'file': open(fileN, 'rb')}
    response = requests.post(url, files=files)
    os.remove(fileN)
    
    ## send the chunks 
    
    fileR = open(file_name, "rb")
    
    
    def sendToTcp(chunk_num, bytes):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        sock.connect((host, port))
        sock.send("upload".encode().ljust(1024))
        fileN = filename + str(chunk_num)
        sock.send(fileN.encode().ljust(1024))
        sock.send("1024".encode().ljust(1024))
        sock.send(bytes.ljust(1024))
        sock.close()
    
    def sendToHttp(chunk_num, bytes):
        fileN = f"{filename}{chunk_num}"
        
        files = {'file': (fileN, bytes)}
        response = requests.post(url, files=files)


    if chunks == 1:
        sendToTcp(0, fileR.read(1024))

    if chunks % 2 == 0: # i have an even number of chunks
        for chunk_num in range(0, chunks,2):
            bytes = fileR.read(1024)
            t1 = threading.Thread(target=sendToTcp, args=(chunk_num, bytes))
            t1.start()
            bytes = fileR.read(1024)
            t2 = threading.Thread(target=sendToHttp, args=(chunk_num+1, bytes))
            t2.start()
            t1.join()
            t2.join()
    else:
        for chunk_num in range(0, chunks-1,2):
            bytes = fileR.read(1024)
            t1 = threading.Thread(target=sendToTcp, args=(chunk_num, bytes))
            t1.start()
            bytes = fileR.read(1024)
            t2 = threading.Thread(target=sendToHttp, args=(chunk_num+1, bytes))
            t2.start()
            t1.join()
            t2.join()
        sendToTcp(chunks-1, fileR.read(1024)) 
    

            

            



    


def split_fetch(file_name) :
    #step 1 get the _ file
    host = '127.0.0.1'
    port = 65432
    
    file_name = file_name.split("/")[-1] # get only the file name
    #file_name = "./client/mem/" + file_name
    #construct the url
    url = 'http://127.0.0.1:5000/download/' + file_name+ "_"
    response = requests.get(url)
    chunks = response.content.split()[0]
    size = response.content.split()[1]
    

    fileW = open("./client/mem/"+file_name, "wb")
    
    for i in range(int(chunks)):
        if i % 2 == 0: #get it from the tcp server 
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            sock.connect((host, port))
            sock.send("download".encode().ljust(1024))
            fileN = f"{file_name}{i}"
            sock.send(fileN.encode().ljust(1024))
            filesize = sock.recv(1024).strip()
            data = sock.recv(int(filesize))
            
            fileW.write(data)
            sock.close()
        else:#get from http server (pain) 
            fileN = f"{file_name}{i}"
            url = 'http://127.0.0.1:5000/download/' + fileN 
            response = requests.get(url)
            data = response.content
            
            fileW.write(data)
    

    fileW.close()
    