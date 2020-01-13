#!/bin/bash
while true; do
    cd /home/mayabasu/EcoApp_2 && /usr/local/bin/gunicorn app:app -b 0.0.0.0:4000 --log-file ecoapp2_logs.txt --log-level debug --capture-output > /home/mayabasu/log1.txt 2>&1
    sleep 5
done
