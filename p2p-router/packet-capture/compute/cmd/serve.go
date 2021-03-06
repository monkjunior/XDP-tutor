package cmd

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/spf13/cobra"
	"github.com/vu-ngoc-son/XDP-tutor/p2p-router/packet-capture/compute/internal/calculator"
	"github.com/vu-ngoc-son/XDP-tutor/p2p-router/packet-capture/compute/internal/storage"
	"github.com/vu-ngoc-son/XDP-tutor/p2p-router/packet-capture/compute/internal/storage/peers"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

var (
	interval int64
)

// serveCmd represents the serve command
var serveCmd = &cobra.Command{
	Use:   "serve",
	Short: "Run a computing service",
	Long:  `Run a computing service which will calculate limit of all peers once per minute`,
	Run:   runServeCmd,
}

func init() {
	rootCmd.AddCommand(serveCmd)

	serveCmd.Flags().Int64Var(&interval, "interval", 60, "update db once each interval seconds")
}

func runServeCmd(serveCmd *cobra.Command, _ []string) {
	db, err := gorm.Open(sqlite.Open("/home/ted/TheFirstProject/XDP-tutor/p2p-router/packet-capture/p2p-router.db"), &gorm.Config{})
	if err != nil {
		fmt.Printf("Error while connecting to SQLite db %v", err)
		return
	}

	db.AutoMigrate(&storage.Peers{}, &storage.Limit{}, &storage.Hosts{})

	myPeers := peers.New(*db)
	myCalculator := calculator.New(*db, myPeers)

	ticker := time.NewTicker(time.Duration(interval) * time.Second)
	signals := make(chan os.Signal, 1)
	done := make(chan bool)

	signal.Notify(signals, syscall.SIGINT, syscall.SIGTERM)

	go func() {
		for {
			select {
			case <-done:
				return
			case t := <-ticker.C:
				fmt.Println(t)
				myCalculator.UpdatePeersLimit()
			}
		}
	}()

	go func() {
		sig := <-signals
		fmt.Println(sig)
		done <- true
	}()

	defer func() {
		fmt.Println("Shutting down gracefully ...")
	}()
	_ = <-done
}
