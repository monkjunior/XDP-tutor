/* SPDX-License-Identifier: GPL-2.0 */
// #include <bpf/bpf_endian.h>
#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/in.h>
#include <linux/ip.h>

int xdp_drop_ipv4(struct xdp_md *ctx){
	void *data_end = (void *)(long)ctx->data_end;
	void *data     = (void *)(long)ctx->data;
	struct ethhdr *eth = data;

	if (data + sizeof(*eth) > data_end) {
		return XDP_DROP;
	}

	if (eth->h_proto == bpf_htons(ETH_P_IPV6)){
		return XDP_DROP;
	}

	return XDP_PASS;
}

BPF_TABLE("percpu_array", uint32_t, long, packetcnt, 256);
int xdp_drop_tcp(struct xdp_md *ctx){
	int ipsize = 0;
	void *data_end = (void *)(long)ctx->data_end;
	void *data     = (void *)(long)ctx->data;
	struct ethhdr *eth = data;
	struct iphdr *ip;
	long *cnt;
	__u32 idx;

	ipsize = sizeof(*eth);
	ip = data + ipsize;
	ipsize += sizeof(struct iphdr);

	if (data + ipsize > data_end) {
		return XDP_DROP;
	}

	idx = ip->protocol;
	cnt = packetcnt.lookup(&idx);
	if (cnt) {
		*cnt += 1;
	}

	if (ip->protocol == IPPROTO_ICMP){
		return XDP_DROP;
	}

	return XDP_PASS;
}
