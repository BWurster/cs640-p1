import argparse
import socket
from datetime import datetime
import struct
import os
import time

socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
this_host = socket.gethostname()
this_ip_addr = socket.gethostbyname(this_host)

def process_request(file_req, requester_ip, req_port, rate, curr_seq_no, length):
    # maybe we end of file token
    remain_file_len = os.path.getsize(file_req)
    payload = ""
    extract_file = open(file_req, "r")
    while (remain_file_len > 0):
        saveTime = time.time()
        tell_length = 0
        # less bytes in file remaining than length
        if remain_file_len < length:
            payload = extract_file.read(remain_file_len)
            tell_length = remain_file_len
            remain_file_len = 0
        else:
            payload = extract_file.read(length)
            tell_length = length
            remain_file_len -= length

        # create udp header (D since its a data packet)
        udp_header = struct.pack("!cII", b'D', socket.htonl(curr_seq_no), tell_length)

        # print information
        print("DATA Packet")
        print("send time:  " + str(datetime.now()))
        print("requester addr:  " + requester_ip + ":" + str(req_port))
        print("Sequence num:  " + str(curr_seq_no))
        print("length:  " + str(tell_length))
        print("payload:  " + payload[0:4])
        # extra space
        print("")

        # increment sequence number
        curr_seq_no += tell_length
        # combine header with payload
        packet_with_header = udp_header + payload.encode()

        # send this packet to the requester
        requester_addr = (requester_ip, req_port)
        socket_obj.sendto(packet_with_header, requester_addr)

        # respect the rate
        # time.sleep(1/rate)

        while(time.time() - saveTime < 1/rate):
            continue

    # send END packet once done
    # create udp header (E since it's an end packet)
    udp_header = struct.pack("!cII", b'E', curr_seq_no, 0)
    # combine header with payload (no payload for end packet)
    packet_with_header = udp_header

    # send this packet to the requester
    requester_addr = (requester_ip, req_port)
    socket_obj.sendto(packet_with_header, requester_addr)
    print("END Packet")
    print("send time:  " + str(datetime.now()))
    print("requester addr:  " + requester_ip + ":" + str(req_port))
    print("Sequence num:  " + str(curr_seq_no))
    print("length:  0")
    print("payload:  ")
    # extra space
    print("")


def check_request(req_port, rate, curr_seq_no, length):
    while True:
        # second nulled out because ip is right but the port is wrong because the requester sends to a random port
        full_packet, (requester_ip, _) = socket_obj.recvfrom(1024)
        udp_header = full_packet[:9]
        # requester fills payload with name of file its requesting
        file_req = full_packet[9:]
        udp_header = struct.unpack("!cII", udp_header)
        
        if(udp_header[0] == b'R'):
            process_request(file_req, requester_ip, req_port, rate, curr_seq_no, length)
            break


def main():
    parser = argparse.ArgumentParser(description="gets sender data")

    parser.add_argument('-p', metavar='port')
    parser.add_argument('-g', metavar='requester_port')
    parser.add_argument('-r', metavar='rate')
    parser.add_argument('-q', metavar='seq_no')
    parser.add_argument('-l', metavar='length')

    args = parser.parse_args()

    socket_obj.bind((this_ip_addr, int(args.p)))

    check_request(int(args.g), float(args.r), int(args.q), int(args.l))

if __name__ == "__main__":
    main()
