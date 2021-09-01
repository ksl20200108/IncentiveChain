#!/bin/bash
for (( i=1; i<=8; i++ ))
do
  for (( j=1; j<=10; j++ ))
  do
    overnode up
    sleep 240
    docker logs experimenter &> $i$j.log &
    overnode up --remove-orphans
    sleep 20
    docker ps -a &> remain_c.txt &
    python3 write_overnode.py
  done
done
