#!/bin/bash

ngrok authtoken $NGROK_AUTHTOKEN &
python -u app.py
