#!/bin/bash
while true; do
    gunicorn app:app -b 0.0.0.0:4000 --log-file ecoapp2_logs.txt --log-level debug --capture-output
done
