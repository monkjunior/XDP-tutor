/* SPDX-License-Identifier: GPL-2.0 */
#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/in.h>
#include <linux/ip.h>

#define IPV4_FAMILY 1
struct ip_key {
	uint32_t s_v4_addr;
	uint32_t d_v4_addr;
	__u8 family;
};

BPF_TABLE("hash", struct ip_key, long, counters, 100);
int xdp_ip_counter(struct xdp_md *ctx){
	struct ip_key key = {};
	long default_value = 0;
	long *value;
	

	int ipsize = 0;
	void *data_end = (void *)(long)ctx->data_end;
	void *data     = (void *)(long)ctx->data;
	struct ethhdr *eth = data;
	struct iphdr *ip;

	ipsize = sizeof(*eth);
	ip = data + ipsize;
	ipsize += sizeof(struct iphdr);

	if (data + ipsize > data_end) {
		return XDP_DROP;
	}

	key.family = ip->protocol;
	key.s_v4_addr = bpf_ntohl(ip->saddr);
	key.d_v4_addr = bpf_ntohl(ip->daddr);
	value = counters.lookup_or_try_init(&key, &default_value);
	if (value) {
		*value += 1;
		return XDP_PASS;
	}

	return XDP_DROP;
}
