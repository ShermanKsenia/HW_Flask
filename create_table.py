import sqlite3

con = sqlite3.connect('survey.db')
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question text
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    age int, gender text, zodiac_sign text, 
    languages text, student text
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS answers (
    id,
    q1 int,
    q2 int,
    q3 int
)
""")
con.commit()

questions = ['Ежёик научился дышать попой, сел и задохнулся',
            'Над домом престарелых прошёл ураган - бабки на ветер',
            'Мне так жаль календарь - его дни сочтены'
            ]

for q in questions:
    cur.execute('INSERT INTO questions (question) VALUES (?)', (q, ))

con.commit()

