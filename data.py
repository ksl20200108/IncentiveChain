import os
import pickle
from random_functions import *


def create_data():
    path = './data'
    for i in range(1, 11):
        for user_num in [1600, 4800]:
            fee1, fee2 = FTET_Sim(user_num), np.array([])
            np.save(os.path.join(path, str(i) + "FTETSIM" + "fee1" + str(user_num) + ".npy"), fee1)
            np.save(os.path.join(path, str(i) + "FTETSIM" + "fee2" + str(user_num) + ".npy"), fee2)

            fee1, fee2 = FTET_Nonsim(user_num)
            np.save(os.path.join(path, str(i) + "FTETNSIM" + "fee1" + str(user_num) + ".npy"), fee1)
            np.save(os.path.join(path, str(i) + "FTETNSIM" + "fee2" + str(user_num) + ".npy"), fee2)

            fee1, fee2 = Current_Sim(user_num), np.array([])
            np.save(os.path.join(path, str(i) + "CURRENTSIM" + "fee1" + str(user_num) + ".npy"), fee1)
            np.save(os.path.join(path, str(i) + "CURRENTSIM" + "fee2" + str(user_num) + ".npy"), fee2)

            fee1, fee2 = Current_Nonsim(user_num)
            np.save(os.path.join(path, str(i) + "CURRENTNSIM" + "fee1" + str(user_num) + ".npy"), fee1)
            np.save(os.path.join(path, str(i) + "CURRENTNSIM" + "fee2" + str(user_num) + ".npy"), fee2)


create_data()
path = './data'
number = 1
user_num = 1600
type = "FTETSIM"
fee1 = np.load(os.path.join(path, str(number) + type + "fee1" + str(user_num) + ".npy"))
fee2 = np.load(os.path.join(path, str(number) + type + "fee2" + str(user_num) + ".npy"))
print(fee1.tolist())
print(fee2.tolist())


"""
old
"""

# def create_peers(round):
#     path = './peers'
#     peers = []
#     for i in range(1, round + 1):
#         peers.append('192.168.1.' + str(i))
#     fp = open(os.path.join(path, "peers.txt"), "wb")
#     pickle.dump(peers, fp)

# create_peers(50)
# path = './peers'
# fp = open(os.path.join(path, "peers.txt"), "rb")
# peers = pickle.load(fp)
# print(peers)
