#!/bin/bash
for (( i=1; i<=8; i++ ))
do
  for (( j=1; j<=10; j++ ))
  do
    docker-compose -f $i$j.yaml up -d
    sleep 240    # please leave enough time + 20 for creating containers
    docker logs experimenter &> $i$j.log &
    docker kill $(docker ps -q)
    sleep 40
    docker rm $(docker ps -a -q)
    sleep 40
  done
done
