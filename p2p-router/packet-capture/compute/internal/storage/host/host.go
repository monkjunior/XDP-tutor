package host

import (
	"gorm.io/gorm"

	"github.com/vu-ngoc-son/XDP-tutor/p2p-router/packet-capture/compute/internal/storage"
)

func New(db gorm.DB) (result storage.Peers) {
	db.Table("host").First(&result)
	return result
}
