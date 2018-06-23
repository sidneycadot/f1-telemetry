 #! /usr/bin/env python3

import socket
import time
import numpy as np
import struct

import f1_2017_defs as f1_2017

def broadcast_file_packets(filename, port):

    sock = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    address = ('<broadcast>', port)
    sock.connect(address)

    with open(filename, "rb") as fi:

        t0_udp = None
        t0_wallclock = None
        packet_index = 0
        realtime_factor = 10.0
        while True:
            packet = fi.read(f1_2017.UdpPacketSize)
            if len(packet) != f1_2017.UdpPacketSize:
                break
            t_udp = struct.unpack('<f', packet[0:4])[0]
            t_wallclock = time.time()
            if t0_udp is None:
                # First packet!
                t0_udp = t_udp
                t0_wallclock = t_wallclock
            t_emit = t0_wallclock + (t_udp - t0_udp) / realtime_factor
            t_sleep = t_emit - t_wallclock
            if t_sleep >= 0:
                time.sleep(t_sleep)
            sock.send(packet)

            print("\r{:12.3f}".format(t_udp), end = '')

    print()

def main():

    filename = "spa_franchorchamps_race_telemetry.dat"
    port = 20777
    broadcast_file_packets(filename, port)

if __name__ == "__main__":
    main()

