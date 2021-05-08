import geoip2.database

ip = "113.22.82.9"
with geoip2.database.Reader('./database/GeoLite2-ASN_20210504/GeoLite2-ASN.mmdb') as reader:
    asn = reader.asn(ip)
    reader.close()
with geoip2.database.Reader('./database/GeoLite2-City_20210427/GeoLite2-City.mmdb') as reader:
    city = reader.city(ip)
    reader.close()
with geoip2.database.Reader('./database/GeoLite2-Country_20210427/GeoLite2-Country.mmdb') as reader:
    country = reader.country(ip)
    reader.close()
print("Network: {}\t ASN: {}\t Org: {}\t City: {}\t Country: {}".format(asn.network, asn.autonomous_system_number, asn.autonomous_system_organization, city.city.name, country.country.iso_code))
