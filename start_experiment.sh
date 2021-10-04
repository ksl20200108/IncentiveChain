#!/bin/bash
for (( i=1; i<=8; i++ ))
do
  for (( j=1; j<=10; j++ ))
  do
    docker-compose -f $i$jstatic.yaml up -d    # new
    docker stack    # new
    sleep 240
    docker logs experimenter &> $i$j.log &    # new
    docker kill $(docker ps -q)    # new
    sleep 40
    docker rm $(docker ps -a -q)    # new
    sleep 40
  done
done
