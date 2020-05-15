# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 19:45:53 2018

@author: Veer
"""
from  struct import unpack
import csv
from operator import mul

row_list=[]
mul_row = []
channel = 18
voltage= 5
ct_rate = 0.5
pt_rate= 75
read_bytes_count= channel*2
byte_array = bytearray()
file = open('data.bin', 'rb')

rate=[75,75,75,0.5,0.5,0.5] # PT and CT rates

try:
    byte_array = file.read(read_bytes_count)
    with open('example3.csv', 'w', newline='') as f:
        while byte_array != "":
            thewriter = csv.writer(f)
            for i in range(0, read_bytes_count, 2):
                b = bytes(byte_array[i:i+2])
                data = unpack('<h', b)
                data = float(data[0])*(voltage/float(32767))
                row_list.append(data)
            #ll =[*map(mul,rate,rowlist)]  -- for adding ct and pt rate
            thewriter.writerow(row_list)
            byte_array = file.read(read_bytes_count)
            row_list=[]
finally:
    file.close()

