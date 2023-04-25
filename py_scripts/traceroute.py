#!/usr/bin/env python3

# print("Hello World")

import socket
import struct  

ICMP_ECHO_REPLY = 0
ICMP_TIME_EXCEEDED = 11


class SocketError(Exception):
    pass

# print(dir(socket.AF_INET))
# print((socket.AF_INET.value))
# print((socket.SOCK_RAW.value))
# print((socket.IPPROTO_ICMP))

def generate_packet(src_addr, dst_addr, payload):
    # TODO: create paacket from scratch.
    # This also does not work.
    from scapy.all import IP
    packet = IP(src=src_addr, dst=dst_addr) / payload
    return (packet.build())
    # import struct
    # src_addr = socket.inet_aton(src_addr) 
    # dst_addr = socket.inet_aton(dst_addr)
    # protocol = 0x0800 
    # data = b'Hello, world!'
    # packet = struct.pack('!4s4sH', src_addr, dst_addr, protocol) + data
    # return bytes(packet)


def send_single_route(TTL, dest_ip_addr, dest_port, ip_pkt_bytes):
    # Raw Socket provide user access to the Internet Control Message Protocol (ICMP).
    # sudo access
    try:
        raw_skt = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    except PermissionError as error:
        raise SocketError(repr(error))

    # print(dir(raw_skt))
    assert (raw_skt.type)  == socket.SocketKind.SOCK_RAW

    # Each packet sent on this socket will have TTL of 64/
    # TTL = 
    # setsockopt accepts little-endian unsigned integers (I: 4 bytes) Host
    ttl_bytes = struct.pack("I", TTL)
    try:
        raw_skt.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl_bytes)
    except OSError as error:
        raise SocketError(repr(error))

    # send packet on socket.
    # send ICMP echo request to host dest address
    # dest_dns_addr = ""
    # dest_port = 
    # TODO: empty bytes won't work. we need to create packet.
    # packet and dest addr have something in common don't know what.
    # i think packet should have both src ip addr and dest ip addr and
    # dest ip addr should match to input addr: sys.argv[1] 
    # ip_pkt_bytes = b"" 
    try:
        raw_skt.sendto(ip_pkt_bytes, (dest_ip_addr, dest_port))
    except OSError as error:
        raise SocketError(repr(error))  

    bufsize = 65534 # receive up to 1024 bytes of data from the socket.
    rec_pkt, addr = raw_skt.recvfrom(bufsize)

    print(f"[HOPS #{TTL}]: address: {addr}")

    # https://github.com/eureyuri/traceroute/blob/1eed6233fe1acef90ea5ab8e68b5eef641fe10d8/Traceroute.py#L97
    icmp_header = rec_pkt[20:28] 
    ip_header_values = struct.unpack(
        "bbHHh", icmp_header
    )
    print(ip_header_values)
    icmp_type = ip_header_values[0]
    if icmp_type ==  ICMP_TIME_EXCEEDED:
        print("Time Limit Exceded")
        return None
    if icmp_type ==  ICMP_ECHO_REPLY:
        print("Success")
        return None


if __name__ == "__main__":
    # ip_pkt_bytes = generate_packet("192.168.1.1", "8.8.8.8", "message")
    ip_pkt_bytes = b'\x08\x00\xf7\xff\x00\x00\x00\x00'
    print(ip_pkt_bytes)

    import sys
    addr = sys.argv[1] 
    print(f"Traceroute: {addr}")

    MX_HOPS = 13 # TTL
    for i in range(1, MX_HOPS):
        ttl = i
        val = send_single_route(ttl, addr, 0, ip_pkt_bytes)
        if val or val is None:
            break
    
