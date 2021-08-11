from network import *
from random_functions import *


def each_test(mode, propose, user_num):
    if mode == "FTET" and propose == "SIM":
        fee1, fee2 = FTET_Sim(user_num), []
    elif mode == "FTET" and propose == "NSIM":
        fee1, fee2 = FTET_Nonsim(user_num)
    elif mode == "CURRENT" and propose == "SIM":
        fee1, fee2 = Current_Sim(user_num), []
    elif mode == "CURRENT" and propose == "NSIM":
        fee1, fee2 = Current_Nonsim(user_num)
    else:
        raise ValueError("Invalid mode or propose")
    net = Network(fee1, fee2, mode, propose, user_num)
    log.info("main function start server")
    t1 = threading.Thread(target=net.start_server_loop, args=(10,))  # only one argument -> not iterable -> add ","
    log.info("main function start client")
    t2 = threading.Thread(target=net.start_client_loop, args=(1, ['192.168.1.1', '192.168.1.2']))
    t1.start()
    t2.start()
    # t1.join()
    # t2.join()
    time.sleep(100)
    # for t in net.threads:
    #     del t
    # del net
    log.info("finally stopped")
    return
    # return None


def main():
    # for r in range(0, 1):
    #     for mode in ["FTET", "CURRENT"]:
    #         for propose in ["SIM", "NSIM"]:
    #             for user_num in [1600, 4800]:
    #                 start_time = time.time()
    #                 each_test(mode, propose, user_num)
    #                 time.sleep(180 - (time.time() - start_time))

    each_test("FTET", "SIM", 1600)
    # each_test("FTET", "SIM", 4800)
    # each_test("FTET", "NSIM", 1600)
    # each_test("FTET", "NSIM", 4800)
    # each_test("CURRENT", "SIM", 1600)
    # each_test("CURRENT", "SIM", 4800)
    # each_test("CURRENT", "NSIM", 1600)

    # start_time = time.time()
    # each_test("CURRENT", "NSIM", 4800)
    # log.info("Exited after " + str((time.time() - start_time) / 60))


main()
