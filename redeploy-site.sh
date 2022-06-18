#!/bin/bash

tmux kill-session

cd project-gentle-otters

git fetch && git reset origin/main --hard

source python3-virtualenv/bin/activate

pip install -r requirements.txt

tmux new-session -d -s my_session 'flask run --host=0.0.0.0' 