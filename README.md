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
  
Erase this line and enter next date when more things are changed and/or tinkered, add log of current additions/changes after putting date.
