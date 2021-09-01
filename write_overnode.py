def write_overnode_yaml():
    f = open("overnode.yaml")
    line = f.readlines()
    line = line[2]
    num_str = line[10:(len(line) - 2)]
    f.close()
    f = open("overnode.yaml", "w")
    f.write("id: my-overnode-project\n")
    f.write("version: 3\n")
    if int(num_str[1:]) < 10:
        num_str = str(int(num_str) + 1)
        f.write("experiment" + num_str + ":\n")
    else:
        num_str = str(int(num_str[0]) + 1) + "1"
        f.write("experiment" + num_str + ":\n")
    f.write("   ./" + num_str + ".yaml: *\n")


write_overnode_yaml()
