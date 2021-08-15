#!/bin/bash
sudo aws s3 cp s3://cpe35-discord-bot/.env /deploy/discord-bot/.env
sudo aws s3 cp s3://cpe35-discord-bot/gcp_client.json /deploy/discord-bot/gcp_client.json
cd /deploy/discord-bot
pip install -r requirements.txt
sudo nohup /home/ubuntu/adam/envs/discord/bin/python main.py >/dev/null 2>&1 &
