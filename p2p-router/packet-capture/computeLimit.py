import bandwidth
import imap
import math
import peers
from tabulate import tabulate

e = 0.1
e1 = 1
alpha1 = 1000
alpha2 = 1000
alpha3 = 2000
B = 2000000
minB = 200

def nearByPeers(asn, isp, countryCode):
    _, asn, isp, countryCode, _ = imap.ipInfo(imap.getMyPublicIP())
    return peers.sameASNPeers(asn), peers.sameISPPeers(isp), peers.sameCountryPeers(countryCode)

def printNearByPeers(asn, isp, countryCode):
    _, asn, isp, countryCode, _ = imap.ipInfo(imap.getMyPublicIP())
    print(tabulate([[peers.sameASNPeers(asn), peers.sameISPPeers(isp), peers.sameCountryPeers(countryCode)]], headers=['Same ASN', 'Same ISP', 'Same Country']))

def calLimitBand(peerIP):
    network, asn, isp, countryCode, distance = imap.ipInfo(imap.getMyPublicIP())
    n1, n2, n3 = nearByPeers(asn, isp, countryCode)
    _, pASN, pISP, pCC, pDist = imap.ipInfo(peerIP)
    f1 = 0 if pASN == asn else alpha1
    f2 = 0 if pISP == isp else alpha2
    f3 = 0 
    if pASN != asn:
        if pCC == countryCode:
            f3 = pDist
        else:
            f3 = alpha3 + pDist
    logicalDistance = f1*math.exp(-1/(n1 + e)) + f2*math.exp(-1/(n1 + e)) + f3*math.exp(-1/(n3 + e))
    bandLimit = B/(logicalDistance + e1)
    # print(tabulate([[n1, n2, n3, f1, f2, f3, pDist, logicalDistance, bandLimit]], headers=['n1', 'n2', 'n3', 'f1', 'f2', 'f3', 'pD', 'lD', 'bw']))
    return bandLimit

