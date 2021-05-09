import peers
import socket
import sqlite3
import geoip2.database
from requests import get
from tabulate import tabulate
from math import sin, cos, sqrt, atan2, radians

def distanceFromIP(peerIP):
    hostIP = getMyPublicIP()
    with geoip2.database.Reader('../database/GeoLite2-City_20210427/GeoLite2-City.mmdb') as reader:
        peerCity = reader.city(peerIP)
        hostCity = reader.city(hostIP)
        reader.close()
    pLat = peerCity.location.latitude
    pLong = peerCity.location.longitude
    hLat = hostCity.location.latitude
    hLong = hostCity.location.longitude
    return distnaceFromCoordinate(pLat, pLong, hLat, hLong)

def distnaceFromCoordinate(pLat, pLong, hLat, hLong):
    R = 6373.0 #km

    pLat = radians(pLat)
    pLong = radians(pLong)
    hLat = radians(hLat)
    hLong = radians(hLong)

    dLong = pLong-hLong
    dLat = pLat-hLat

    a = sin(dLat / 2)**2 + cos(pLat) * cos(hLat) * sin(dLong / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

def ipInfo(peerIP):
    with geoip2.database.Reader('../database/GeoLite2-ASN_20210504/GeoLite2-ASN.mmdb') as reader:
        asn = reader.asn(peerIP)
        reader.close()

    with geoip2.database.Reader('../database/GeoLite2-Country_20210427/GeoLite2-Country.mmdb') as reader:
        country = reader.country(peerIP)
        reader.close()
    
    return asn.network, asn.autonomous_system_number, asn.autonomous_system_organization, country.country.iso_code, distanceFromIP(peerIP)

def addPeerToDB(peerIP):
    hostIP = getMyPublicIP()
    network, asn, cc, distance, isp = ipInfo(peerIP, hostIP)
    try:
        peers.addOne(peerIP, network, asn, cc, distance, isp)
    except sqlite3.OperationalError:
        peers.init()

def deletePeerData():
    try:
        tableName = "peers"
        peers.dropTable(f"{tableName}")
        print(f"delete table {tableName} successfully")
    except Exception as e:
        print(f"Exception {e}: failed to delete table {tableName}")

def getMyPublicIP():
    ip = get('https://api.ipify.org').text
    return ip


def getMyPrivateIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP