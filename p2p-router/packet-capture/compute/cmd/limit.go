package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
	"github.com/vu-ngoc-son/XDP-tutor/p2p-router/packet-capture/compute/internal/calculator"
	"github.com/vu-ngoc-son/XDP-tutor/p2p-router/packet-capture/compute/internal/storage"
	"github.com/vu-ngoc-son/XDP-tutor/p2p-router/packet-capture/compute/internal/storage/peers"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

var (
	peerAddress string
	updateToDB  bool
)

var limitCmd = &cobra.Command{
	Use:   "limit",
	Short: "Calculate limit from ip",

	Run: runLimitCmd,
}

func init() {
	rootCmd.AddCommand(limitCmd)

	limitCmd.Flags().StringVar(&peerAddress, "ip", "", "ip address that you want to calculate limit")
	limitCmd.Flags().BoolVar(&updateToDB, "update-to-db", false, "update result to db or not")
}

func runLimitCmd(limitCmd *cobra.Command, _ []string) {
	db, err := gorm.Open(sqlite.Open("../p2p-router.db"), &gorm.Config{})
	if err != nil {
		fmt.Printf("Error while connecting to SQLite db %v", err)
		return
	}

	err = db.AutoMigrate(&storage.Peers{}, &storage.Limit{})
	if err != nil {
		fmt.Printf("Error while migrating db %v", err)
		return
	}

	myPeers := peers.New(*db)
	myCalculator := calculator.New(*db, myPeers)

	myCalculator.LimitByIP(myPeers.FindByIP(peerAddress), bool(updateToDB))
}
