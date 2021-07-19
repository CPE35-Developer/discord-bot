#!/bin/bash

sudo kill $(ps aux | grep python | grep main.py | awk '{print $2}') || echo 'nohup is not running'
