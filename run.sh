#!/bin/bash

while :; do
    python main.py
    echo "$(date) Sleep 30 seconds. ctrl-c to exit."
    sleep 30
done
