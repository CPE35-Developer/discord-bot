#!/bin/bash
source activate discord
cd discord-bot
forever start -c python main.py