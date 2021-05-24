package main

import (
	"fmt"
	"github.com/iovisor/gobpf/elf"
	"io/ioutil"
	"os"
	"os/signal"

	bpf "github.com/iovisor/gobpf/bcc"
)

/*
#cgo CFLAGS: -I/usr/include/bcc/compat
#cgo LDFLAGS: -lbcc
#include <bcc/bcc_common.h>
#include <bcc/libbpf.h>
void perf_reader_free(void *ptr);
*/
import "C"

func usage() {
	fmt.Printf("Usage: %v <ifdev>\n", os.Args[0])
	fmt.Printf("e.g.: %v eth0\n", os.Args[0])
	os.Exit(1)
}

func main() {
	source, err := ioutil.ReadFile("limit-band.c")
	if err != nil {
		fmt.Printf("Error while reading file %v", err)
	}
	var device string

	if len(os.Args) != 2 {
		usage()
	}

	device = os.Args[1]

	ret := "XDP_DROP"
	ctxtype := "xdp_md"

	module := bpf.NewModule(string(source), []string{
		"-w",
		"-DRETURNCODE=" + ret,
		"-DCTXTYPE=" + ctxtype,
	})
	defer module.Close()

	fn, err := module.Load("packet_capture", C.BPF_PROG_TYPE_XDP, 1, 65536)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to load xdp prog: %v\n", err)
		os.Exit(1)
	}

	err = module.AttachXDP(device, fn)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to attach xdp prog: %v\n", err)
		os.Exit(1)
	}

	defer func() {
		if err := module.RemoveXDP(device); err != nil {
			fmt.Fprintf(os.Stderr, "Failed to remove XDP from %s: %v\n", device, err)
		}
	}()

	fmt.Println("Dropping packets, hit CTRL+C to stop")

	sig := make(chan os.Signal, 1)
	signal.Notify(sig, os.Interrupt, os.Kill)

	xdpStatsMap := bpf.NewTable(module.TableId("xdp_stats_map"), module)
	xdpStatsMapConfig := xdpStatsMap.Config()

	pinPath := "/sys/fs/bpf/shared/xdp_stats_map"
	err = elf.PinObject(xdpStatsMapConfig["fd"].(int), pinPath)
	if err != nil{
		fmt.Fprintf(os.Stderr, "Failed to pin xdp_stats_map to %s: %v\n",pinPath, err)
	}
	defer func() {
		err = os.Remove(pinPath)
		if err != nil{
			fmt.Fprintf(os.Stderr, "Failed to delete pinned xdp_stats_map at %s: %v\n",pinPath, err)
		}
	}()

	<-sig
}
