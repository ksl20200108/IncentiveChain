from network import *
from random_functions import *


def main():
    net = Network(Current_Sim(1600), [], "CURRENT", "SIM")
    log.info("main function start server")
    t1 = threading.Thread(target=net.start_server_loop, args=(10,))    # only one argument -> not iterable -> add ","
    log.info("main function start client")
    t2 = threading.Thread(target=net.start_client_loop, args=(1, ['192.168.1.1', '192.168.1.2']))
    t1.start()
    t2.start()
    # net.start_server_loop(10)
    # net.start_client_loop(['192.168.1.1', '192.168.1.2'])


main()
