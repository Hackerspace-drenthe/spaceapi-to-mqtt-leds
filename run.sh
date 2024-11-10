#!/bin/bash

while :
do
    ./venv/bin/python main.py
    echo "`date` Sleep 30 seconds. ctrl-c to exit."
    sleep 30
done
