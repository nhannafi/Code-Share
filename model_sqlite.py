import sqlite3

# ---------------------------------------------------------

def createTables():
    conn = sqlite3.connect('shareCode.db')
    c = conn.cursor()

    c.execute("DROP TABLE code")
    c.execute("DROP TABLE edition")

    c.execute('''
        CREATE TABLE IF NOT EXISTS code (
            uid INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT DEFAULT 'Insert your code here ...',
            language VARCHAR(50) DEFAULT 'py',
            createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updatedAt TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS edition (
            uid INTEGER PRIMARY KEY AUTOINCREMENT,
            code_id INTEGER,
            ip VARCHAR(20),
            user_agent VARCHAR(1000),
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# ---------------------------------------------------------

def createCode():
    conn = sqlite3.connect('shareCode.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO code DEFAULT VALUES
    ''')

    uid = c.lastrowid

    conn.commit()
    conn.close()

    return uid

# ---------------------------------------------------------

def getCode(uid):
    conn = sqlite3.connect('shareCode.db')
    print(uid)
    c = conn.cursor()
    
    c.execute('''
        SELECT
            code,
            language
        FROM code
        WHERE uid = ?
    ''', uid)

    result = c.fetchone()

    conn.commit()
    conn.close()

    return result

# ---------------------------------------------------------

def getAllCode():
    conn = sqlite3.connect('shareCode.db')
    c = conn.cursor()

    c.execute('''
        SELECT
            uid,
            code,
            language
        FROM code
        ORDER BY
            updatedAt DESC,
            createdAt DESC
    ''')

    result = c.fetchall()

    conn.commit()
    conn.close()

    return result

# ---------------------------------------------------------

def updateCode(uid, code, language):
    conn = sqlite3.connect('shareCode.db')
    c = conn.cursor()

    result = c.execute('''
        UPDATE code
        SET
            code= ?,
            language = ?,
            updatedAt = CURRENT_TIMESTAMP
        WHERE uid = ?
    ''', (code, language, uid))

    conn.commit()
    conn.close()

    return result

# ---------------------------------------------------------

def createEdition(code_id, ip, user_agent):
    conn = sqlite3.connect('shareCode.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO edition(code_id, ip, user_agent)
        VALUES(?, ?, ?)
    ''', (code_id, ip, user_agent))

    uid = c.lastrowid

    conn.commit()
    conn.close()

    return uid

# ---------------------------------------------------------

def getEdition():
    conn = sqlite3.connect('shareCode.db')
    c = conn.cursor()

    c.execute('''
        SELECT code_id, ip, user_agent, date
        FROM edition
        ORDER BY date DESC
    ''')

    result = c.fetchall()

    conn.commit()
    conn.close()

    return result