# Networks_Hackathon

## Servers
 You have access to 2 servers, one which communicates using HTTPS and other using TCP. To simulate these servers, there are 2 folders, namely server_https and server_tcp. These 2 servers store all files they get inside a folder called server_files

## How to interact with the servers
To run the server, go to the server directory and run the command python3 <server_name>.py</br>
Do note that you run both the servers in **separate** terminals!! As both server need to be up and running at the same time.</br>

Clone this repository to your local computer using
```git
git clone git@github.com:Proxihox/Networks_Hackathon.git
```
Open your terminal and navigate to the local copy of this repository</br>

Then go to the directory of server communicating via HTTPS using 
```sh
cd server_https
```
Then type the command below to run the server
```py
python3 server.py
```

In a **separate** terminal tab, navigate to the local copy of this repository</br>

Then go to the durectory of server communicating via TCP using
```sh
cd server_tcp
```
Then type the command below to run the server
```py
python3 server.py
```

To run the code you've written, do the same. Navigate to the directory of your code in a **separate** terminal and use the command</br>
```py
python3 your_file_name.py
```

***Note*** : You can write your code in multiple files but you have to encapsulate all the features into a single runnable file as a library!!

## Problem Statement
FIle Sharing is very common over the internet, be it uploading some important document over cloud storage or downloading your favourite games!!</br>
As long as the data is small in size, it is not a very big problem to send the file as a whole. But when file sizes are large, it is very difficult to send the file all at once.</br>
To counter this problem, data is usually sent into smaller blocks called chunks, independently of each other.


Write a library which implements split_store(file) and split_fetch(file). Also write an example code which uses these 2 functions to store and fetch the file 

### split_store(file)
This function takes a file in your local device, splits this file into chunks of 1024 bytes and sends these chunks to server.</br>
We send every alternate chunk to the same server, for example say a file is split into 4 chunks.
* Chunk-1 is sent to the server communicating via HTTPS
* Chunk-2 is sent to the server communicating via TCP
* Chunk-3 is sent to the server communicating via HTTPS
* Chunk-4 is sent to the server communicating via TCP

Once the chunks of data are uploaded, they will be stored in the server, at ../server_files

**Note that the files are split between two servers, one communicating via HTTPS and other via TCP**

### split_fetch(file)
This function makes a request to each of the servers. The server sends chunks of data to the client.

You are expected to appropriately handle these chunks of data and patch them to get your originally uploaded file back.

### Open ended problem
* Try to implement security features to make the file sharing secure
* Try to use a other efficient data management algorithims to store large data
* Try to have a check for malicious files
