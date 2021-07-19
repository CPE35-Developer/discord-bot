#!/bin/bash

forever stop 0 || echo "forever stop failed"
cd /deploy/discord-bot
sudo rm -r discord-bot/
cd