import os
import pickle
from network import *
from random_functions import *


def each_test(number, mode, propose, user_num):
    type = mode + propose
    if (type != "FTETSIM") and (type != "FTETNSIM") and \
            (type != "CURRENTSIM") and (type != "CURRENTNSIM"):
        raise ValueError("Invalid mode or propose")

    path = './data'
    fee1 = np.load(os.path.join(path, str(number) + type + "fee1" + str(user_num) + ".npy"))
    fee2 = np.load(os.path.join(path, str(number) + type + "fee2" + str(user_num) + ".npy"))
    fee1 = fee1.tolist()
    fee2 = fee2.tolist()

    path = './peers'
    fp = open(os.path.join(path, "peers.txt"), "rb")
    peers = pickle.load(fp)

    net = Network(fee1, fee2, mode, propose, user_num)
    log.info("main function start server")
    t1 = threading.Thread(target=net.start_server_loop, args=(10,))  # only one argument -> not iterable -> add ","
    log.info("main function start client")
    t2 = threading.Thread(target=net.start_client_loop, args=(1, peers))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    log.info("finally stopped")


def main():

    # each_test(1, "FTET", "SIM", 1600)
    # each_test(1, "FTET", "SIM", 4800)
    # each_test(1, "FTET", "NSIM", 1600)
    # each_test(1, "FTET", "NSIM", 4800)
    each_test(1, "CURRENT", "SIM", 1600)
    # each_test(1, "CURRENT", "SIM", 4800)
    # each_test(1, "CURRENT", "NSIM", 1600)
    # each_test("CURRENT", "NSIM", 4800)


main()
