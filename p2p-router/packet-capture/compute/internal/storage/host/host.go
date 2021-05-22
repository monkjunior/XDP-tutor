package host

import (
	"fmt"
	"gorm.io/gorm"

	"github.com/vu-ngoc-son/XDP-tutor/p2p-router/packet-capture/compute/internal/storage"
)

func New(db gorm.DB) (myHost storage.Hosts) {
	result := db.Table("hosts").First(&myHost)
	if result.Error != nil {
		fmt.Printf("Error while init host %v\n", result.Error)
		return
	}
	return myHost
}
