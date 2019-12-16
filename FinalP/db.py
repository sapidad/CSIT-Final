import sqlite3
import string
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
    cur.execute("INSERT OR IGNORE INTO students(cwid,sname,gradelv,gpa) VALUES(?,?,?,?)", student)
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
            cwid = int(input("Student ID: "))
            return cwid
        except ValueError:
            print("Not a valid Student ID, please try again.")

def cwidgen(con):
    while True:
        gcwid = randint(10000000, 99999999)
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM students WHERE cwid=? GROUP BY cwid", (gcwid,))
        exist = cur.fetchone()
        if exist is None:
            print("Your CWID is: " + str(gcwid))
            cur.close()
            return gcwid

def sname():
    name = input("Student Name: ")
    for i in range(len(name)):
        if name[i].isdigit():
            print("Invalid entry, please try again.")
            sname()
    else:
        return string.capwords(name)

def gradelv():
    while True:
        g = input("Grade level: ")
        if g.lower() == 'freshman' or g.lower() == 'sophomore' or g.lower() == 'junior' or g.lower() == 'senior':
            return string.capwords(g)
        else:
            print("Entries can only be Freshman, Sophomore, Junior, Senior")

def gpa():
    while True:
        try:
            gp = float(input("GPA: "))
            if gp > 4.0 or gp < 0:
                print("Invalid GPA value, please enter a valid number.")
            else:
                return gp
        except ValueError:
            print("Invalid GPA value, please enter a valid number.")

def n_student(con):
        ncwid = cwidgen(con)
        nsname = sname()
        ngradelv = gradelv()
        ngpa = gpa()

        print("\nYour Information is:\nCWID: " + str(ncwid) + "\nName: " + nsname + "\nGrade level: " + ngradelv + "\nGPA: " + str(ngpa))
        c = str(input("Is this correct? Please type Y or N: "))

        if c.lower() == 'y':
            c_student(con, ncwid, nsname, ngradelv, ngpa)
            print("You have been registered in the database! Log in to enroll into a course.")
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
                                               gradelv text NOT NULL,
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

            c_enroll(con, "0", "21612390", "420", "4-20-2020", "A+")
            c_enroll(con, "1", "21612390", "500", "4-01-2020", "B+")
            c_enroll(con, "2", "21612390", "012", "3-16-2020", "F")
            c_enroll(con, "3", "21612390", "069", "3-20-2020", "B")

            c_enroll(con, "4", "21612391", "420", "4-20-2020", "A+")
            c_enroll(con, "5", "21612391", "500", "4-10-2020", "B-")
            c_enroll(con, "6", "21612391", "012", "4-15-2020", "C+")

            c_enroll(con, "7", "21612392", "500", "1-11-2020", "A-")
            c_enroll(con, "8", "21612392", "012", "3-22-2020", "B")
            c_enroll(con, "9", "21612392", "069", "4-23-2020", "D")

            c_enroll(con, "10", "21612393", "420", "2-03-2020", "C-")
            c_enroll(con, "11", "21612393", "777", "2-01-2020", "D+")

            c_enroll(con, "12", "21612394", "420", "4-20-2020", "A+")
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
    cur.execute("SELECT sname FROM students WHERE cwid=?", (cwid,))
    getname = cur.fetchall()
    s = str(getcwid)
    n = str(getname)
    cwid = re.sub('[^A-Za-z0-9]+', '', s)
    name = re.sub('[^A-Za-z0-9]+', ' ', n)
    print("\nWelcome, please type in a command or type commands for help!")
    print("Student:" + name)
    print("CWID: " + cwid)
    cur.close()
    cline(con, cwid)

         
def cline(con, cwid):
        inp = str(input("Please type in a command: "))
        if inp.isdigit() == True:
            print("Integer values are not valid commands, try again.\n")
        elif inp == 'commands':
            print("L: Lists all Courses")
            print("E: Enrolls Student(s) into a Course")
            print("W: Withdraw Class")
            print("S: Search for a Course")
            print("M: View your Classes")
            print("X: Exit")
            print("-: Log Out\n")
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
        elif inp == '-':  # function i added to return to the login
            login(con)
        else:
            print("Not a valid command, try again.\n")

        cline(con, cwid)

def list(con):
    cur = con.cursor()
    cur.execute("SELECT * FROM courses")
    courserecord = cur.fetchall()
    cur.close()
    for all in courserecord:
        print(all)

def eclass(conn, cwid):
    while True:
        gcid = input("Please enter a Course ID or type 'exit': ")
        if gcid.isalpha and gcid == "exit":
            print("Returning to main menu...\n")
            break
        elif gcid.isdigit():
            cur = conn.cursor()
            cur.execute("SELECT cid FROM courses WHERE cid=?", (gcid,))
            records = cur.fetchall()
            if not records:
                print("Course does not exist, please try again.")
                cur.close()
            else:
                cur.execute("SELECT cid, cwid FROM enroll WHERE cwid=? AND cid=?", (cwid, str(gcid)))
                cpis = cur.fetchall()
                cur.execute("SELECT eid FROM enroll ORDER BY eid DESC LIMIT 1;")
                leid = str(cur.fetchall())
                eid = int(re.sub('[^A-Za-z0-9]+', '', leid)) + 1
                if not cpis:
                    cur.execute("SELECT cid, cname FROM courses WHERE cid=?", (str(gcid),))
                    get = cur.fetchall()
                    print(get)
                    c = str(input("Are you sure you want to enroll in this class? Please type Y or N: "))
                    if c.lower() == 'y':
                        with conn:
                            c_enroll(conn, str(eid), cwid, str(gcid), str(date.today()), "N/A")
                            cur.close()
                            print("Enrollment Complete")
                    elif c.lower == 'n':
                        print("Enrollment Failed.")
                        cur.close()
                else:
                    print("You are currently registered for this class!")
                    cur.close()
        else:
            print("Invalid Course ID, please try again.")

def wclass(conn, cwid):
    while True:
        cur = conn.cursor()
        cur.execute("SELECT cid FROM enroll WHERE cwid=?", (cwid,))
        erecords = cur.fetchall()
        if not erecords:
            print("You are not enrolled in any classes, please enter the 'E' command to enroll in a class or 'L' to view all available classes!")
            break
        else:
            gcid = input("Please enter a Course ID or type 'exit': ")
            if gcid.isalpha() and gcid == "exit":
                print("Returning to main menu...\n")
                break
            elif gcid.isdigit() == True:
                cur = conn.cursor()
                cur.execute("SELECT cid FROM courses WHERE cid=?", (gcid,))
                records = cur.fetchall()
                if not records:
                    print("Course does not exist, please try again.")
                    cur.close()
                else:
                    cur.execute("SELECT cid, cwid FROM enroll WHERE cwid=? AND cid=?", (cwid, str(gcid)))
                    cpis = cur.fetchall()
                    if not cpis:
                        print("You are not registered for this class!")
                        cur.close()
                        wclass(conn, cwid)
                    else:
                        with conn:
                            cur.execute("SELECT E.cwid, E.cid, C.cname FROM enroll E, courses C WHERE E.cid = C.cid AND E.cwid=? AND E.cid=?",
                                (cwid, str(gcid),))
                            get = cur.fetchall()
                            print(get)
                            c = str(input("Are you sure you want to withdraw from this class? Please type Y or N: "))
                            if c.lower() == 'y':
                                with conn:
                                    cur.execute("DELETE FROM enroll WHERE cwid=? AND cid=?", (cwid, str(gcid),))
                                    cur.close()
                                    print("Withdrawal Successful")
                            elif c.lower() == 'n':
                                print("Withdrawal Failed.")
                                cur.close()
            else:
                print("Invalid Course ID, please try again.")


def sclass(con):
    while True:
        gcname = str(input("Enter a string to search the course list for, or type 'exit': "))
        if gcname == "exit":
            print("Returning to main menu...\n")
            break
        else:
            gcname = ("%" + gcname + "%")
            cur = con.cursor()
            cur.execute("SELECT cname FROM courses WHERE cname LIKE ?", (gcname,))
            courserecord = cur.fetchall()
            cur.close()
            if not courserecord:
                print("This course does not exist in the database. Please contact your System Administrator.")
            else:
                for all in courserecord:
                    print(all)

def mclass(con, cwid):
    cur = con.cursor()
    cur.execute("SELECT c.cname, c.cid FROM courses c, enroll e WHERE E.cwid=? AND e.cid=c.cid", (cwid,))
    courserecord = cur.fetchall()
    if not courserecord:
        print("You are not enrolled in any classes, please enter the 'E' command to enroll in a class or 'L' to view all available classes!")
    else:
        for all in courserecord:
            print(all)
        print("")

def exitapp(con):
    con.close()
    quit()

def main():
        db = r'fdb.db'
        atmpconn = estconn(db)
        login(atmpconn)
        
if __name__ == "__main__":
        main()
