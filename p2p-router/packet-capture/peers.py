import sqlite3

dbFile = "p2p-router.db"
tableName = "peers"

def init():
    conn = sqlite3.connect(f'{dbFile}')
    c = conn.cursor()

    c.execute(f"""CREATE TABLE {tableName} (
        ip TEXT,
        network TEXT,
        asn INTEGER,
        isp TEXT,
        country_code TEXT,
        distance REAL
    )
    """)

    commitAndClose(conn)

# Query the database and return all records 
def showAll():
    conn = sqlite3.connect(f'{dbFile}')
    c = conn.cursor()

    c.execute(f"SELECT rowid, * FROM {tableName}")
    peers = c.fetchall()

    for p in peers:
        print(p)
    
    commitAndClose(conn)

def getASN(ip):
    conn = sqlite3.connect(f'{dbFile}')
    c = conn.cursor()

    c.execute(f"SELECT asn FROM {tableName} WHERE ip like {ip}")
    data = c.fetchall()

    commitAndClose(conn)

    return data[0][0]

def getCountry(ip):
    conn = sqlite3.connect(f'{dbFile}')
    c = conn.cursor()

    c.execute(f"SELECT country_code FROM {tableName} WHERE ip like {ip}")
    data = c.fetchall()

    commitAndClose(conn)

    return data[0][0]

def getDistance(ip):
    conn = sqlite3.connect(f'{dbFile}')
    c = conn.cursor()

    c.execute(f"SELECT distance FROM {tableName} WHERE ip like {ip}")
    data = c.fetchall()

    commitAndClose(conn)

    return data[0][0]

def isRowExisted(cursor, ip):
    cursor.execute(f"SELECT rowid FROM {tableName} WHERE ip like '{ip}'")
    data=cursor.fetchall()
    if len(data)==1:
        return True
    
    return False

def addOne(ip, network, asn, isp, cc, distance):
    conn = sqlite3.connect(f'{dbFile}')
    c = conn.cursor()

    if not isRowExisted(c, ip):
        c.execute(f"""INSERT INTO {tableName} VALUES (
                '{ip}', '{network}', '{asn}', '{isp}', '{cc}', '{distance}'
            )"""
        )

    commitAndClose(conn)

def sameASNPeers(hostASN):
    conn = sqlite3.connect(f'{dbFile}')
    c = conn.cursor()

    c.execute(f"""SELECT COUNT(asn) from {tableName}
    WHERE asn = {hostASN}
    GROUP BY asn
    """)

    result = c.fetchall()
    commitAndClose(conn)

    return result[0][0]

def sameISPPeers(hostISP):
    conn = sqlite3.connect(f'{dbFile}')
    c = conn.cursor()

    c.execute(f"""SELECT COUNT(asn) from {tableName}
    WHERE isp like '{hostISP}'
    GROUP BY isp
    """)

    result = c.fetchall()
    commitAndClose(conn)

    return result[0][0]

def sameCountryPeers(hostCountry):
    conn = sqlite3.connect(f'{dbFile}')
    c = conn.cursor()

    c.execute(f"""SELECT COUNT(asn) from {tableName}
    WHERE country_code like '{hostCountry}'
    GROUP BY country_code
    """)

    result = c.fetchall()
    commitAndClose(conn)

    return result[0][0]

def commitAndClose(conn):
    conn.commit()
    conn.close()

def dropTable(table_name):
    conn = sqlite3.connect(f'{dbFile}', uri=False)
    c = conn.cursor()

    c.execute(f"DROP TABLE {table_name}")

    commitAndClose(conn)
