Assignment Instructions from: https://eclass.srv.ualberta.ca/mod/page/view.php?id=1723201

Due : Oct 27 at 5pm 


Clarifications and updates:

You are responsible for monitoring the course news and discussion forums in eclass and this section of the project specification for more details and clarifications. No clarification will be posted after 5pm on Oct 26.

    None.

#Introduction

The goal of this assignment is twofolds: (1) to teach the use of SQL in a host programming language, and (2) to demonstrate some of the functionalities that result from combining SQL with a host programming language.

Your job in this project is to build a system that keeps the enterprise data in a database and to provide services to users. You will be storing data in Oracle and will be writing code in Java/JDBC (or similarly in Python/cx_oracle, C/proC, etc.) to access it. Your code will implement a simple command line interface. You are free to implement a GUI interface instead but there will be no support nor bonus for doing that. You are free to write your code in Java, Python, C, C++, Perl or any other language that is suited for the task. If you decide to use any language other than Java and Python, discuss it with the instructor first.

Your project will be evaluated on the basis of 84% of the mark for implementing the functionalities listed in this specification; this component will be assessed in a demo session. Another 12% of the mark will be assigned for the documentation and quality of your source code and for your design document. 4% of the mark is assigned for the quality of your group coordination and the project break-down between partners.
Group work policy

You will be doing this project with one or two partners from the 291 class. Register your group at the group registration page, as soon as possible. It is assumed that both group members contribute somewhat equally to the project, hence they would receive the same mark. In case of difficulties within groups and when a partner is not lifting his/her weight, make sure to document all your contributions. If there is a break-up, each group member will get credit only for his/her portion of the work completed (losing the mark for any work either not completed or completed by the partner). For the same reason, a break-up should be your last resort.
Database Specification

You are given the following relational schema.

    airports(*acode*, name, city, country, tzone)
    flights(*flightno*, src, dst, dep_time, est_dur)
    sch_flights(*flightno, dep_date*, act_dep_time, act_arr_time)
    fares(*fare*, descr)
    flight_fares(*flightno, fare*, limit, price, bag_allow)
    users(*email*, pass, last_login)
    passengers(*email, name*, country)
    tickets(*tno*, name, email, paid_price)
    bookings(*tno, flightno, dep_date*, fare, seat)
    airline_agents(*email*, name)

The tables are derived from the spec of Assignment 1 and are identical to those in Assignment 2 except the newly added tables users which authenticates the users of your application and airlne_agents which lists the authorized airline agents. The primary key for passengers is changed to email and name, and the name field is added to the tickets table; this change allows users to book for multiple passengers. The SQL commands to create the tables of the system are given here. Use the given schema in your project and do not change any table/column names as we will be testing your project with the given schema.

##Login Screen

The first screen should provide options for both registered and unregistered users. There must be also an option to exit the program. Registered users should be able to login using a valid email and password, respectively referred to as email and pass in table users.

Unregistered users should be able to sign up by providing an email and a password. After a successful login or signup, users should be able to perform the subsequent operations (possibly chosen from a menu) as discussed next.
System Functionalities

##Users should be able to perform all of the following tasks:

###Search for flights. -- Vitor 

A user should be able to search for flights. Your system should prompt the user for a source, a destination and a departure date. For source and destination, the user may enter an airport code or a text that can be used to find an airport code. If the entered text is not a valid airport code, your system should search for airports that have the entered text in their city or name fields (partial match is allowed) and display a list of candidates from which an airport can be selected by the user. Your search for source and destination must be case-insensitive. Your system should search for flights between the source and the destination on the given date(s) and return all those that have a seat available. The search result will include both direct flights and flights with one connection (i.e. two flights with a stop between). The result will include flight details (including flight number, source and destination airport codes, departure and arrival times), the number of stops, the layover time for non-direct flights, the price, and the number of seats at that price. The result should be sorted based on price (from the lowest to the highest); the user should also have the option to sort the result based on the number of connections (with direct flights listed first) as the primary sort criterion and the price as the secondary sort criterion.


###Make a booking. -- Umair

A user should be able to select a flight (or flights when there are connections) from those returned for a search and book it. The system should get the name of the passenger and check if the name is listed in the passenger table with the user email. If not, the name and the country of the passenger should be added to the passenger table with the user email. Your system should add rows to tables bookings and tickets to indicate that the booking is done (a unique ticket number should be generated by the system). Your system can be used by multiple users at the same time and overbooking is not allowed. Therefore, before your update statements, you probably want to check if the seat is still available and place this checking and your update statements within a transaction. Finally the system should return the ticket number and a confirmation message if a ticket is issued or a descriptive message if a ticket cannot be issued for any reason.


###List exiting bookings. -- Umair

A user should be able to list all his/her existing bookings. The result will be given in a list form and will include for each booking, the ticket number, the passenger name, the departure date and the price. The user should be able to select a row and get more detailed information about the booking.


###Cancel a booking. -- Vitor

The user should be able to select a booking from those listed under "list existing bookings" and cancel it. The proper tables should be updated to reflect the cancelation and the cancelled seat should be returned to the system and is made available for future bookings.


###Logout. 

There must be an option to log out of the system. At logout, the field last_login in users is set to the current system date.

##Airline agents should be able to perform all the tasks listed above and the following additional tasks:

###Record a flight departure. -- Umair 

After a plane takes off, the user may want to record the departure. Your system should support the task and make necessary updates such as updating the act_dep_time.

###Record a flight arrival. -- Vitor

After a landing, the user may want to record the arrival and your system should support the task.

## Optional Queries

You are expected to implement one or two tasks of your choice from the following list, depending on the size of your group. A group of two members is required to implement one of the three tasks; a group of three is required to implement two of the tasks. These tasks will not be weighted more than 10% of the project mark, and it is recommended that they are implemented after implementing and testing the basic functionalities, as listed above.


###Support search and booking of round-trips. 

The system should offer an option for round-trips. If this option is selected, your system will get a return date from the user, and will list the flights in both directions, sorted by the sum of the price (from lowest to the highest). The user should be able to select an option and book it.


###Support search and booking of flights with three connecting flights. 

In its default setting, your system will search for flights with two connections at most. In implementing this functionality, your system should offer an option to raise this maximum to three connections. Again this is an option to be set by user when running your system and cannot be the default setting of your application.


###Support search and booking for parties of size larger than one. 

There should be an option for the user to state the number of passengers. The search component of your system will only list flights that have enough seats for all party members. Both the seat pricing and the booking will be based on filling the lowest fare seats first before moving to the next fare. For example, suppose there are 2 seats available in the lowest fare and 5 seats in some higher-priced fare. For a party of size 4, your system will book those 2 lowest fare seats and another 2 seats in the next fare type that is available.

#Testing

At development time you will be testing your programs with your own data sets (make sure that it conforms to the project specification). At demo time we will be creating the database using these SQL statements and will be populating it with our own test data set. Your application will be tested under a demo account (and not your account).

The demo will be run using the source code submitted and nothing else. Therefore, it is essential to include every file that is needed to compile and run your code including all source code and any makefile or script that you may use to compile or run your code. You will neither be able to change your code, nor use any file other than those submitted. This policy can be altered only in exceptional cases at the instructor's discretion and for a hefty penalty. The code will be executed under a demo account. Do not hard-code username, password or table prefixes (such as username or group name) in your code. As a test drill, you should be able to set up your application under someone else's account (in case of testing, this would be under a demo/TA account) within 3 minutes at most.

Every group will book a time slot convenient to all group members to demo their projects. At demo time, all group members must be present.The TA will be using a script to both create and populate the tables. The TA will be asking you to perform various tasks and show how your application is handling each task. A mark will be assigned to your demo immediately after the testing.
Instructions for Submissions

Your submission includes (1) the application source code and (2) the design document. The source code is submitted as follows:

Create a single gzipped tar file with all your source code and additional files you may need for your demo. Name the file prjcode.tgz.
Submit your project tarfile in the project submission site.

Your design document must be type-written and submitted in hardcopy at the designated drop boxes located on the first floor of CSC building, across from the room 1-45, before the due date. Your design document cannot exceed 4 pages.

The design document should include (a) a general overview of your system with a small user guide, (b) a detailed design of your software with a focus on the components required to deliver the major functions of your application, (c) your testing strategy, and (d) your group work break-down strategy. The general overview of the system gives a high level introduction and may include a diagram showing the flow of data between different components; this can be useful for both users and developers of your application. The detailed design of your software should describe the responsibility and interface of each primary class (not secondary utility classes) and the structure and relationships among them. Depending on the programming language being used, you may have methods or functions instead of classes. The testing strategy discusses your general strategy for testing, with the scenarios being tested, the coverage of your test cases and (if applicable) some statistics on the number of bugs found and the nature of those bugs. The group work strategy must list the break-down of the work items among partners, both the time spent (an estimate) and the progress made by each partner, and your method of coordination to keep the project on track. The design document should also include a documentation of any decision you have made which is not in the project specification or any coding you have done beyond or different from what is required.

Your design document must not include the source code. However your source code (which is submitted electronically) would be inspected for source code quality (whether the code is easy to read and if data processing is all done in SQL) and self-documentation (whether the code is properly commented).


