import imap
import sqlite3

dbFile = "p2p-router.db"
tableName = "host"

def commitAndClose(conn):
    conn.commit()
    conn.close()

def init():
    conn = sqlite3.connect(f'file:{dbFile}?mode=rw', uri=True)
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

    ip = imap.getMyPublicIP()
    network, asn, isp, cc, distance = imap.ipInfo(ip)

    c.execute(f"""INSERT INTO {tableName} VALUES (
        '{ip}', '{network}', '{asn}', '{isp}', '{cc}', '{distance}'
    )
    """)

    commitAndClose(conn)

def dropTable():
    conn = sqlite3.connect(f'{dbFile}', uri=False)
    c = conn.cursor()

    c.execute(f"DROP TABLE {tableName}")

    commitAndClose(conn)
    print(f"delete table {tableName} successfully")