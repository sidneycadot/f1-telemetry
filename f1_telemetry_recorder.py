 #! /usr/bin/env python3

import socket

filename = "recorder.dat"
udp_port = 20777
udp_packet_size_expected = 1289

with open(filename, "wb") as fo:

    sock = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
    try:
        # Allow multiple receiving endpoints...
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        address = ('', udp_port)
        sock.bind(address)

        packets_received = 0
        while True:
            (packet, address) = sock.recvfrom(2048)
            packets_received += 1
            if packets_received % 100 == 0:
                print("Packets received: {}".format(packets_received))
            if len(packet) != udp_packet_size_expected:
                print("Bad UDP packet (length: {} bytes)".format(len(packet)))
                continue
            fo.write(packet)

    finally:
        sock.close()
