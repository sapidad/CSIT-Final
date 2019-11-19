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
