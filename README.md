# Networks_Hackathon

## Servers
 You have access to 2 servers, one which communicates using https and other using tcp. To simulate these servers, there are 2 folders, namely server_https and server_tcp. These 2 servers store all files they get inside a folder called _____

## How to interact with the servers




## Problem Statement
FIle Sharing is very common over the internet, be it uploading some important document over cloud storage or downloading your favourite games!!\
As long as the data is small in size, it is not a very big problem to send the file as a whole. But when file sizes are large, it is very difficult to send the file all at once.
To counter this problem, data is usually sent into smaller blocks called chunks, independently of each other.


Write a library which has implements split_store(file) and split_fetch(file). Also write an example code which uses these 2 functions to store and fetch the file ________

### split_store(file)
This function takes a file in your local device, splits this file into chunks of 1024 bytes and sends these chunks to server.
We send every alternate chunk to the same server, for example say a file is split into 4 chunks.
* Chunk-1 is sent to the server communicating via https
* Chunk-2 is sent to the server communicating via tcp
* Chunk-3 is sent to the server communicating via https
* Chunk-4 is sent to the server communicating via tcp

Once the chunks of data are uploaded, they will be stored in the server, at ../server_files

**Note that the files are split between two servers, one communicating via https and other via tcp**

### split_fetch(file)
This function makes a request to each of the servers. The server sends chunks of data to the client.

You are expected to appropriately handle these chunks of data and patch them to get your originally uploaded file back.

### Open ended problem
* Try to implement security features to make the file sharing secure
* Try to use a other efficient data management algorithims to store large data
* Try to have a check for malicious files
