import sqlite3
from sqlite3 import Error

def main():
        try:
                id = int(input("Student ID: "))
        except ValueError:
                print("Not a valid Student ID, please try again.")
                main()

if __name__ == "__main__":
        main()

def estconn(db):
        try:
            conn = sqlite3.connect(db)
            print(sqlite3.version)
        except Error as e:
            print(e)

        return conn

def c_table(conn, sql_table):
        try:
            c = conn.cursor()
            c.execute(sql_table)
        except Error as e:
            print(e)

def c_obj(conn, obj):

    sql = ''' INSERT INTO ''' + obj + '''(name,begin_date,end_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid
