import sqlite3
from sqlite3 import Error
from datetime import date
import re


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

def c_enroll(conn, eid, cwid, cid, denroll, grade):
    studentenroll = (eid, cwid, cid, denroll, grade)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO enroll(eid,cwid,cid,denroll,grade) VALUES(?,?,?,?,?)", studentenroll)
    return cur.lastrowid

def c_courses(conn, cid, cname, credits, preq):
    course = (cid, cname, credits, preq)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO courses(cid,cname,credits,preq) VALUES(?,?,?,?)", course)
    return cur.lastrowid

def d_enroll(conn, cwid, cid):
    cur = conn.cursor()
    cur.execute("SELECT E.cwid, E.cid, C.cname FROM enroll E, courses C WHERE E.cid = C.cid AND E.cwid=? AND E.cid=?", (cwid, str(cid),))
    get = cur.fetchall()
    print(get)
    c = str(input("Are you sure you want to withdraw from this class? Please type Y or N: "))
    if c == 'Y':
        with conn:
            cur.execute("DELETE FROM enroll WHERE cwid=? AND cid=?", (cwid, str(cid),))
            print("Withdrawl Successful")
    elif c == 'N':
        print("Withdrawl Failed.")
        cline(conn, cwid)
    else:
        print("Invalid option, please try again.")
        d_enroll(conn, cwid, cid)

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

def cline(con, cwid):
    cur = con.cursor()
    cur.execute("SELECT cwid FROM students WHERE cwid=?", (cwid,))
    getcwid = cur.fetchall()
    s = str(getcwid)
    cwid = re.sub('[^A-Za-z0-9]+', '', s)
    print("\nWelcome, please type in a command or type commands for help!")
    print("CWID: " + cwid)
    try:
        while(True):
            inp = str(input("Please type in a command: "))
            for i in range(len(inp)):
                if inp[i].isdigit() == True:
                    print("\nInteger values are not valid commands, try again.")
                    cline(con, cwid)

            if inp == 'commands':
                print("L: Lists all Courses")
                print("E: Enrolls Student(s) into a Course")
                print("W: Withdraw Class")
                print("S: Search for a Course")
                print("M: View your Classes")
                print("X: Exit")
                cline(con, cwid)
            elif not inp.strip():
                print("Not a valid command, try again.")
                cline(con, cwid)
            elif inp == 'L':
                list(con)
                cline(con, cwid)
            elif inp == 'E':
                eclass(con, cwid)
            elif inp == 'W':
                wclass(con, cwid)
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

def eclass(conn, cwid):
    try:
     cid = int(input("Please enter a Course ID: "))
    except ValueError as e:
        print("Invalid Course ID, please try again.")

    cur = conn.cursor()
    cur.execute("SELECT cid FROM courses WHERE cid=?", (cid,))
    records = cur.fetchall()
    if not records:
        print("Course does not exist, please try again.")
        eclass(conn, cwid)
    else:
        cur.execute("SELECT cid, cwid FROM enroll WHERE cwid=? AND cid=?", (cwid, str(cid)))
        cpis = cur.fetchall()
        cur.execute("SELECT eid FROM enroll ORDER BY eid DESC LIMIT 1;")
        leid = str(cur.fetchall())
        eid = int(re.sub('[^A-Za-z0-9]+', '', leid)) + 1
        if not cpis:
            with conn:
                c_enroll(conn, str(eid), cwid, str(cid), str(date.today()), "N/A")
            print("Enrollment Complete!")
            cline(conn, cwid)
        else:
            print("You are currently registered for this class!")
            eclass(conn, cwid)

def wclass(conn, cwid):
    try:
        cid = int(input("Please enter a Course ID: "))
    except ValueError as e:
        print("Invalid Course ID, please try again.")

    cur = conn.cursor()
    cur.execute("SELECT cid FROM courses WHERE cid=?", (cid,))
    records = cur.fetchall()
    if not records:
        print("Course does not exist, please try again.")
        wclass(conn, cwid)
    else:
        cur.execute("SELECT cid, cwid FROM enroll WHERE cwid=? AND cid=?", (cwid, str(cid)))
        cpis = cur.fetchall()
        if not cpis:
            print("You are not registered for this class!")
            wclass(conn, cwid)
        else:
            with conn:
                d_enroll(conn, cwid, cid)

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
                                           eid integer PRIMARY KEY,
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
            existing_connection = True
            cur = atmpconn.cursor()
            cur.execute("SELECT * FROM enroll")
            get = cur.fetchall()
            if not get:
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


                c_enroll(atmpconn,"0", "21612390", "420", "4/20/2020", "A+")
                c_enroll(atmpconn,"1", "21612390", "500", "4/01/2020", "B+")
                c_enroll(atmpconn,"2", "21612390", "012", "3/16/2020", "F")
                c_enroll(atmpconn,"3", "21612390", "069", "3/20/2020", "B")

                c_enroll(atmpconn,"4", "21612391", "420", "4/20/2020", "A+")
                c_enroll(atmpconn,"5", "21612391", "500", "4/10/2020", "B-")
                c_enroll(atmpconn,"6", "21612391", "012", "4/15/2020", "C+")

                c_enroll(atmpconn,"7", "21612392", "500", "1/11/2020", "A-")
                c_enroll(atmpconn,"8", "21612392", "012", "3/22/2020", "B")
                c_enroll(atmpconn,"9", "21612392", "069", "4/23/2020", "D")

                c_enroll(atmpconn,"10", "21612393", "420", "2/03/2020", "C-")
                c_enroll(atmpconn,"11", "21612393", "777", "2/01/2020", "D+")

                c_enroll(atmpconn,"12", "21612394", "420", "4/20/2020", "A+")

        while(existing_connection == True):
            currentcwid = cwidinp()
            check = checkdb(atmpconn, currentcwid)
            if currentcwid != -1 and check == True:
                cline(atmpconn, currentcwid)
            elif currentcwid == -1:
                print("Use the new student function")
                #Create new student function
            else:
                print("There are no records for this CWID in our Database, please type -1 to sign up as a new Student, if your CWID exists please try again.")

if __name__ == "__main__":
        main()
