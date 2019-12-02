import sqlite3
from sqlite3 import Error
from datetime import date
from random import randint
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
    if c.lower() == 'y':
        with conn:
            cur.execute("DELETE FROM enroll WHERE cwid=? AND cid=?", (cwid, str(cid),))
            cur.close()
            print("Withdrawal Successful")
    elif c.lower() == 'n':
        print("Withdrawal Failed.")
        cur.close()
        cline(conn, cwid)
    else:
        print("Invalid option, please try again.")
        cur.close()
        d_enroll(conn, cwid, cid)

def checkdb(conn, cwid):
    cur = conn.cursor()
    cur.execute("SELECT cwid FROM students WHERE cwid=?", (cwid,))
    records = cur.fetchall()
    cur.close()
    if not records:
        return False
    else:
        return True


def cwidinp():
    while (True):
        try:
            cwid = str(input("Student ID: "))
            return cwid
        except ValueError:
            print("Not a valid Student ID, please try again.")

def cwidgen(con):
    while True:
        gcwid = randint(1000000, 9999999)
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM students WHERE cwid=? GROUP BY cwid", (gcwid,))
        exist = cur.fetchone()
        if exist is None:
            print("cwid generated! Your cwid is: " + str(gcwid) + ".")
            cur.close()
            return gcwid

def gpainp():
    while (True):
        try:
            gpa = float(input("GPA: "))
            return gpa
        except ValueError:
            print("Not a valid GPA value, please try again.")

def n_student(con):
    while True:
        ncwid = cwidgen(con)
        nsname = str(input("Student name: "))
        ngrade = str(input("Grade level: "))
        ngpa = gpainp()
        print("\nYour information is:\ncwid: " + str(ncwid) + "\nname: " + nsname + "\ngrade: " + ngrade + "\nGPA: " + str(ngpa))
        c = str(input("Is this correct? Please type Y or N: "))
        if c.lower() == 'y':
            c_student(con, ncwid, nsname, ngrade, ngpa)
            print("You have been registered in the database! Log in to enroll in a course.")
            login(con)
        elif c.lower() == 'n':
            print("Enter -1 to re-enter your information.")
            login(con)
        else:
            print("Invalid option, enter -1 to re-enter your information.")
            login(con)

def login(con):
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

    if con is not None:
        c_table(con, sqlc_students)
        c_table(con, sqlc_enroll)
        c_table(con, sqlc_courses)
    else:
        print("Database Connection Failed.")

    with con:
        existing_connection = True
        cur = con.cursor()
        cur.execute("SELECT * FROM enroll")
        get = cur.fetchall()
        if not get:
            c_student(con, "21612390", "David Sapida", "Senior", "3.5")
            c_student(con, "21612391", "Andre Stillo", "Senior", "3.7")
            c_student(con, "21612392", "John Jingleheimer", "Senior", "3.0")
            c_student(con, "21612393", "James WhoDied", "Senior", "1.2")
            c_student(con, "21612394", "Totina HotPizzaRolls", "Senior", "4.0")

            c_courses(con, "420", "Cooking Totino's Pizza Rolls 101", "3", "N/A")
            c_courses(con, "500", "How to not be a failure in life 101", "3", "N/A")
            c_courses(con, "012", "How to prevent James from Dying 101", "3", "N/A")
            c_courses(con, "069", "How to do the thing 101", "3", "N/A")
            c_courses(con, "777", "How to lose your money in Vegas", "3", "N/A")


            c_enroll(con,"0", "21612390", "420", "4-20-2020", "A+")
            c_enroll(con,"1", "21612390", "500", "4-01-2020", "B+")
            c_enroll(con,"2", "21612390", "012", "3-16-2020", "F")
            c_enroll(con,"3", "21612390", "069", "3-20-2020", "B")

            c_enroll(con,"4", "21612391", "420", "4-20-2020", "A+")
            c_enroll(con,"5", "21612391", "500", "4-10-2020", "B-")
            c_enroll(con,"6", "21612391", "012", "4-15-2020", "C+")

            c_enroll(con,"7", "21612392", "500", "1-11-2020", "A-")
            c_enroll(con,"8", "21612392", "012", "3-22-2020", "B")
            c_enroll(con,"9", "21612392", "069", "4-23-2020", "D")

            c_enroll(con,"10", "21612393", "420", "2-03-2020", "C-")
            c_enroll(con,"11", "21612393", "777", "2-01-2020", "D+")

            c_enroll(con,"12", "21612394", "420", "4-20-2020", "A+")
        cur.close()

    while(existing_connection == True):
        print("\nEnter your student ID or enter -1 to register as a new student.")
        currentcwid = cwidinp()
        check = checkdb(con, currentcwid)
        if currentcwid != -1 and check == True:
            welcome(con, currentcwid)
        elif currentcwid == -1:
            print("Entering new student into the database...")
            n_student(con)
        else:
           print("There are no records for this CWID in our Database, please type -1 to sign up as a new Student, if your CWID exists please try again.")
    
def welcome(con, cwid):
    cur = con.cursor()
    cur.execute("SELECT cwid FROM students WHERE cwid=?", (cwid,))
    getcwid = cur.fetchall()
    s = str(getcwid)
    cwid = re.sub('[^A-Za-z0-9]+', '', s)
    print("\nWelcome, please type in a command or type commands for help!")
    print("CWID: " + cwid)
    cur.close()
    cline(con, cwid)

         
def cline(con, cwid):
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
            print("-: Log Out")
        elif not inp.strip():
            print("Not a valid command, try again.")
        elif inp.lower() == 'l':
            list(con)
        elif inp.lower() == 'e':
            eclass(con, cwid)
        elif inp.lower() == 'w':
            wclass(con, cwid)
        elif inp.lower() == 's':
            sclass(con)
        elif inp.lower() == 'm':
            mclass(con, cwid)
        elif inp.lower() == 'x':
            exitapp(con)
        elif inp == '-': #function i added to return to the login
            login(con)
        else:
            print("Not a valid command, try again.")
        cline(con, cwid)

def list(con):
    cur = con.cursor()
    cur.execute("SELECT * FROM courses")
    courserecord = cur.fetchall()
    cur.close()
    for all in courserecord:
        print(all)

def eclass(conn, cwid):
    try:
        gcid = int(input("Please enter a Course ID: "))
    except ValueError:
        print("Invalid Course ID, please try again.")
        eclass(conn, cwid)
    cur = conn.cursor()
    cur.execute("SELECT cid FROM courses WHERE cid=?", (gcid,))
    records = cur.fetchall()
    if not records:
        print("Course does not exist, please try again.")
        cur.close()
        eclass(conn, cwid)
    else:
        cur.execute("SELECT cid, cwid FROM enroll WHERE cwid=? AND cid=?", (cwid, str(gcid)))
        cpis = cur.fetchall()
        cur.execute("SELECT eid FROM enroll ORDER BY eid DESC LIMIT 1;")
        leid = str(cur.fetchall())
        eid = int(re.sub('[^A-Za-z0-9]+', '', leid)) + 1
        if not cpis:
            with conn:
                c_enroll(conn, str(eid), cwid, str(gcid), str(date.today()), "N/A")
                cur.close()
                print("Enrollment Complete!")
        else:
            print("You are currently registered for this class!")
            cur.close()
            eclass(conn, cwid)

def wclass(conn, cwid):
    try:
       gcid = int(input("Please enter a Course ID: "))
    except ValueError:
        print("Invalid Course ID, please try again.")
        wclass(conn, cwid)

    cur = conn.cursor()
    cur.execute("SELECT cid FROM courses WHERE cid=?", (gcid,))
    records = cur.fetchall()
    if not records:
        print("Course does not exist, please try again.")
        cur.close()
        wclass(conn, cwid)
    else:
        cur.execute("SELECT cid, cwid FROM enroll WHERE cwid=? AND cid=?", (cwid, str(gcid)))
        cpis = cur.fetchall()
        if not cpis:
            print("You are not registered for this class!")
            cur.close()
            wclass(conn, cwid)
        else:
            with conn:
                cur.close()
                d_enroll(conn, cwid, gcid)

def sclass(con):
    while True:
        gcname = str(input("Enter a string to search the course list for, or enter 'exit' to return to the main menu: "))
        if gcname == "exit":
            print("Returning to main menu...\n")
            break
        else:
            gcname = ("%" + gcname + "%")
            cur = con.cursor()
            cur.execute("SELECT cname FROM courses WHERE cname LIKE ?", (gcname,))
            courserecord = cur.fetchall()
            cur.close()
            for all in courserecord:
                print(all)

def mclass(con, cwid):
    cur = con.cursor()
    cur.execute("SELECT c.cname, c.cid FROM courses c, enroll e WHERE E.cwid=? AND e.cid=c.cid", (cwid,))
    courserecord = cur.fetchall()
    cur.close()
    for all in courserecord:
        print(all)

def exitapp(con):
    con.close()
    quit()

def main():
        db = r'fdb.db'
        atmpconn = estconn(db)
        login(atmpconn)
        
if __name__ == "__main__":
        main()
