## IncentiveChain

> *A demo for testing a new bitcoin mechanism using docker swarm with clustered cloud instances.*

### Environment Setup

> *For new cloud instances with Ubuntu system, you need to install some pre-requisite packages.*

```
sudo apt-get update
sudo apt-get install git-all
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.8
sudo apt install python3-numpy
pip3 install --upgrade numpy

```

### Download the Source

> *Download the source code from GitHub for further manipulation.*

```
sudo -i
git clone https://github.com/ksl20200108/IncentiveChain.git
cd IncentiveChain
git checkout dynamic_10000

```

### Build Docker Images

> *Please change the start.sh file before building each image.*

```
docker build -t test1 .
docker build -t test2 .
docker build -t test .

```

### Pull Docker Images

> *Instead of building docker images locally, you can also pull from docker hub.*

```
docker pull shulinke/static_swarm1
docker pull shulinke/static_swarm2
docker pull shulinke/static_swarm

```

### Data Preparation

> *The data is generated from random processes, which means the data is unique for each experiment.*
> *<span style="color:red">The random seed should be generated each time before doing the experiment by the user.</span>* 
> *The random seed is 32 bit unsigned integers ([0 to 4294967295]).*
> *Before running commands below, modify line 29 in data.py: change the 0 with your generated random seed.*

```
python3 data.py
python3 write_static_compose.py
python3 write_dynamic_compose.py
python3 write_main.py

```

### Initializing Docker Swarm

> *Initializing the docker swarm before both automatical and testing experiment. After using docker swarm init, let other cloud instances join the swarm cluster. Should you have any question, please refer to docker swarm document.*

```
docker swarm init

```

### Automatic Experiment

> *The experiment could be tedious. Here is the automatical experiment implementing with bash scripts. Note that the sleeping time in bash script should be modified with respect to the number of containers.*

```
chmod +x start_experiment.sh

```
```
nohup ./start_experiment.sh &

```

### Test Experiment

> *This is for author's debugging when developing the system.*

```
docker network create --driver overlay --subnet 192.168.0.0/16 --gateway 192.168.0.1 --attachable test
docker stack deploy -c 11static.yaml test
docker stack deploy -c 11dynamic.yaml test

```

or

```
chmod +x test_experiment.sh

```
```
nohup ./test_experiment.sh &

```

### Check the result

> *When debugging, use this command to check the result.*

```
vim $i.txt, i\in [1, 8]

```

### Push Images

> *This is only for the author's reference*

```
docker tag <existing-image> <hub-user>/<repo-name>[:<tag>]
docker push <hub-user>/<repo-name>:<tag>

```

### Further Info

> *Should you have any question, please contact Shulin Ke at <shulinke@link.cuhk.edu.cn>.*

### About the Author

> *My name is Shulin Ke, an undergraduate from The Chinese University of Hong Kong, Shenzhen (CUHKSZ) major in Data Science and Big Data Technology.*

