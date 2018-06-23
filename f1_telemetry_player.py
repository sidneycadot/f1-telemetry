 #! /usr/bin/env python3

import socket
import time
import numpy as np
import matplotlib.pyplot as plt

from f1_telemetry_dtype import F1_2017_UDPPacket

filename = "spa_franchorchamps_race_telemetry.dat"

with open(filename, "rb") as fi:
    data = fi.read()

data = np.frombuffer(data, dtype = F1_2017_UDPPacket)

plt.plot(data['m_x'], -data['m_z'])
#plt.plot(data['m_time'], data['m_totalDistance'])
#plt.plot(data['m_time'], data['m_track_size'])
#print(data['m_track_size'].min(), data['m_track_size'].max())

#ax1 = plt.subplot(211)
#for i in range(20):
#    ax1.plot(data['m_time'], data['m_car_data'][:,i]['m_carPosition'])

#ax2 = plt.subplot(212, sharex = ax1)
#for i in [17]:
#    ax2.plot(data['m_time'], data['m_car_data'][:,i]['m_lapDistance'])

plt.show()
