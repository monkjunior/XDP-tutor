package calculator

import (
	"fmt"
	"math"

	"github.com/vu-ngoc-son/XDP-tutor/p2p-router/packet-capture/compute/internal/storage"

	"gorm.io/gorm"
)

const (
	e      = 0.1
	e1     = 1
	alpha1 = 1000
	alpha2 = 1000
	alpha3 = 2000
	B      = 2000000
	minB   = 200
)

type ServiceCalculator struct {
	db gorm.DB
	storage.PeerService
}

func New(db gorm.DB, p storage.PeerService) ServiceCalculator {
	return ServiceCalculator{
		db,
		p,
	}
}

//UpdatePeersLimit calculate limit of all peers and update to database.
func (c ServiceCalculator) UpdatePeersLimit() {
	var peers []storage.Peers

	result := c.db.Find(&peers)
	if result.Error != nil {
		fmt.Println("Error while update peers limit", result.Error)
		return
	}

	for _, p := range peers {
		c.LimitByIP(p, true)
	}
}

//LimitByIP calculate limit bandwidth of a specific ip address
func (c ServiceCalculator) LimitByIP(p storage.Peers, updateDB bool) storage.Limit {
	var limit float64 = B
	n1, n2, n3, f1, f2, f3 := c.prepareArgs(p)

	logicalDistance := f1*math.Exp(-1/(n1+e)) + f2*math.Exp(-1/(n2+e)) + f3*math.Exp(-1/n3+e)
	limit = B / (logicalDistance + e1)

	if limit < minB {
		limit = minB
	}

	l := storage.Limit{
		Ip:        p.Ip,
		Bandwidth: limit,
	}
	if updateDB {

		result := c.db.Model(&l).Where("ip = ?", l.Ip).Updates(&l)
		if result.Error != nil {
			fmt.Println("Error while update limit by ip", result.Error)
		}
		if result.RowsAffected == 0 {
			c.db.Create(&l)
		}
	}

	fmt.Printf("%s %s: %f\n", p.CountryCode, p.Ip, limit)
	return l
}

func (c ServiceCalculator) prepareArgs(p storage.Peers) (n1, n2, n3 float64, f1, f2, f3 float64) {
	f1 = 0
	f2 = 0
	f3 = 0
	n1, n2, n3 = c.FindNearBy()
	sameASN, sameISP, sameCountry := c.CompareToHost(p)

	if !sameASN {
		f1 = alpha1
		f3 = p.Distance
	}
	if !sameISP {
		f2 = alpha2
	}

	if !sameCountry {
		f3 = f3 + alpha3
	}

	return n1, n2, n3, f1, f2, f3
}
