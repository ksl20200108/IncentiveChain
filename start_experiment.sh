#!/bin/bash
for (( i=1; i<=8; i++ ))
do
  # for (( j=1; j<=10; j++ ))
  # do
  docker-compose -f $i.yaml up -d
  sleep 260
  docker logs experimenter | tee $i.txt
  docker kill $(docker ps -q)
  sleep 10
  docker rm $(docker ps -a -q)
  sleep 5
  # done
done
exit
