### IncentiveChain

> *A demo for testing a new bitcoin mechanism using docker swarm with clustered cloud instances.*

### Environment Setup
sudo apt-get update

sudo apt-get install git-all

sudo apt install software-properties-common

sudo add-apt-repository ppa:deadsnakes/ppa

sudo apt update

sudo apt install python3.8

sudo apt install python3-numpy

pip3 install --upgrade numpy

### Download the Source

sudo -i

git clone https://github.com/ksl20200108/IncentiveChain.git

cd IncentiveChain

git checkout dynamic_50

### Build Docker Images

> *Please change the start.sh file before building each image.*

docker build -t test1 .

docker build -t test2 .

docker build -t test .

### Pull Docker Images

> *Instead of building docker images locally, you can also pull from docker hub.*

docker pull shulinke/static_swarm1

docker pull shulinke/static_swarm2

docker pull shulinke/static_swarm

### Data Preparation

python3 data.py

python3 write_static_compose.py

python3 write_dynamic_compose.py

python3 write_main.py

### Automatic Experiment

chmod +x start_experiment.sh

nohup ./start_experiment.sh &

### Test Experiment

docker swarm init

docker network create --driver overlay --subnet 192.168.0.0/16 --gateway 192.168.0.1 --attachable test

docker stack deploy -c 11static.yaml test

docker stack deploy -c 11dynamic.yaml test

### Check the result

vim $i.txt, i\in [1, 8]

### Push Images

> *This is only for the author's reference*

```

docker tag <existing-image> <hub-user>/<repo-name>[:<tag>]

docker push <hub-user>/<repo-name>:<tag>

```
