import argparse
import socket
import struct
from datetime import datetime
import time

# create socket object
socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
this_host = socket.gethostname()
this_ip_addr = socket.gethostbyname(this_host)

def send_data(line):
    ip_addr = socket.gethostbyname(line[2])
    sender_addr = (ip_addr, int(line[3]))

    # create udp header (R since its a request packet)
    udp_header = struct.pack("!cII", b'R', 0, 0)
    # combine header with payload
    packet_with_header = udp_header + line[0].encode()

    # send this request to the sender
    socket_obj.sendto(packet_with_header, sender_addr)

def receive_data():
    # decide when this ends...
    start_time = time.time()

    total_packets = 0
    total_bytes = 0

    while True:
        full_packet, (sender_ip, sender_port) = socket_obj.recvfrom(1024)
        udp_header = full_packet[:9]
        data = full_packet[9:]
        udp_header = struct.unpack("!cII", udp_header)

        packet_type = {}
        packet_type[b'D'] = "DATA"
        packet_type[b'E'] = "END"

        # process packet with print statements
        print("Requester's print information")

        print(packet_type[udp_header[0]] + " Packet")
        print("recv time   " + str(datetime.now()))
        print("sender addr:  " + sender_ip + ":" + str(sender_port))
        print("sequence:  " + str(udp_header[1]))
        print("length:  " + str(udp_header[2]))
        if udp_header[0] == b'D':
            print("payload:  " + str(data[0:4]))
            total_packets += 1
        else:
            print("payload:  0")
        total_bytes += udp_header[2]

        # leave space
        print("")

        # end packet case (print summary info)
        if udp_header[0] == b'E':
            print("Summary")
            print("Total Data packets  " + str(total_packets))
            print("Total Data bytes  " + str(total_bytes))
            end_time = time.time()
            print("Average packets/second  " + str(total_packets/(end_time - start_time)))
            print("Duration of the test  " + str(end_time - start_time))
            break

        # leave space
        print("")


def main():
    parser = argparse.ArgumentParser(description="gets requester data")

    parser.add_argument('-p', metavar='port')
    parser.add_argument('-o', metavar='file_option')

    args = parser.parse_args()

    socket_obj.bind((this_ip_addr, int(args.p)))

    tracker_lines = []
    tracker_file = open("tracker.txt", "r")
    curr_line = tracker_file.readline()
    while len(curr_line) != 0:
        send_parts = curr_line.split(" ")
        if(send_parts[0] == args.o):
            send_parts[-1] = send_parts[-1].strip()
            tracker_lines.append(send_parts)
        curr_line = tracker_file.readline()

    tracker_lines.sort(key = lambda x: int(x[1]))

    for part in tracker_lines:
        send_data(part)
        receive_data()


if __name__ == "__main__":
    main()
