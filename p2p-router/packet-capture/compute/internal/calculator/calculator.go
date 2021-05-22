package calculator

import (
	"math"

	"github.com/vu-ngoc-son/XDP-tutor/p2p-router/packet-capture/compute/internal/storage"
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
	storage.PeerService
}

func New(p storage.PeerService) ServiceCalculator {
	return ServiceCalculator{
		p,
	}
}

func (c ServiceCalculator) LimitByIP(p storage.Peers) (limit float64) {
	n1, n2, n3, f1, f2, f3 := c.prepareArgs(p)

	logicalDistance := f1*math.Exp(-1/(n1+e)) + f2*math.Exp(-1/(n2+e)) + f3*math.Exp(-1/n3+e)
	limit = B / (logicalDistance + e1)

	if limit < minB {
		return minB
	}

	return limit
}

func (c ServiceCalculator) prepareArgs(p storage.Peers) (n1, n2, n3 float64, f1, f2, f3 float64) {
	f1 = 0
	f2 = 0
	f3 = 0
	n1, n2, n3 = c.FindNearBy(p)
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
