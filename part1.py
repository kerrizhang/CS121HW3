import os
import json

a = os.walk('DEV')
for i, b in enumerate(a):
    print(b[0])
    if b[0] != 'DEV':
        something = os.listdir(b[0])
        print(" --> " + str(something))

    # print(b[0])
    # if i == 2:
    # folders = b[1]
    # for folder in folders:
    #     os.listdir(b[1])
    # print(b[1])