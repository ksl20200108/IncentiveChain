#!/bin/bash
script $results.txt
for (( i=1; i<=8; i++ ))
do
  # for (( j=1; j<=10; j++ ))
  # do
  docker-compose -f $i.yaml up -d
  sleep 260
  # script $i$j.txt
  docker logs experimenter
  # exit
  docker kill ${docker ps -a -q}
  sleep 10
  docker rm ${docker ps -a -q}
  sleep 10
  # done
done
exit
