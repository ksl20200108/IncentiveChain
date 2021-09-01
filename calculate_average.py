"""
python3 calculate_average.py &> averages.txt &
"""

types = ["", "FTETSIM1600", "FTETSIM4800", "FTETNSIM1600", "FTETNSIM4800",
         "CURRENTSIM1600", "CURRENTSIM4800", "CURRENTNSIM1600", "CURRENTNSIM4800"]


def pick_up(num_str):
    f = open(num_str + ".log")
    line = f.readlines()
    line = line[1]
    num_str = ""
    for char in range(len(line) - 1, -1, -1):
        if char and line[char] == " ":
            break
        num_str = line[char] + num_str
    num = int(num_str)
    return num


def calculate_sum():
    sums = [0] * 9
    for i in range(1, 9):
        for j in range(1, 11):
            sums[i] += pick_up(str(i) + str(j))
    return sums


def calculate_average():
    sums = calculate_sum()
    for i in range(1, 9):
        print("the average of " + types[i] + " is " + str(sums[i] / 10))
