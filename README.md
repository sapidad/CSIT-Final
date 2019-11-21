# CSIT-Final

CHANGE LOG:

11/11/2019: Created main, connection, creating table functions however getting an error below.

Traceback (most recent call last):
  File "<pyshell#0>", line 1, in <module>
    main()
  File "C:/Users/sapidad1/Desktop/pyportable-master/db.py", line 37, in main
    main()
  File "C:/Users/sapidad1/Desktop/pyportable-master/db.py", line 37, in main
    main()
  File "C:/Users/sapidad1/Desktop/pyportable-master/db.py", line 37, in main
    main()
  [Previous line repeated 986 more times]
  File "C:/Users/sapidad1/Desktop/pyportable-master/db.py", line 27, in main
    connect = e_conn(dbase)
  File "C:/Users/sapidad1/Desktop/pyportable-master/db.py", line 42, in e_conn
    conn = sqlite3.connect(db)
RecursionError: maximum recursion depth exceeded while calling a Python object

11/18/2019:

    Implemented:
        - Database Established
        - Data inserted into Tables
        - Existing CWID will bring user into command line, any invalid CWIDs will prompt use to re-enter CWID or type -1
        - L (List Command) has been implemented (See code as a template to create other commands)

     To Do List:
        - Create the -1 option on the "Enter Student ID:" which will prompt user with multiple inputs and will create new student based on inputs
        - Implement the other required commands
        - Probably review/revise the command line menu (?)
        - Test to make sure everything is working as intended.
        - Realized that every other attempt at a command closes the program, will do a constant check for everything that isnt one of the commands in the command list to redirect user to always try again.
        
11/20/2019:

    Implemented:
        - Fixed multiple bugs regarding termination of the command line after multiple failures/successes after failures
        - W and E commands have been implemented and are working as intended (until further notice)
        - FIXED MAJOR BUG where duplicate entries would be entered in to the database when compiling program
        - Enroll Table in Database has a new PRIMARY KEY (eid)
        - New Enrollments by Student are entered in the database having the eid of the last entry + 1 (Enrollment ID)
        - Setup a template in main for partner to work on creating new student function

     To Do List:
        - Implement the other required commands
        - Probably review/revise the command line menu (?)
        - -1 Option for Student ID portion
     
     Creating Student Function (Requirements, atleast in my opinion)
        - Asks Student for Name, Grade (Freshman, Sophomore, Junior, Senior)
        - Generates a 7-Digit CWID at random and sets their GPA to N/A
        - Provide user with the CWID and displays the information asking them to confirm if this information is correct or not.
