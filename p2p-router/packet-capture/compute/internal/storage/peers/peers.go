package peers

import (
	"github.com/vu-ngoc-son/XDP-tutor/p2p-router/packet-capture/compute/internal/storage"
	"github.com/vu-ngoc-son/XDP-tutor/p2p-router/packet-capture/compute/internal/storage/host"

	"gorm.io/gorm"
)

type peer struct {
	Host storage.Peers
	db   gorm.DB
}

func New(db gorm.DB) peer {
	return peer{
		host.New(db),
		db,
	}
}

func (p peer) FindByIP(ip string) (result storage.Peers) {
	p.db.Table("peers").Where("ip = ?", ip).First(&result)
	return result
}

/*
	n1: number of peers which have the same ASN
	n2: number of peers which have the same ISP
	n3: number of peers which have the same Country Code
*/
func (p peer) FindNearBy(peerInfo storage.Peers) (n1, n2, n3 float64) {
	var r1, r2, r3 int64
	p.db.Table("peers").Where("asn = ?", peerInfo.Asn).Count(&r1)
	p.db.Table("peers").Where("isp = ?", peerInfo.Isp).Count(&r2)
	p.db.Table("peers").Where("country_code = ?", peerInfo.CountryCode).Count(&r3)
	return float64(r1), float64(r2), float64(r3)
}

/*
	b1: equal true if peer is in the same ASN with host
	b2: equal true if peer is in the same ISP with host
	b3: equal true if peer is in the same Country with host
*/
func (p peer) CompareToHost(peerInfo storage.Peers) (b1, b2, b3 bool) {
	b1 = peerInfo.Asn == p.Host.Asn
	b2 = peerInfo.Isp == p.Host.Isp
	b3 = peerInfo.CountryCode == p.Host.CountryCode
	return b1, b2, b3
}
