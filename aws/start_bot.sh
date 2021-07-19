#!/bin/bash
aws s3 cp s3://cpe35-discord-bot/.env  ~/.env
sudo mv ~/.env /deploy/discord-bot
cd /deploy/discord-bot
pip install -r requirements.txt
forever start -c ~/adam/envs/discord/bin/python main.py 
