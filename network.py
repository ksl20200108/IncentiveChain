"""
tbc: to be continued
    Add a call to Experimenter.save_result() at the end of 10 experiments (send ending message from miners)
tbt: to be tested
tbd: to be deleted
tbm: to be modified
tba: to be added
    Three and four nodes test (two miners and one experimenter, three miners and one experimenter)
    10 nodes test
    20 nodes test
    50 nodes test
    100 nodes test
"""


import socket
import threading
import time    # for sleeping between network communication
import os    # to get the container's predefined ip address
import random    # to select random peers from peers list
import json    # to transform data into json string
import struct    # for adding prefix indicating message length
from blockchain_structures import *


"""
Message Types:
1. LEN_REQ: request for length
2. BC_REQ: request for blockchain
3. LEN_MSG: data for length request
4. BC_MSG: data for blockchain request
5. RST_MSG: experiment result report message
6. END_MSG: ending the whole experiment
"""
LEN_REQ = 1
BC_REQ = 2
LEN_MSG = 3
BC_MSG = 4
RST_MSG = 5
END_MSG = 6


class Network:

    """
    Miner's network
    """

    def __init__(self, fees1, fees2, mode, propose, user_num):
        """
        :param fees1: transactions in simultaneous proposing and early half transactions in non-simultaneous proposing
        :param fees2: late half transactions in non-simultaneous proposing
        :param mode: "FTET" mechanism or current blockchain  mechanism
        :param propose: simultaneous proposing or non-simultaneous proposing
        self.bc: the local blockchain
        self.server_sock: socket object for server side
        """
        log.info("The current Mode and Propose are % s and %s" % (mode, propose))
        self.bc = Blockchain(fees1, fees2, mode, propose)
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # let not call addr already in use
        # self.clients = random_chosen(bootstrap)
        self.bc_lock = threading.Lock()
        self.stop_lock = threading.Lock()
        self.experimenter_host = '192.168.1.0'
        self.first_start = True
        self.client_stop = False
        self.user_num = user_num
        log.info("Initializing Success")

    """
    Server side
    """

    def start_server_loop(self, max_conn):
        """
        :param max_conn: maximum number of connection to this server
        self.HOST: ipv4 address of local host
        self.PORT: all the peers communicate between each other through this port, predefined in compose yml as 5678
        """
        log.info("start server loop")
        env_dist = os.environ
        host = env_dist.get('LOCAL_IP')  # get the environment variable: LOCAL_IP
        port = 5678
        self.server_sock.bind((host, port))
        self.server_sock.listen(max_conn)
        """
        1st thread in Network: Server thread
        """
        t = threading.Thread(target=self.server_main_loop, args=())
        t.start()
        t.join()
        log.info("start server loop stop")

    def server_main_loop(self):
        log.info("server main loop")
        while True:
            self.stop_lock.acquire()
            if not self.client_stop:
                conn, addr = self.server_sock.accept()
                t = threading.Thread(target=self.server_handler, args=(conn, addr))
                t.start()
                self.stop_lock.release()
                time.sleep(1)
            else:
                self.stop_lock.release()
                break
        self.server_sock.close()
        log.info("server main loop stop")

    def server_handler(self, conn, addr):    # max_recv can be 61995
        """
        :param conn:
        :param addr:
        data: blockchain length from client side
        """
        log.info("server handler")
        data = self.recv_msg(conn)
        data = json.loads(data.decode())
        log.info("server receive message: " + str(data))
        if data["type_"] == 1:
            self.handle_request_len(conn)
        elif data["type_"] == 2:
            self.handle_request_chain(conn)
        else:
            raise ValueError("Server side: the message type is not legal")

    def handle_request_len(self, conn):
        log.info("server handle request len")
        self.bc_lock.acquire()
        sender = json.dumps({"type_": LEN_MSG, "data": len(self.bc.blocks)}).encode()
        self.bc_lock.release()
        # log.info("server handle request len try to send: " + str(sender))
        self.send_msg(conn, sender)
        log.info("server handle request len stop")

    def handle_request_chain(self, conn):
        log.info("server handle request chain")
        self.bc_lock.acquire()
        sender = json.dumps({"type_": BC_MSG, "data": self.bc.serialize()}).encode()
        self.bc_lock.release()
        # log.info("server handle request chain try to send: " + str(sender))
        self.send_msg(conn, sender)
        log.info("server handle request chain stop")

    """
    Client side
    """

    def start_client_loop(self, peers):
        log.info("start client loop")
        t = threading.Thread(target=self.client_main_loop, args=(peers,))
        t.start()
        t.join()
        log.info("start client loop stop")

    def client_main_loop(self, peers):
        log.info("client main loop")
        if self.bc.MODE == "FTET":
            set_round = 13
        else:
            set_round = 24
        peers.remove(os.environ.get('LOCAL_IP'))
        peers = random.choices(peers, k=int(len(peers) / 3))
        r = 1
        while r <= set_round:    # if it's not while the blocks will increase out of limit
            """
            In one experiment, stop loop after mining defined number of blocks
            """
            # mining
            self.bc.add_block_by_mining(self.bc_lock)
            time.sleep(10)    # sleep for 1 minutes
            log.info("Mined " + str(r) + " block(s)")
            # start connections thread -> require server's chain length
            threads = [None] * len(peers)
            self.results = [None] * len(peers)
            self.results_hosts = {}
            # select peers randomly
            # env_dist = os.environ
            # host = env_dist.get('LOCAL_IP')  # get the environment variable: LOCAL_IP
            # peers = random.sample()
            # recv results
            for i in range(0, len(peers)):
                threads[i] = threading.Thread(target=self.acquire_peers_info, args=(i, peers[i]))
                threads[i].start()
            # stop connections
            for i in range(0, len(peers)):
                threads[i].join()
                threads[i] = None    # de-reference the thread
            log.info("client send len request")
            self.first_start = False
            # compare with the longest (save ipv4 address)
            max_length = max(self.results)
            self.bc_lock.acquire()
            if max_length > len(self.bc.blocks):
                # shorter: start client connection -> request chain info for the optimal address
                log.info("client request chain length " + str(max_length)
                         + " and local length " + str(self.bc.blocks[-1].index))
                data = self.acquire_peer_chain(self.results_hosts[max_length])
                # log.info("client receive chain: " + str(data))
                self.results_hosts = None    # de-reference the hosts dictionary
                self.bc = Blockchain.deserialize(data)    # update local chain
                log.info("client update local chain")

            r = self.bc.blocks[-1].index + 1
            self.bc_lock.release()
            # -> start mining again

        # calculate the social welfare
        self.bc.update_total_welfare()
        # send the information to the Experimenter
        if self.experimenter_host:
            log.info("there is experimenter")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((self.experimenter_host, 5678))
                sender = json.dumps({
                    "type_": RST_MSG,
                    "mode": self.bc.MODE, "propose": self.bc.PROPOSE,
                    "welfare": self.bc.current_social_welfare,
                    "user_num": self.user_num,
                    "remain_txs": len(self.bc.transaction_pool1)
                }).encode()
                self.send_msg(s, sender, True)    # close the connection after reporting
            except:
                log.info("The experimenter has been closed")
        else:
            log.info("there is no experimenter")
        log.info("The node " + os.environ.get('LOCAL_IP') + "'s social welfare is " + str(self.bc.current_social_welfare))
        log.info("In " + self.bc.MODE + " " + self.bc.PROPOSE + " " + str(self.user_num) + " users")
        self.stop_lock.acquire()
        self.client_stop = True
        self.stop_lock.release()
        # exit()
        log.info("client main loop stop")
        log.info("with blocks")
        log.info(str([str(i.show()) for i in self.bc.blocks]))

    def acquire_peers_info(self, index, host, port=5678):
        """
        :param host: randomly chosen host
        :param port: pre-defined port 5678. All servers communicate on this port
        :return:
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        log.info("Trying connect")
        if self.first_start:    # in case that the target peer is not started yet
            while True:
                try:
                    s.connect((host, port))
                    break
                except:
                    time.sleep(1)   # sleep for a while, wait the target peer
        else:
            s.connect((host, port))    # must add this otherwise it will not connect again when it is not first_start
        log.info("Successfully connected")
        # require server's chain length
        sender = json.dumps({"type_": LEN_REQ, "data": None}).encode()
        self.send_msg(s, sender)
        receiver = self.recv_msg(s)
        receiver = json.loads(receiver.decode())
        if receiver["type_"] != LEN_MSG:
            raise ValueError("Client side: did not receive length message for length request")
        self.results[index] = receiver["data"]
        self.results_hosts[receiver["data"]] = host
        s.close()
        log.info("acquire peers info stop")

    def acquire_peer_chain(self, host, port=5678):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        # require server's chain
        sender = json.dumps({"type_": BC_REQ, "data": None}).encode()
        self.send_msg(s, sender)
        receiver = self.recv_msg(s)
        s.close()
        receiver = json.loads(receiver.decode())
        if receiver["type_"] != BC_MSG:
            raise ValueError("Client side: did not receive length message for length request")
        return receiver["data"]

    """
    Methods from the internet
    https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
    """

    def send_msg(self, sock, msg, close=False):
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        sock.sendall(msg)
        if close:
            sock.close()

    def recv_msg(self, sock):
        # Read message length and unpack it into an integer
        raw_msglen = self.all_recv(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.all_recv(sock, msglen)

    def all_recv(self, sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data


class Experimenter:

    """
    A special server which collects each experiment's result
    """

    def __init__(self):
        self.FTET_Sim_rtx = 0    # the remain transactions
        self.FTET_Nsim_rtx = 0    # the remain transactions
        self.welfare_sum = {"FTETSIM": 0, "FTETNSIM": 0, "CURRENTSIM": 0, "CURRENTNSIM": 0}
        self.welfare_times = {"FTETSIM": 0, "FTETNSIM": 0, "CURRENTSIM": 0, "CURRENTNSIM": 0}
        self.result = 0
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_service(self):
        env_dist = os.environ
        host = env_dist.get('LOCAL_IP')  # get the environment variable: LOCAL_IP
        port = 5678
        self.server_sock.bind((host, port))
        self.server_sock.listen(1024)
        # self.handle_loop()
        t = threading.Thread(target=self.handle(), args=())
        t.start()
        t.join()

    def handle(self):
        log.info("Waiting for connection...")
        conn, addr = self.server_sock.accept()
        data = self.recv_msg(conn)
        data = json.loads(data.decode())
        log.info("The " + data["mode"] + data["propose"] + "'s social welfare is " + str(data["welfare"]))
        log.info("with " + str(data["user_num"]) + " users and remains " + str(data["remain_txs"]) + " transactions")

    def handle_loop(self):
        while True:
            conn, addr = self.server_sock.accept()
            data = self.recv_msg(conn)
            data = json.loads(data.decode())
            self.welfare_sum[data["mode"] + data["propose"]] += data["welfare"]
            self.welfare_times[data["mode"] + data["propose"]] += 1
            if data["mode"] == "FTET" and data["propose"] == "SIM":
                self.FTET_Sim_rtx += data["remain_txs"]
            elif data["mode"] == "FTET" and data["propose"] == "NSIM":
                self.FTET_Nsim_rtx += data["remain_txs"]

    def save_result(self):
        log.info("The average social welfare of FTET mechanism and simultaneous proposing is:")
        log.info(self.welfare_sum["FTETSIM"] / self.welfare_times["FTETSIM"])
        log.info("with average remain transaction of")
        log.info(self.FTET_Sim_rtx / self.welfare_times["FTETSIM"])
        log.info("The average socail welfare of FTET mechanism and non-simultaneous proposing is:")
        log.info(self.welfare_sum["FTETNSIM"] / self.welfare_times["FTETNSIM"])
        log.info("with average remain transaction of")
        log.info(self.FTET_Nsim_rtx / self.welfare_times["FTETNSIM"])
        log.info("The average social welfare of Current blockchain mechanism and simultaneous proposing is:")
        log.info(self.welfare_sum["CURRENTSIM"] / self.welfare_times["CURRENTSIM"])
        log.info("The average social welfare of Current blockchain mechanism and non-simultaneous proposing is:")
        log.info(self.welfare_sum["CURRENTNSIM"] / self.welfare_times["CURRENTNSIM"])
        exit()

    """
    Methods from the internet
    https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
    """

    def recv_msg(self, sock):
        # Read message length and unpack it into an integer
        raw_msglen = self.all_recv(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.all_recv(sock, msglen)

    def all_recv(self, sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data
