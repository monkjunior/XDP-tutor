#!/usr/bin/python
from bcc import BPF
import time
import sys

device = "wlp8s0"
bpf = BPF(src_file="packet01-xdp-pass.c")
fn = bpf.load_func("xdp_drop_ipv4", BPF.XDP)
bpf.attach_xdp(device, fn, 0)

# packetcnt = bpf.get_table("packetcnt")

# prev = [0]*256
# print("Printing packet counts per IP protocol-number, hit CTRL+C to stop")
# while True:
#     try:
#         for k in packetcnt.keys():
#             val = packetcnt.sum(k).value
#             i = k.value
#             if val:
#                 delta = val - prev[i]
#                 prev[i] = val
#                 print("{}: {} pkt/s".format(i, delta))
#         time.sleep(1)
#     except KeyboardInterrupt:
#         print("Removing filter from device")
#         break

# bpf.remove_xdp(device, 0)
