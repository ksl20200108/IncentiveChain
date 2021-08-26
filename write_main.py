def write_py(main_num):
    f = open("main" + str(main_num) + ".py", "w")
    f.write("import os\n")
    f.write("import pickle\n")
    f.write("import time\n")
    f.write("\n")
    f.write("\n")

    
    f.write("def main():\n")
    f.write("\n")
    f.write('    time.sleep(200)\n')
    

    f.write("\n")
    f.write("\n")
    f.write("main()\n")
    f.write("\n")

    f.close()


for i in range(1, 9):
    for j in range(1, 11):
        write_py(int(str(i) + str(j)))
