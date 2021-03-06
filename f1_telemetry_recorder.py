 #! /usr/bin/env python3

import socket

import f1_2017_defs as f1_2017

filename = "recorder.dat"
udp_port = 20777

with open(filename, "wb") as fo:

    sock = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
    try:
        # Allow multiple receiving endpoints...
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        address = ('', udp_port)
        sock.bind(address)

        good_packet_count = 0
        bad_packet_count = 0

        while True:
            (packet, address) = sock.recvfrom(2048)
            if len(packet) != f1_2017.UdpPacketSize:
                bad_packet_count += 1
            else:
                good_packet_count += 1
                fo.write(packet)

            print("\rPackets recorded: {} ({} bad)".format(good_packet_count, bad_packet_count), end = '')

    finally:
        sock.close()
