package cmd

import (
	"fmt"
	"github.com/spf13/cobra"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

// ipCmd represents the ip command
var ipCmd = &cobra.Command{
	Use:   "ip",
	Short: "Compute the limit bandwidth of a specific ip",
	Long: `This command will show you the limit bandwidth of an ip

But it will not update to the limit bandwidth database

Should implement to decide if we can update the value or not`,
	Run: runCmd,
}

func init() {
	rootCmd.AddCommand(ipCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// ipCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// ipCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}

func runCmd(cmd *cobra.Command, args []string) {
	db, err := gorm.Open(sqlite.Open("../p2p-router.db"), &gorm.Config{})
	if err != nil {
		fmt.Printf("Error while connecting to SQLite db %v", err)
		return
	}

	type Peers struct {
		Ip          string
		Network     string
		Asn         int
		Isp         string
		CountryCode string
		Distance    float32
	}
	type Host struct {
		Ip          string
		Network     string
		Asn         int
		Isp         string
		CountryCode string
		Distance    float32
	}

	var host Host
	db.Table("host").First(&host)

	fmt.Printf("%+v", host)
}
