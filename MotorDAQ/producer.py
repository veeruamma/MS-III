# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 16:18:51 2019

@author: Veeresh Ittangihal
"""

import paho.mqtt.client as mqtt
import  time
from datetime import date
from time import sleep





topic = 'motor'

HOST = "10.1.1.11"
PORT = 1883

# If broker asks client ID.
client_id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
client = mqtt.Client(client_id=client_id)

# If broker asks user/password.
#user = "535548aa-cb69-4180-afb7-8f961dfd9c0b:cfd379b5-ca6f-47b6-89d0-1dde5f336b80"
#password = "BnS3rrzGLcVaP20zs77LtdTjd"
#client.username_pw_set(user, password)

client.connect(HOST, PORT)

#measurement1 = 'bin_trial'
