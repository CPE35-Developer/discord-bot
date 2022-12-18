#!/bin/bash
/home/ubuntu/adam/envs/discord/bin/python scripts/webhook_info_offline.py

sudo kill $(ps aux | grep python | grep main.py | awk '{print $2}') || echo 'nohup is not running'
