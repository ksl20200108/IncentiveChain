{\rtf1\ansi\ansicpg936\cocoartf2580
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fmodern\fcharset0 CourierNewPSMT;}
{\colortbl;\red255\green255\blue255;\red52\green52\blue52;\red255\green255\blue255;}
{\*\expandedcolortbl;;\cssrgb\c26667\c26667\c26667;\cssrgb\c100000\c100000\c100000;}
\paperw11900\paperh16840\margl1440\margr1440\vieww12500\viewh15300\viewkind1
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs29\fsmilli14667 \cf2 \cb3 \expnd0\expndtw0\kerning0
#!/bin/bash\
\
for (( i=1; i<=8; i++ ))\
do\
  for (( j=1; j<=10; j++ ))
	docker-compose -f $i.yaml up -d\
	sleep 1440\
	script $i$j.txt\
	docker logs experimenter\
	exit\
	docker stop $\{docker ps -a -q\}\
	docker rm $\{docker ps -a -q\}\
	sleep 30\
done\
}
