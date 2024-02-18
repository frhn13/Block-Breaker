import sqlite3


def tables_setup():
    conn_users = sqlite3.connect("tables/users.db")
    conn_scores = sqlite3.connect("tables/scores.db")

    c_users = conn_users.cursor()
    c_scores = conn_scores.cursor()

    c_users.execute("""CREATE TABLE if not exists users
                    (username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL)""")
    conn_users.commit()

    c_scores.execute("""CREATE TABLE if not exists scores
                        (score INTEGER NOT NULL,
                        time TEXT NOT NULL,
                        username TEXT NOT NULL)""")
    conn_scores.commit()

    conn_users.close()
    conn_scores.close()
