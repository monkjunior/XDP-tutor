import geoip2.database

with geoip2.database.Reader('./database/GeoLite2-ASN_20210504/GeoLite2-ASN.mmdb') as reader:
    response = reader.asn("104.16.37.47")
    print(response.autonomous_system_number)
# TODO: get more info about peer like country, ISP, distance