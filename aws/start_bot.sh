#!/bin/bash
source activate discord
cd ~/deploy/discord-bot
pip install -r requirements.txt
forever start -c python main.py