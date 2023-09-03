import sqlite3

db = sqlite3.connect('database.db')
sql = db.cursor()


def database_setup():
    sql.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tgId INT
    )
    """)

    sql.execute("""CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message INT
    )
    """)

    sql.execute(f'INSERT INTO messages(message) VALUES (?)', ("Ласкаво просимо :)",))
    db.commit()
    sql.close()

def get_user(user_id):
    db = sqlite3.connect('database.db')
    sql = db.cursor()
    sql.execute(f"SELECT tgId FROM users WHERE tgId = '{user_id}'")
    if sql.fetchone() is None:
        sql.execute(f'INSERT INTO users(tgId) VALUES (?)', (user_id,))
        db.commit()
        sql.close()
    else:
        sql.close()

def get_message():
    db = sqlite3.connect('database.db')
    sql = db.cursor()
    message = []
    for i in sql.execute(f"SELECT message FROM messages"):
        message += i
    sql.close()
    return message[0]

def set_message(new_text):
    db = sqlite3.connect('database.db')
    sql = db.cursor()
    sql.execute(f"UPDATE messages SET message = '{new_text}' WHERE id = 1")
    db.commit()
    sql.close()

def get_users():
    db = sqlite3.connect('database.db')
    sql = db.cursor()
    users = []
    for i in sql.execute("SELECT tgId FROM users"):
        users += i
    sql.close()
    amount_users = f'Всього користувачів🧍‍♀🧍‍♂: {len(users)}'
    return amount_users, users