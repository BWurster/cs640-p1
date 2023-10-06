import argparse
import socket
import struct
from datetime import datetime
import time

# create socket object
socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
this_host = socket.gethostname()
this_ip_addr = socket.gethostbyname(this_host)
socket.bind((this_ip_addr, port))

def send_data(port, file_option, tracker_lines):

    for line in tracker_lines:
        if line[0] == file_option:
            ip_addr = socket.gethostbyname(line[2])
            sender_addr = (ip_addr, line[3])

            # create udp header (R since its a request packet)
            udp_header = struct.pack("!cII", 'R', 0, 0)
            # combine header with payload
            packet_with_header = udp_header + file_option

            # send this request to the sender
            socket_obj.sendto(packet_with_header, sender_addr)

def receive_data():
    # decide when this ends...
    start_time = time.time()
    while True:
        full_packet, (sender_ip, sender_port) = socket_obj.recvfrom(1024)
        udp_header = full_packet[:9]
        data = full_packet[9:]
        udp_header = struct.unpack("!cII", udp_header)

        packet_type = {}
        packet_type['D'] = "DATA"
        packet_type['E'] = "END"

        total_packets = 0
        total_bytes = 0

        # process packet with print statements
        print("Requester's print information")

        print(packet_type[udp_header[0]] + " Packet\n")
        print("recv time   " + str(datetime.now()) + "\n")
        print("Sender ip address:  " + sender_ip + "\n")
        print("Sender port:  " + sender_port + "\n")
        print("sequence:  " + str(udp_header[1]) + "\n")
        print("length:  " + str(udp_header[2]) + "\n")
        if udp_header[0] == 'D':
            print("payload:  " + str(data[0:4]) + "\n")
        else:
            print("payload:  0\n")
        total_packets += 1
        total_bytes += udp_header[2]

        # leave space
        print("\n")

        # end packet case (print summary info)
        if udp_header[0] == 'E':
            print("Summary\n")
            print("Total Data packets  " + str(total_packets) + "\n")
            print("Total Data bytes  " + str(total_bytes) + "\n")
            end_time = time.time()
            print("Average packets/second  " + str(total_packets/(end_time - start_time) + "\n")
            print("Duration of the test  " + str(end_time - start_time) + "\n")
            # reset timer
            start_time = time.time()

        # leave space
        print("\n")


def main():
    parser = argparse.ArgumentParser(description="gets requester data")

    parser.add_argument('-p', metavar='port')
    parser.add_argument('-o', metavar='file_option')

    args = parser.parse_args()

    tracker_lines = []

    tracker_file = open("tracker.txt", "r")
    curr_line = tracker_file.readline()
    while len(curr_line) != 0:
        send_parts = curr_line.split(" ")
        send_parts[-1] = send_parts[-1].strip()
        tracker_lines.append(send_parts)
        curr_line = tracker_file.readline()

    tracker_lines.sort(key = lambda x: int(x[1]))

    send_data(args.p, args.o, tracker_lines)

    receive_data()




if __name__ == "__main__":
    main()
