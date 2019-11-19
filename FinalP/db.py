import sqlite3
from sqlite3 import Error

def estconn(db):
    try:
        conn = sqlite3.connect(db)
        print("Database has been connected successfully, Database Version: " + sqlite3.version)
    except Error as e:
        print(e)

    return conn


def c_table(conn, sql_table):
    try:
        c = conn.cursor()
        c.execute(sql_table)
    except Error as e:
        print(e)


def c_student(conn, cwid, sname, grade, gpa):
    student = (cwid, sname, grade, gpa)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO students(cwid,sname,grade,gpa) VALUES(?,?,?,?)", student)
    return cur.lastrowid

def c_enroll(conn, cwid, cid, denroll, grade):
    studentenroll = (cwid, cid, denroll, grade)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO enroll(cwid,cid,denroll,grade) VALUES(?,?,?,?)", studentenroll)
    return cur.lastrowid

def c_courses(conn, cid, cname, credits, preq):
    course = (cid, cname, credits, preq)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO courses(cid,cname,credits,preq) VALUES(?,?,?,?)", course)
    return cur.lastrowid

def checkdb(conn, cwid):
    cur = conn.cursor()
    cur.execute("SELECT cwid FROM students WHERE cwid=?", (cwid,))
    records = cur.fetchall()
    if not records:
        return False
    else:
        return True


def cwidinp():
    try:
        cwid = int(input("Student ID: "))
        return cwid
    except ValueError:
        print("Not a valid Student ID, please try again.")
        cwidinp()

def cline(con):
    print("\nWelcome, please type in a command or type commands for help!")
    try:
        inp = str(input("Please type in a command: "))
        for i in range(len(inp)):
            if inp[i].isdigit() == True:
                print("\nInteger values are not valid commands, try again.")
                cline(con)

        if inp == 'commands':
            print("L: Lists all Courses")
            cline(con)
        elif not inp.strip():
            print("Not a valid command, try again.")
            cline(con)
        elif inp == 'L':
            list(con)
            cline(con)
        ## elif command: here's where you put the next command
    except ValueError:
        print("Not a valid command, try again.")
        cline(con)

def list(con):
    cur = con.cursor()
    cur.execute("SELECT * FROM courses")
    courserecord = cur.fetchall()
    for all in courserecord:
        print(all)

def main():
        db = r'fdb.db'
        atmpconn = estconn(db)

        sqlc_students = """ CREATE TABLE IF NOT EXISTS students (
                                               cwid integer PRIMARY KEY,
                                               sname text NOT NULL,
                                               grade text NOT NULL,
                                               gpa double NOT NULL
                                           ); """

        sqlc_enroll = """CREATE TABLE IF NOT EXISTS enroll (
                                           cwid integer,
                                           cid integer,
                                           denroll text,
                                           grade text,
                                           FOREIGN KEY (cwid) REFERENCES students (cwid)
                                       );"""

        sqlc_courses = """CREATE TABLE IF NOT EXISTS courses (
                                                   cid integer PRIMARY KEY,
                                                   cname text NOT NULL,
                                                   credits integer NOT NULL,
                                                   preq text
                                               );"""

        if atmpconn is not None:
            c_table(atmpconn, sqlc_students)
            c_table(atmpconn, sqlc_enroll)
            c_table(atmpconn, sqlc_courses)

        else:
            print("Database Connection Failed.")

        with atmpconn:
            c_student(atmpconn, "21612390", "David Sapida", "Senior", "3.5")
            c_student(atmpconn, "21612391", "Andre Stillo", "Senior", "3.7")
            c_student(atmpconn, "21612392", "John Jingleheimer", "Senior", "3.0")
            c_student(atmpconn, "21612393", "James WhoDied", "Senior", "1.2")
            c_student(atmpconn, "21612394", "Totina HotPizzaRolls", "Senior", "4.0")

            c_courses(atmpconn, "420", "Cooking Totino's Pizza Rolls 101", "3", "N/A")
            c_courses(atmpconn, "500", "How to not be a failure in life 101", "3", "N/A")
            c_courses(atmpconn, "012", "How to prevent James from Dying 101", "3", "N/A")
            c_courses(atmpconn, "069", "How to do the thing 101", "3", "N/A")
            c_courses(atmpconn, "777", "How to lose your money in Vegas", "3", "N/A")

            c_enroll(atmpconn, "21612390", "420", "4/20/2020", "A+")
            c_enroll(atmpconn, "21612390", "500", "4/01/2020", "B+")
            c_enroll(atmpconn, "21612390", "012", "3/16/2020", "F")
            c_enroll(atmpconn, "21612390", "069", "3/20/2020", "B")

            c_enroll(atmpconn, "21612391", "420", "4/20/2020", "A+")
            c_enroll(atmpconn, "21612391", "500", "4/10/2020", "B-")
            c_enroll(atmpconn, "21612391", "012", "4/15/2020", "C+")

            c_enroll(atmpconn, "21612392", "500", "1/11/2020", "A-")
            c_enroll(atmpconn, "21612392", "012", "3/22/2020", "B")
            c_enroll(atmpconn, "21612392", "069", "4/23/2020", "D")

            c_enroll(atmpconn, "21612393", "420", "2/03/2020", "C-")
            c_enroll(atmpconn, "21612393", "777", "2/01/2020", "D+")

            c_enroll(atmpconn, "21612394", "420", "4/20/2020", "A+")

        check = checkdb(atmpconn, cwidinp())
        if check == True:
            cline(atmpconn)
        else:
            print("There are no records for this CWID in our Database, please type -1 to sign up as a new Student, if your CWID exists please try again.")
            checkdb(atmpconn, cwidinp())


if __name__ == "__main__":
        main()
