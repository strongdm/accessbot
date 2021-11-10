#!/bin/sh

ngrok authtoken $NGROK_TOKEN
ngrok http -log=stdout 80 &
