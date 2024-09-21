#!/usr/bin/env bash

# Start tmux session
tmux new-session -d -s mysession

# Run first server in the first pane
tmux send-keys "python3 ./https_server/server.py" C-m

# Split the window and run the second server in the new pane
tmux split-window -h
tmux send-keys "python3 ./tcp_server/server.py" C-m

# Attach to the tmux session to see both running
tmux attach -t mysession
