#!/usr/bin/python
from bcc import BPF
import sys
import time

device = "wlp8s0"
maptype = "percpu_array"
bpf = BPF(src_file="limit-band.c")
fn = bpf.load_func("packet_capture", BPF.XDP)
bpf.attach_xdp(device, fn, 0)

passcnt_map = bpf.get_table("xdp_stats_map")
trigger_limit = bpf.get_table("trigger_limit")
threshold = 800
prev_pkgs = [0] * 5
prev_bytes = [0] * 5
max_pkgs = 0
max_bytes = 0
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
                # if last_1s_bytes > max_bytes:
                #     max_bytes = last_1s_bytes
                # if last_1s_pkgs > max_pkgs:
                #     max_pkgs = last_1s_pkgs
                prev_pkgs[i] = total_pkgs
                prev_bytes[i] = total_bytes
                if last_1s_bytes*4*8/(1024) > 800:
                    trigger_limit[trigger_limit.Key(0)] = trigger_limit.Leaf(1)
                    print("{}: {} pkt/s \t {} Mbps \t YES Dropping".format(i, last_1s_pkgs, last_1s_bytes*4*8/(1024*1024)))
                else:
                    trigger_limit[trigger_limit.Key(0)] = trigger_limit.Leaf(0)
                    print("{}: {} pkt/s \t {} Mbps \t NOT Dropping".format(i, last_1s_pkgs, last_1s_bytes*4*8/(1024*1024)))
            
        time.sleep(0.25)
    except KeyboardInterrupt:
        # print("Bandwidth: {} pkt/s \t {} Mbps".format(max_pkgs*4, max_bytes*4*8/(1024*1024)))
        break

bpf.remove_xdp(device, 0)
