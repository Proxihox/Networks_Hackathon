# Networks_Hackathon
## Modifications Made for Part 2

- Added multithreading for both servers
- Added authorization for Flask server and authentication for TCP server

## Additional Modifications Possible (Not Implemented)

- Can encrypt the payload for the TCP server (or just the wrap the server with a SSL layer)
- Limit the file size while using the TCP server (Currently, user can put in a very large file)
- Add rate limiting to the servers (to prevent DDOS)