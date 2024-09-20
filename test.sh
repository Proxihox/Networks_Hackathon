#!/bin/bash

PYTHON_SCRIPT_1="https_server/server.py"
PYTHON_SCRIPT_2="tcp_server/server.py"
PYTHON_SCRIPT_3="solution.py"

echo "............................. Running https_server/server.py ......................."
python3 "$PYTHON_SCRIPT_1" &

sleep 2 
echo "............................. Running tcp_server/server.py ........................."
python3 "$PYTHON_SCRIPT_2" &

sleep 2
echo "............................. Running solution.py ..........................................."
python3 "$PYTHON_SCRIPT_3"

cleanup() {
    echo "Cleanup started."
    kill -9 $(lsof -t -i :5000)
    kill -9 $(lsof -t -i :65432)
    echo "Cleanup completed."
}

trap cleanup EXIT
wait
