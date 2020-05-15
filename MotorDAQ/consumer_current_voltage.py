# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 16:29:59 2019

@author: Veeresh Ittangihal
"""

import time
from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt
import struct

sample_legth = 2048

data_packet_length = 128

current_index = int(sample_legth / data_packet_length)


HOST = "10.1.1.11"
PORT = 1883
#
#global data_points, header
data_points =[]
header = []

#client_id='TI_AM3358_III'

# To recieve data from all the topics
#topic = "mbed/lpc1769/+"

#Topics for Current and Voltage signals
#I_a = mbed/lpc1769/a1d685d6-b9f6-a000-b000-91f7ca006000
#I_b = mbed/lpc1769/a1d685d6-b9f6-a000-b000-91f7ca006001
#I_c = mbed/lpc1769/a1d685d6-b9f6-a000-b000-91f7ca006002
#V_a = mbed/lpc1769/a1d685d6-b9f6-a000-b000-91f7ca006003
#V_b = mbed/lpc1769/a1d685d6-b9f6-a000-b000-91f7ca006004
#V_c = mbed/lpc1769/a1d685d6-b9f6-a000-b000-91f7ca006005


topic = "mbed/lpc1769/a1d685d6-b9f6-a000-b000-91f7ca006000" 


def get_influx_client():
    host ='localhost'
    port=8086
    dbName= 'motorDAQ'
    user= ''
    pwd=''
    client =  InfluxDBClient(host, port,user, pwd, dbName)
    return client


def push_influx(msg):
    influx_client = get_influx_client()
    data ={}
    data['measurement']= 'motor2'
    fields ={}
    for i in range(0, len(msg)):
        fields['f'+str(i)] = msg[i][0]
    data['fields']= fields
    json_body = []
    json_body.append(data)
#    print('JSON BODY', json_body)
    written = influx_client.write_points(json_body)
#    print('value of writeeeeeee', written)
    if written == True:
        print('successfully written to DB')
    else :
        print('Could not write into DB')


def client_loop():
    client_id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    client = mqtt.Client(client_id)
#    client.username_pw_set("535548aa-cb69-4180-afb7-8f961dfd9c0b:cfd379b5-ca6f-47b6-89d0-1dde5f336b80", "BnS3rrzGLcVaP20zs77LtdTjd")  #須設置，否则會返回「Connected with result code 4」
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOST, PORT, 60)
    client.loop_forever()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)


def read_int(msg):
    for i in range(0, len(msg), 4):
        index = int.from_bytes(msg[i:i+4], byteorder='little')
        header.append(index)
#        print('index_ values ==== ', index)
    return header
    

def read_float(msg):
    index = int.from_bytes(msg[0:4], byteorder='little')
    print(' lenth of msg ', index)
    for i in range(4, len(msg), 4):
        value = struct.unpack('<f',msg[i:i+4])
        data_points.append(value)
        print('data values', len(data_points))
    return index, data_points
    
def check_header(msg):
    head = False
    index = int.from_bytes(msg[0:4], byteorder='little')
    if index == 0:
        head = True
    return head

def on_message(client, userdata, msg):
    write_flag =0
    write_data = []
    is_it_header = check_header(msg.payload[0:16])
    if is_it_header ==True:
        write_header = read_int(msg.payload[0:16])
        print('head ===', write_header)
    else :
        write_flag, write_data = read_float(msg.payload)
        print('index == ', write_flag)
        print('data ', len(write_data))
    if write_flag==current_index:
        print('data ====', len(write_data))
        push_influx(write_data)
        global data_points
        data_points = []
        global header
        header = []

def write_bin_to_file():
    print('hello sir')


if __name__ == '__main__':
    client_loop()
    
