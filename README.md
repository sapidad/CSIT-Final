# CSIT-Final

Authors of this Project: David Sapida and Andre Stillo

CHANGE LOG:

11/11/2019 (David) : Created main, connection, creating table functions however getting an error below.

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

11/18/2019 (David):

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
        
11/20/2019 (David):

    Implemented:
        - Fixed multiple bugs regarding termination of the command line after multiple failures/successes after failures
        - W and E commands have been implemented and are working as intended (until further notice)
        - FIXED MAJOR BUG where duplicate entries would be entered in to the database when compiling program
        - Enroll Table in Database has a new PRIMARY KEY (eid)
        - New Enrollments by Student are entered in the database having the eid of the last entry + 1 (Enrollment ID)
        - Setup a template in main for partner to work on creating new student function
        - EDIT ON 11/20/2019 @ 11:13PM: Fixed Bug if user incorrectly types a invalid Course ID when being prompted to in W and E commands.

     To Do List:
        - Implement the other required commands
        - Probably review/revise the command line menu (?)
        - -1 Option for Student ID portion
        - Potentially (If we have time), I (David) will redo the course table, to have another field for size and will reject the user from enrolling in a course that is full.
     
     Creating Student Function (Requirements, atleast in my opinion)
        - Asks Student for Name, Grade (Freshman, Sophomore, Junior, Senior)
        - Generates a 7-Digit CWID at random and sets their GPA to N/A
        - Provide user with the CWID and displays the information asking them to confirm if this information is correct or not.

12/1/2019 (Andy):

    Implemented:
        - Fixed a bug where inputting an invalid CWID would cause the next valid CWID to fail
        - Restructured many of the functions to simplify code and reduce repetitiveness on the user side
        - Implemented the remaining functions, m, s, x and the new student function. Also added a function tied to - that will log the user out.
     
     To Do List:
        - Error checking for the new student function, possibly making the cwid randomly generated. Adding a confirmation to the new student function.
        - Improving the search function
        - Revise command line menu(?)
        - Adding method to return to main menu from each function (If there's time, I (Andy) will implement this)

12/2/2019 (Andy):

    Implemented:
        -CWID is randomly generated when creatinng a new student. Also added the confirmation, as well as formatting to the entries, as well as adding some constraints to entries.
        -Fixed errors within the new student function.
        -Closed cursors all cursors at the end of most functions.
        -Changed formatting on date in enrolled to match generated dates.
        -Improved search function, now loops until the user types 'exit' and searches more effectively.
        -Restructured program in order to be more concise, weworked cline function.
        -Improved presentation (it still needs work though).
     
     To Do List:
        - Improve presentation.
        - Ask professor for advice involviong foreign keys (cid in table enroll).
        - Try to think of ways to refine the program, I'm out of ideas.
        - Bug fixing.
        
12/2/2019 (David):

    Implemented:
        -Added exit functionality in Withdraw and Enroll commands
        -Fixed up creating New Student Function (with restrictions)
        -New Students/Not Enrolled Students will be prompted that they have no courses in their account if they are not enrolled in any classes when using M or W commands.
        
    To Do List: 
        -Finding/Fixing Bugs
        -Possible additional implementations

12/3/2019 (Andy):

    Implemented:
        -Fixed a bug that caused the new student function to throw an error after a invalid grade and gpa were passed.
        
    To Do List: 
        -Finding/Fixing Bugs

12/15/2019 (Andy):

    Implemented:
        -Changed the name of grade in students table to gradelv. This is because a variable grade already exists in Enrolled. 
        -A few other QOL changes.
        
    To Do List: 
        -Finding/Fixing Bugs
        -Ask david if we should keep the preq attribute in Courses.


12/16/2019 (Andy & David):

    Implemented:
        -Fixed a bug that would allow users to enter a name as only numbers. 
        -Fixed a bug that would cause multiple outputs of the same string in the witdrawal method (wclass)
        -Changed preq attribute to professor (attribute is never used, moreso done for realism)
        -Edited the classes and students entries to their final iterations (RIP James)
        
    To Do List: 
        -Finding/Fixing Bugs, but overall we are done.
