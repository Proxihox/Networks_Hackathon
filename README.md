# Solution

## split_store

- computes the size and the number of chunks
- stores a file `filename_` in the http server, containing the number of chunks
and the size of the file

- consecutively store `filename_i` where i is 0 indexed index of the chunk, stores
in tcp if i is even and http if i is odd.

## split_fetch

- First fetches the metadata file from the http server, 
- Follows the same algorithtm while taking even chunks from tcp and odd from http


## Improvements made

- Added threading so that sends to http server, tcp server parallelly
- Was creating temporary files in disk for sending to http server, removed this to reduce disk i/o (increase performance)

## Scope for improvement

- Add encryption to both servers