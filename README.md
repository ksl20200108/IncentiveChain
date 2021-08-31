# IncentiveChain
A demo for IncentiveChain using overnode.

# Pre-Requisites

Install Docker, Docker-Compose, overnode

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

git checkout overnode_200

docker build -t two_miners_test:1.0 .

python3 data.py

python3 write_compose.py

python3 write_main.py

# Start experiment

chmod +x start_experiment.sh

nohup ./start_experiment.sh &

# Check the result

vim $i.txt, i\in [1, 8]
