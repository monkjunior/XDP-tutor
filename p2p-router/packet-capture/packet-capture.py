#!/usr/bin/python
from bcc import BPF
import time
import socket
import struct
import sys

device = "wlp8s0"
bpf = BPF(src_file="packet-capture.c")
fn = bpf.load_func("xdp_ip_counter", BPF.XDP)
bpf.attach_xdp(device, fn, 0)

counters = bpf.get_table("counters")

print("Printing packet counts per IP, hit CTRL+C to stop")
while True:
    try:
        for k in counters.keys():
            val = counters[k].value
            source = socket.inet_ntoa(struct.pack("!I", k.s_v4_addr))
            destination = socket.inet_ntoa(struct.pack("!I", k.d_v4_addr))
            if val:
                print("Source IP:{}\t\t Destination IP: {}\t\t Packets count: {} pkts".format(source, destination, val))
        time.sleep(1)
    except KeyboardInterrupt:
        print("Removing filter from device")
        break

bpf.remove_xdp(device, 0)
