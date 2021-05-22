package calculator

import (
	"github.com/vu-ngoc-son/XDP-tutor/p2p-router/packet-capture/compute/internal/storage"
	"github.com/vu-ngoc-son/XDP-tutor/p2p-router/packet-capture/compute/internal/storage/peers"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"testing"
)

func BenchmarkServiceCalculator_UpdatePeersLimit(b *testing.B) {
	for i := 0; i < 1; i++ {
		db, err := gorm.Open(sqlite.Open("/home/ted/TheFirstProject/XDP-tutor/p2p-router/packet-capture/p2p-router.db"), &gorm.Config{})
		if err != nil {
			b.Errorf("%v", err)
			return
		}
		err = db.AutoMigrate(&storage.Peers{}, &storage.Limit{}, &storage.Hosts{})
		if err != nil {
			b.Errorf("%v", err)
			return
		}
		myPeers := peers.New(*db)
		myCalculator := New(*db, myPeers)
		myCalculator.UpdatePeersLimit()
	}
}
