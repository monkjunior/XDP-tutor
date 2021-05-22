package storage

type Hosts struct {
	Ip          string
	Network     string
	Asn         int
	Isp         string
	CountryCode string
	Distance    float64
}

type Peers struct {
	Ip          string
	Network     string
	Asn         int
	Isp         string
	CountryCode string
	Distance    float64
}

type Limit struct {
	Ip        string
	Bandwidth float64
}

type PeerService interface {
	FindByIP(IP string) Peers
	/*
		n1: number of peers which have the same ASN
		n2: number of peers which have the same ISP
		n3: number of peers which have the same Country Code
	*/
	FindNearBy() (n1, n2, n3 float64)
	/*
		b1: equal true if peer is in the same ASN with host
		b2: equal true if peer is in the same ISP with host
		b3: equal true if peer is in the same Country with host
	*/
	CompareToHost(peer Peers) (b1, b2, b3 bool)
}
