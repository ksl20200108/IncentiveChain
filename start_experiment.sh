#!/bin/bash

for (( i=1; i<=8; i++ ))
do
  # for (( j=1; j<=10; j++ ))
  # do
  docker-compose -f $i.yaml up -d
  sleep 140
  # script $i$j.txt
  script $i.txt
  docker logs experimenter
  exit
  docker stop ${docker ps -a -q}
  docker rm ${docker ps -a -q}
  sleep 20
  # done
done
