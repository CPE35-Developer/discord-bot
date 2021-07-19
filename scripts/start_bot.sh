#!/bin/bash

cd /deploy/discord-bot
pip install -r requirements.txt
nohup /home/ubuntu/adam/envs/discord/bin/python main.py > /dev/null 2> /dev/null < /dev/null &
