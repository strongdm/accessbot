#!/bin/bash

errbot &
pid[0]=$!
ssh -N -R 3141:localhost:3141 -i $LOG_EXPORT_CONTAINER_SSH_CREDENTIALS $LOG_EXPORT_CONTAINER_SSH_DESTINATION &
pid[1]=$!
trap "kill ${pid[0]} ${pid[1]}; exit 1" INT
wait
