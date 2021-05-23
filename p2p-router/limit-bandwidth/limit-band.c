/* SPDX-License-Identifier: GPL-2.0 */
#include "common_kern_user.h" /* defines: struct dataRec; */

/* IP whitelist map stores a list of IPs which allowed to pass through XDP layer */
BPF_TABLE("hash", int, int, IP_whitelist, 1);

int  xdp_pass_func(struct xdp_md *ctx)
{
	return XDP_PASS;
}

int  xdp_drop_func(struct xdp_md *ctx)
{
	return XDP_DROP;
}

int  xdp_abort_func(struct xdp_md *ctx)
{
	return XDP_ABORTED;
}

int packet_capture(struct xdp_md *ctx)
{
	void *data_end = (void *)(long)ctx->data_end;
	void *data     = (void *)(long)ctx->data;
	struct dataRec *rec;
	__u32 key = XDP_PASS; /* XDP_PASS = 2 */

	/* Lookup in kernel BPF-side return pointer to actual data record */
	
	/* BPF kernel-side verifier will reject program if the NULL pointer
	 * check isn't performed here. Even-though this is a static array where
	 * we know key lookup XDP_PASS always will succeed.
	 */
	rec = xdp_stats_map.lookup(&key);
	if (!rec) {
		return XDP_ABORTED;
	}
	__u64 bytes = data_end - data; /* Calculate packet length */
	__sync_fetch_and_add(&rec->rx_packets, 1);
	__sync_fetch_and_add(&rec->rx_bytes, bytes);

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
	
	int key2 = 0;
	int *isOverThreshold;
	isOverThreshold = trigger_limit.lookup(&key2);
	if (isOverThreshold) {
		if (*isOverThreshold){
			return XDP_DROP;
		}
	}

	return XDP_PASS;
}