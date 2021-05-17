#!/usr/bin/python
from bcc import BPF
import time
import socket
import struct
import sys
import imap, host
import geoip2

host.init()
device = "wlp8s0"
bpf = BPF(src_file="packet-capture.c")
fn = bpf.load_func("xdp_ip_counter", BPF.XDP)
bpf.attach_xdp(device, fn, 0)
counters = bpf.get_table("counters")

myPrivateIP = imap.getMyPrivateIP()
while True:
    print("watchdog")
    try:
        for k in counters.keys():
            val = counters[k].value
            if val:
                source = socket.inet_ntoa(struct.pack("!I", k.s_v4_addr))
                destination = socket.inet_ntoa(struct.pack("!I", k.d_v4_addr))
                if destination != myPrivateIP:
                    continue
                else:
                    try:
                        imap.addPeerToDB(source)
                    except geoip2.errors.AddressNotFoundError:
                        continue
        time.sleep(1)
    except KeyboardInterrupt:
        imap.deletePeerData()
        print("Removing filter from device.")
        break
    except Exception as e:
        print(f"Something went wrong. Exception: {e}")
        break

bpf.remove_xdp(device, 0)
host.dropTable()