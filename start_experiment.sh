#!/bin/bash
for (( i=1; i<=8; i++ ))
do
  for (( j=1; j<=10; j++ ))
  do
    docker-compose -f $i.yaml up -d
    sleep 200    # please leave enough time + 20 for creating containers
    docker logs experimenter &> $i$j.log &
    docker kill $(docker ps -q)
    sleep 20
    docker rm $(docker ps -a -q)
    sleep 20
  done
done
