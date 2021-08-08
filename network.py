"""
tbc: to be continued
    Add a call to Experimenter.save_result() at the end of 10 experiments (send ending message from miners)
    main function
        def experiment_start
tbt: to be tested
    Network.server_handler
    Network.client_main_loop
    Network.acquire_peer_info
tbd: to be deleted
tbm: to be modified
    Network.experimenter_host = -> define it in docker
    Network.client_main_loop: add another loop outside the original for loop
        to implement automatic repetitive experiment, at the start of each experiment：
            Network.bc = Blockchain(fees1, fees2, mode, propose)
            Network.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Network.lock = threading.Lock()
            Network.start_client_loop()
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
PEERS_LIST: since we do not implement seed peers in real Bitcoin network
we use this list to simulate the list given by seed peers. 
Local client randomly connect to peers included in this list.  
"""
PEERS_LIST = []
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

    def __init__(self, fees1, fees2, mode, propose):
        """
        :param fees1: transactions in simultaneous proposing and early half transactions in non-simultaneous proposing
        :param fees2: late half transactions in non-simultaneous proposing
        :param mode: "FTET" mechanism or current blockchain  mechanism
        :param propose: simultaneous proposing or non-simultaneous proposing
        self.bc: the local blockchain
        self.server_sock: socket object for server side
        """
        self.bc = Blockchain(fees1, fees2, mode, propose)
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.clients = random_chosen(bootstrap)
        self.lock = threading.Lock()
        self.experimenter_host = None    # need to be modified

    """
    Server side
    """

    def start_server_loop(self, max_conn):
        """
        :param max_conn: maximum number of connection to this server
        self.HOST: ipv4 address of local host
        self.PORT: all the peers communicate between each other through this port, predefined in compose yml as 5678
        """
        env_dist = os.environ
        host = env_dist.get('LOCAL_IP')  # get the environment variable: LOCAL_IP
        port = 5678
        self.server_sock.bind((host, port))
        self.server_sock.listen(max_conn)
        """
        1st thread in Network: Server thread
        """
        t = threading.Thread(target=self.server_main_loop(), args=())
        t.start()

    def server_main_loop(self):
        while True:
            conn, addr = self.server_sock.accept()
            t = threading.Thread(target=self.server_handler, args=(conn, addr))
            t.start()

    def server_handler(self, conn, addr):    # max_recv can be 61995
        """
        :param conn:
        :param addr:
        data: blockchain length from client side
        """
        data = self.recv_msg(conn)
        data = json.loads(data.decode())
        if data["type_"] == 1:
            self.handle_request_len(conn)
        elif data["type_"] == 2:
            self.handle_request_chain(conn)
        else:
            raise ValueError("Server side: the message type is not legal")

    def handle_request_len(self, conn):
        self.lock.acquire()
        sender = json.dumps({"type_": LEN_MSG, "data": len(self.bc.blocks)}).encode()
        self.lock.release()
        self.send_msg(conn, sender)

    def handle_request_chain(self, conn):
        sender = json.dumps(self.bc.serialize()).encode()
        self.send_msg(conn, sender)

    """
    Client side
    """

    def start_client_loop(self, connection_num):
        t = threading.Thread(target=self.client_main_loop, args=(connection_num))
        t.start()

    def client_main_loop(self, connection_num):
        """
        :param connection_num: the defined number of connections
        """
        if self.bc.MODE == "FTET":
            set_round = 13
        else:
            set_round = 24
        for r in range(0, set_round):
            """
            In one experiment, stop loop after mining defined number of blocks
            """
            # mining
            self.bc.add_block_by_mining()
            time.sleep(60)    # sleep for 1 minutes
            # start connections thread -> require server's chain length
            threads = [None] * connection_num
            self.results = [None] * connection_num
            self.results_hosts = {}
            hosts = random.sample()
            # recv results
            for i in range(0, connection_num):
                threads[i] = threading.Thread(target=self.acquire_peers_info, args=(i, hosts[i]))
                threads[i].start()
            # stop connections
            for i in range(0, connection_num):
                threads[i].join()
                threads[i] = None    # de-reference the thread
            # compare with the longest (save ipv4 address)
            max_length = max(self.results)
            self.lock.acquire()
            if max_length > len(self.bc.blocks):
                # shorter: start client connection -> request chain info for the optimal address
                data = self.acquire_peer_chain(self.results_hosts[max_length])
                self.results_hosts = None    # de-reference the hosts dictionary
                self.bc = Blockchain.deserialize(data)    # update local chain
            self.lock.release()
            # -> start mining again
        # calculate the social welfare
        self.bc.update_total_welfare()
        # send the information to the Experimenter
        if self.experimenter_host:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.experimenter_host, 5678))
            sender = json.dumps({
                "type_": RST_MSG,
                "mode": self.bc.MODE, "propose": self.bc.PROPOSE,
                "welfare": self.bc.current_social_welfare,
                "remain_txs": len(self.bc.transaction_pool1)
            }).encode()
            self.send_msg(s, sender, True)    # close the connection after reporting

    def acquire_peers_info(self, index, host, port=5678):
        """
        :param host: randomly chosen host
        :param port: pre-defined port 5678. All servers communicate on this port
        :return:
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
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

    def acquire_peer_chain(self, host, port=5678):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        # require server's chain
        sender = json.dumps({"type_": BC_REQ, "data": None}).encode()
        self.send_msg(s, sender)
        receiver = self.recv_msg(s)
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

    """The special server which collects each experiment's result"""

    def __init__(self):
        self.FTET_Sim_rtx = 0    # the remain transactions
        self.FTET_Nsim_rtx = 0    # the remain transactions
        self.welfare_sum = {"FTETSIM": 0, "FTETNSIM": 0, "CURRENTSIM": 0, "CURRENTNSIM": 0}
        self.welfare_times = {"FTETSIM": 0, "FTETNSIM": 0, "CURRENTSIM": 0, "CURRENTNSIM": 0}
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_service(self):
        env_dist = os.environ
        host = env_dist.get('LOCAL_IP')  # get the environment variable: LOCAL_IP
        port = 5678
        self.server_sock.bind((host, port))
        self.server_sock.listen(1024)
        self.handle_loop()

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
        print("The average social welfare of FTET mechanism and simultaneous proposing is:")
        print(self.welfare_sum["FTETSIM"] / self.welfare_times["FTETSIM"])
        print("with average remain transaction of")
        print(self.FTET_Sim_rtx / self.welfare_times["FTETSIM"])
        print("The average socail welfare of FTET mechanism and non-simultaneous proposing is:")
        print(self.welfare_sum["FTETNSIM"] / self.welfare_times["FTETNSIM"])
        print("with average remain transaction of")
        print(self.FTET_Nsim_rtx / self.welfare_times["FTETNSIM"])
        print("The average social welfare of Current blockchain mechanism and simultaneous proposing is:")
        print(self.welfare_sum["CURRENTSIM"] / self.welfare_times["CURRENTSIM"])
        print("The average social welfare of Current blockchain mechanism and non-simultaneous proposing is:")
        print(self.welfare_sum["CURRENTNSIM"] / self.welfare_times["CURRENTNSIM"])
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
