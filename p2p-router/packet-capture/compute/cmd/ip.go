package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
	"github.com/vu-ngoc-son/XDP-tutor/p2p-router/packet-capture/compute/internal/calculator"
	"github.com/vu-ngoc-son/XDP-tutor/p2p-router/packet-capture/compute/internal/storage/peers"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

var limitCmd = &cobra.Command{
	Use:   "limit",
	Short: "Calculate limit from ip",

	Run: runCmd,
}

func init() {
	rootCmd.AddCommand(limitCmd)

	limitCmd.Flags().String("ip", "", "ip address that you want to calculate limit")
}

func runCmd(limitCmd *cobra.Command, _ []string) {
	db, err := gorm.Open(sqlite.Open("../p2p-router.db"), &gorm.Config{})
	if err != nil {
		fmt.Printf("Error while connecting to SQLite db %v", err)
		return
	}

	myPeers := peers.New(*db)

	myCalculator := calculator.New(myPeers)

	println(int64(myCalculator.LimitByIP(myPeers.FindByIP(limitCmd.Flag("ip").Value.String()))))
}
