import argparse
import socket
from datetime import datetime

def check_request(port, req_port, rate, curr_seq_no, length):
    # create socket object
    socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    this_host = socket.gethostname()
    this_ip_addr = socket.gethostbyname(this_host)
    socket.bind((this_ip_addr, port))

    # second nulled out because ip is right but the port is wrong because the requester sends to a random port
    full_packet, (requester_ip, _) = socket_obj.recvfrom(1024)
    udp_header = full_packet[:9]
    # requester fills payload with name of file its requesting
    file_req = full_packet[9:]
    udp_header = struct.unpack("!cII", udp_header)

    # maybe we end of file token
    remain_file_len = os.path.getsize(file_req)
    payload = ""
    extract_file = open(file_req, "r")
    while (remain_file_len > 0):
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
        udp_header = struct.pack("!cII", 'D', curr_seq_no, tell_length)

        # print information
        print("DATA Packet\n")
        print("send time:  " + str(datetime.now()) + "\n")
        print("requester ip address:  " + requester_ip + "\n")
        print("requester port:  " + req_port + "\n")
        print("Sequence num:  " + str(curr_seq_no) + "\n")
        print("length:  " + str(tell_length) + "\n")
        print("payload:  " + payload[0:4] + "\n")
        # extra space
        print("\n")

        # increment sequence number
        curr_seq_no += tell_length
        # combine header with payload
        packet_with_header = udp_header + payload

        # send this packet to the requester
        sender_addr = (requester_ip, req_port)
        socket_obj.sendto(packet_with_header, sender_addr)

        # respect the rate
        time.sleep(1/rate)

    # send END packet once done
    # create udp header (E since it's an end packet)
    udp_header = struct.pack("!cII", 'E', curr_seq_no, 0)
    # combine header with payload (no payload for end packet)
    packet_with_header = udp_header + ""

    # send this packet to the requester
    sender_addr = (requester_ip, req_port)
    socket_obj.sendto(packet_with_header, sender_addr)
    print("END Packet\n")
    print("send time:  " + str(datetime.now()) + "\n")
    print("requester ip address:  " + requester_ip + "\n")
    print("requester port:  " + req_port + "\n")
    print("Sequence num:  " + str(curr_seq_no) + "\n")
    print("length:  0\n")
    print("payload:  \n")
    # extra space
    print("\n")



def main():
    parser = argparse.ArgumentParser(description="gets sender data")

    parser.add_argument('-p', metavar='port')
    parser.add_argument('-g', metavar='requester_port')
    parser.add_argument('-r', metavar='rate')
    parser.add_argument('-q', metavar='seq_no')
    parser.add_argument('-l', metavar='length')

    args = parser.parse_args()

    check_request(args.p, args.g, args.r, args.q, args.l)

if __name__ == "__main__":
    main()
