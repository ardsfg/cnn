import numpy as np
from numpy import load


data = load('/Users/ray/Downloads/2020-12-08npzs/kata1-b40c256x2-s5095420928-d1229425124/0A0C37CBED7EFC7539163FF09BBFD31C.npz')
lst = data.files
cnt = 1
for item in lst:
    print(item)
    print(data[item])
    cnt+=1
    if(cnt == 2):
        break