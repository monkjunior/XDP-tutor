#!/usr/bin/python
from bcc import BPF
import time

device = "wlp8s0"
maptype = "percpu_array"
bpf = BPF(src_file="basic01-xdp-pass.c")
fn = bpf.load_func("xdp_count_func", BPF.XDP)
bpf.attach_xdp(device, fn, 0)

passcnt_map = bpf.get_table("xdp_stats_map")
prev_pkgs = [0] * 5
prev_bytes = [0] * 5
print("Counting packets, hit CTRL+C to stop")
while True:
    try:
        for k in passcnt_map.keys():
            total_pkgs = 0
            total_bytes = 0
            if maptype == "array":
                total_pkgs = passcnt_map[k].rx_packets 
                total_bytes = passcnt_map[k].rx_bytes   
            else:
                for c in range(len(passcnt_map[k])):
                    total_pkgs += passcnt_map[k][c].rx_packets 
                    total_bytes += passcnt_map[k][c].rx_bytes
            i = k.value
            if total_pkgs:
                last_1s_pkgs = total_pkgs - prev_pkgs[i]
                last_1s_bytes = total_bytes - prev_bytes[i]
                prev_pkgs[i] = total_pkgs
                prev_bytes[i] = total_bytes
                print("{}: {} pkt/s \t {} bytes/s".format(i, last_1s_pkgs, last_1s_bytes))
        time.sleep(1)
    except KeyboardInterrupt:
        print("Removing filter from device")
        break
