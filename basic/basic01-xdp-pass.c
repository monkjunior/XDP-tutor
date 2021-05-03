/* SPDX-License-Identifier: GPL-2.0 */
// #include <linux/bpf.h>
// #include <bpf/bpf_helpers.h>
// Because we are using BCC for compile and load eBPF program
// So we dont need helper header file

#include "common_kern_user.h" /* defines: struct datarec; */

// struct bpf_map_def SEC("maps") xdp_stats_map = {
// 	.type        = BPF_MAP_TYPE_ARRAY,
// 	.key_size    = sizeof(__u32),
// 	.value_size  = sizeof(struct datarec),
// 	.max_entries = XDP_ACTION_MAX,
// };

// Syntax: BPF_TABLE(_table_type, _key_type, _leaf_type, _name, _max_entries)
BPF_TABLE("percpu_array", __u32, struct datarec, xdp_stats_map, XDP_ACTION_MAX);

// SEC("xdp")
int  xdp_prog_pass(struct xdp_md *ctx)
{
	return XDP_PASS;
}

// SEC("xdp")
int  xdp_prog_drop(struct xdp_md *ctx)
{
	return XDP_DROP;
}

// SEC("xdp")
int  xdp_prog_aborted(struct xdp_md *ctx)
{
	return XDP_ABORTED;
}

// SEC("xdp")
int  xdp_count_func(struct xdp_md *ctx)
{
	void *data_end = (void *)(long)ctx->data_end;
	void *data     = (void *)(long)ctx->data;
	struct datarec *rec;
	__u32 key = XDP_PASS; /* XDP_PASS = 2 */

	/* Lookup in kernel BPF-side return pointer to actual data record */
	
	/* BPF kernel-side verifier will reject program if the NULL pointer
	 * check isn't performed here. Even-though this is a static array where
	 * we know key lookup XDP_PASS always will succeed.
	 */
	rec = xdp_stats_map.lookup(&key);
	if (rec) {
		__u64 bytes = data_end - data; /* Calculate packet length */
		__sync_fetch_and_add(&rec->rx_packets, 1);
		__sync_fetch_and_add(&rec->rx_bytes, bytes);
		return XDP_PASS;
	}

	/* Multiple CPUs can access data record. Thus, the accounting needs to
	 * use an atomic operation.
	 */
	// lock_xadd(&rec->rx_packets, 1);
        /* Assignment#1: Add byte counters
         * - Hint look at struct xdp_md *ctx (copied below)
         *
         * Assignment#3: Avoid the atomic operation
         * - Hint there is a map type named BPF_MAP_TYPE_PERCPU_ARRAY
         */

	return XDP_ABORTED;
}


// char _license[] SEC("license") = "GPL";