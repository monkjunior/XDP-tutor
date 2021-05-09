import sqlite3
import geoip2
import computeLimit

dbFile = "p2p-router.db"
tableName = "bandwidth"

def init():
    conn = sqlite3.connect(f'{dbFile}')
    c = conn.cursor()

    c.execute(f"""CREATE TABLE {tableName} (
        ip TEXT,
        bandwidth REAL      
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

def isRowExisted(cursor, ip):
    cursor.execute(f"SELECT rowid FROM {tableName} WHERE ip like '{ip}'")
    data=cursor.fetchall()
    if len(data)==1:
        return True
    
    return False

def addOne(ip):
    conn = sqlite3.connect(f'{dbFile}')
    c = conn.cursor()
    limitBand = computeLimit.calLimitBand(ip)

    if not isRowExisted(c, ip):
        c.execute(f"""INSERT INTO {tableName} VALUES (
                '{ip}', {limitBand}
            )"""
        )

    commitAndClose(conn)


def commitAndClose(conn):
    conn.commit()
    conn.close()

def dropTable():
    conn = sqlite3.connect(f'{dbFile}', uri=False)
    c = conn.cursor()

    c.execute(f"DROP TABLE {tableName}")

    commitAndClose(conn)
