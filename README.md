# IncentiveChain
A demo for

# Experiment preparation
sudo apt-get update

sudo apt-get install git-all

sudo apt install software-properties-common

sudo add-apt-repository ppa:deadsnakes/ppa

sudo apt update

sudo apt install python3.8

sudo -i

git clone https://github.com/ksl20200108/IncentiveChain.git

cd IncentiveChain

git checkout 50_miners_test

sudo apt install python3-numpy

pip3 install --upgrade numpy

python3 data.py

docker build -t two_miners_test:1.0 .

# Start experiment
docker-compose -f emm.yaml up -d

# Check the result
docker logs -f experimenter

# After experimenter logging result
docker stop $(docker ps -q)

# Experiment stop
docker rm $(docker ps -a -q)
