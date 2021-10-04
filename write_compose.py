def write_yaml(main_num):

    fee1 = ["", "FTETSIMfee11600", "FTETSIMfee14800", "FTETNSIMfee11600", "FTETNSIMfee14800",
            "CURRENTSIMfee11600", "CURRENTSIMfee14800", "CURRENTNSIMfee11600", "CURRENTNSIMfee14800"]
    fee2 = ["", "FTETSIMfee21600", "FTETSIMfee24800", "FTETNSIMfee21600", "FTETNSIMfee24800",
            "CURRENTSIMfee21600", "CURRENTSIMfee24800", "CURRENTNSIMfee21600", "CURRENTNSIMfee24800"]

    f = open(str(main_num) + ".yaml", "w")
    f.write("version: '3'\n")
    f.write("\n")
    f.write('services:\n')
    f.write("\n")

    f.write("  experimenter" + ":\n")
    f.write("    image: two_miners_test:1.0 \n")

    """old"""
    # f.write("    container_name: experimenter\n")

    f.write("    environment:\n")
    f.write("      - STATIC_IP=192.168.1." + str(0) + "\n")
    f.write("    ports:\n")
    f.write("      - " + str(5679 + 0 - 1) + ":5678\n")

    """old"""
    # f.write("    privileged: true\n")

    f.write("    volumes:\n")
    f.write("      - ./main" + str(main_num)  + ".py:/run/main.py\n")
    f.write("      - ./network.py:/run/network.py\n")
    f.write("      - ./blockchain_structures.py:/run/blockchain_structures.py\n")
    f.write("      - ./random_functions.py:/run/random_functions.py\n")
    f.write("      - ./tests.py:/run/tests.py\n")
    f.write("      - ./data/" + str(main_num)[1:] + fee1[int(str(main_num)[0])] + ".npy" + ":/run/data/"
        + str(main_num)[1:] + fee1[int(str(main_num)[0])] + ".npy" + "\n")
    f.write("      - ./data/" + str(main_num)[1:] + fee2[int(str(main_num)[0])] + ".npy" + ":/run/data/"
        + str(main_num)[1:] + fee2[int(str(main_num)[0])] + ".npy" + "\n")
    f.write("      - ./peers:/run/peers\n")
    f.write("      - ./experimenter.py:/run/experimenter.py\n")
    f.write("    command: >\n")
    f.write('        bash -c "python3 experimenter.py"\n')

    """old"""
    # f.write("    networks:\n")
    # f.write("      static-network:\n")
    # f.write("        ipv4_address: 192.168.1." + str(0) + "\n")

    """new"""
    f.write("    networks:\n")
    f.write("      - test\n")
    f.write("    cap_add::\n")
    f.write("      - NET_ADMIN\n")

    f.write("\n")
    f.write("\n")

    for i in range(1, 51):    # 5 users
        f.write("  node" + str(i) + ":\n")
        f.write("    image: two_miners_test:1.0 \n")
        f.write("    depends_on:\n")
        f.write("      - experimenter\n")

        """old"""
        # f.write("    container_name: node" + str(i) + "\n")

        f.write("    environment:\n")
        f.write("      - STATIC_IP=192.168.1." + str(i) + "\n")
        f.write("    ports:\n")
        f.write("      - " + str(5679 + i - 1) + ":5678\n")

        """old"""
        # f.write("    privileged: true\n")

        f.write("    volumes:\n")
        f.write("      - ./main" + str(main_num)  + ".py:/run/main.py\n")
        f.write("      - ./network.py:/run/network.py\n")
        f.write("      - ./blockchain_structures.py:/run/blockchain_structures.py\n")
        f.write("      - ./random_functions.py:/run/random_functions.py\n")
        f.write("      - ./tests.py:/run/tests.py\n")
        f.write("      - ./data/" + str(main_num)[1:] + fee1[int(str(main_num)[0])] + ".npy" + ":/run/data/"
                + str(main_num)[1:] + fee1[int(str(main_num)[0])] + ".npy" + "\n")
        f.write("      - ./data/" + str(main_num)[1:] + fee2[int(str(main_num)[0])] + ".npy" + ":/run/data/"
                + str(main_num)[1:] + fee2[int(str(main_num)[0])] + ".npy" + "\n")
        f.write("      - ./peers:/run/peers\n")
        f.write("    command: >\n")
        f.write('        bash -c "python3 main.py"\n')

        """old"""
        # f.write("    networks:\n")
        # f.write("      static-network:\n")
        # f.write("        ipv4_address: 192.168.1." + str(i) + "\n")

        """new"""
        f.write("    networks:\n")
        f.write("      - test\n")
        f.write("    cap_add::\n")
        f.write("      - NET_ADMIN\n")

        f.write("\n")
        f.write("\n")

    """new"""
    f.write("\n")
    f.write("networks: \n")
    f.write("  test:\n")
    f.write("    external: true\n")
    f.write("    name: test")

    f.write("# docker network create --driver overlay --subnet 192.168.0.0/16 --gateway 192.168.0.1 --attachable test")

    f.close()


for i in range(1, 9):
    for j in range(1, 11):
        write_yaml(int(str(i) + str(j)))
