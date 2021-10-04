# IncentiveChain
A demo for

# Experiment preparation
sudo apt-get update

sudo apt-get install git-all

sudo apt install software-properties-common

sudo add-apt-repository ppa:deadsnakes/ppa

sudo apt update

sudo apt install python3.8

sudo apt install python3-numpy

pip3 install --upgrade numpy

sudo -i

git clone https://github.com/ksl20200108/IncentiveChain.git

cd IncentiveChain

git checkout static_swarm_50

docker build -t two_miners_test:1.0 .

python3 data.py

python3 write_compose.py

python3 write_main.py

# Automatical Experiment

chmod +x start_experiment.sh

nohup ./start_experiment.sh &

# Test Experiment

docker network create --driver overlay --subnet 192.168.0.0/16 --gateway 192.168.0.1 --attachable test

docker stack deploy -c 11.yaml static-ip

# Check the result

vim $i.txt, i\in [1, 8]
