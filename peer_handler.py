from network import *


def main():
    peer_handler = Peer_Handler()
    log.info("Peer_handler start")
    peer_handler.main_loop()
    # t = threading.Thread(target=peer_handler.main_loop(), args=())
    # t.start()
    # t.join()


main()
