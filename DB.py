import cx_Oracle as Or
from random import randint

class DB():
    """
    Connects to the database when created
    and performs all CRUD
    """

    def __init__(self):
        fi = open("credentials.txt")
        uname, upass = [line.strip() for line in fi.readlines()]
        self.con = Or.connect(uname, upass, "gwynne.cs.ualberta.ca:1521/CRS")
        self.createViews()

    def createViews(self):
        """
        Create in the database some views
        defined by SQL scripts that will
        be useful in queries
        """
        cur = self.con.cursor()
        for fname in ['available_flights.sql','connections.sql']:
            script = open(fname).read()
            cur.execute(script)
        self.con.commit()

    def fetch(self, stmt):
        """
        Execute a SQL SELECT statement
        """
        cur = self.con.cursor()
        cur.execute(stmt)
        res = cur.fetchall()
        cur.close()
        return res

    def update(self, stmt):
        """
        Execute a SQL INSERT or UPDATE statement
        """
        print('inside update')
        print(stmt)
        cur = self.con.cursor()
        cur.execute(stmt)
        self.con.commit()
        cur.close()
        

    def getPassenger(self, name, email):
        """
        Return a list of all rows that match
        the name and email
        """
        stmt = "SELECT * FROM passengers " + \
        "WHERE email = '%s' " % email + \
        "AND name = '%s'" % name

        return self.fetch(stmt)

    def addPassenger(self, name, email, country):
        """
        Add a new passenger to the DB
        """
        stmt = "INSERT INTO passengers " + \
        "VALUES ('%s', '%s', '%s')" % (email, name, country)
        self.update(stmt)

    def airportExists(self, airport):
        stmt = "SELECT acode FROM airports " + \
                "WHERE acode='%s' " % airport
        return (self.fetch(stmt) != [])

    def getSimilarAirports(self, airport):
        """
        Find airports that might match the string given
        """
        stmt = "SELECT acode, city FROM airports " + \
                "WHERE acode LIKE '%{}%' ".format(airport) + \
                "OR UPPER(city) LIKE '%{}%' ".format(airport) + \
                "OR UPPER(name) LIKE '%{}%' ".format(airport)
        return self.fetch(stmt)

    def getRoundTrips(self, sourceForward, destForward, departure, return_date):
        """
        Retrieve all round trips (or pair of flights) available
        with the specifications
        """
        sourceBackward = destForward
        destBackward = sourceForward

        #####
        # beginning portion
        #####
        stmt = "select t1.flightno1 as forwardFlight1, t1.flightno2 as forwardFlight2, t1.dep_time, t1.src, t1.dst, t1.seats1, t1.seats2, t2.flightno1 as backwardFlight1, t2.flightno2 as backwardFlight2, t2.dep_time, t2.src, t2.dst, t2.seats1, t2.seats2, (t1.price + t2.price) as Price from ("
        


        # for the forward flight info

        stmt += "(select flightno1, flightno2, src, dst, layover, price, to_char(dep_time, 'HH:MI AM') as dep_time, to_char(arr_time, 'HH:MI AM') as arr_time, 1 nCons, seats1, seats2 " + \
                "from connections " + \
                "where to_char(dep_date,'DD-MON-YYYY')='%s' and src='%s' and dst='%s') " % (departure, sourceForward, destForward) + \
                "union " + \
                "(select flightno flightno1, null flightno2, src, dst,  0 layover, price, to_char(dep_time, 'HH:MI AM') as dep_time, to_char(arr_time, 'HH:MI AM') as arr_time, 0 nCons, seats seats1, null seats2 " + \
                "from available_flights " + \
                "where to_char(dep_date,'DD-MON-YYYY')='%s' and src='%s' and dst='%s') " % (departure, sourceForward, destForward)
        stmt += "order by nCons, price "

        #####
        # middle portion
        #####
        stmt += ") t1, ("
        

        # for the backwards flight info

        stmt += "(select flightno1, flightno2, src, dst, layover, price, to_char(dep_time, 'HH:MI AM') as dep_time, to_char(arr_time, 'HH:MI AM') as arr_time, 1 nCons, seats1, seats2 " + \
                "from connections " + \
                "where to_char(dep_date,'DD-MON-YYYY')='%s' and src='%s' and dst='%s') " % (return_date, sourceBackward, destBackward) + \
                "union " + \
                "(select flightno flightno1, null flightno2, src, dst,  0 layover, price, to_char(dep_time, 'HH:MI AM') as dep_time, to_char(arr_time, 'HH:MI AM') as arr_time, 0 nCons, seats seats1, null seats2 " + \
                "from available_flights " + \
                "where to_char(dep_date,'DD-MON-YYYY')='%s' and src='%s' and dst='%s') " % (return_date, sourceBackward, destBackward)
        stmt += "order by nCons, price "


        #####
        # end portion
        #####
        stmt += ") t2 order by Price"
        


        return self.fetch(stmt)


    def getFlights(self, source, dest, departure, sortByCons=False):
        """
        Retrieve all flights (or pair of flights) available
        with the specifications
        """
        stmt = "(select flightno1, flightno2, src, dst, layover, price, to_char(dep_time, 'HH:MI AM'), to_char(arr_time, 'HH:MI AM'), 1 nCons, seats1, seats2 " + \
                "from connections " + \
                "where to_char(dep_date,'DD-MON-YYYY')='%s' and src='%s' and dst='%s') " % (departure, source, dest) + \
                "union " + \
                "(select flightno flightno1, null flightno2, src, dst,  0 layover, price, to_char(dep_time, 'HH:MI AM'), to_char(arr_time, 'HH:MI AM'), 0 nCons, seats seats1, null seats2 " + \
                "from available_flights " + \
                "where to_char(dep_date,'DD-MON-YYYY')='%s' and src='%s' and dst='%s') " % (departure, source, dest)
        if sortByCons:
            stmt += "order by nCons, price "
        else:
            stmt += "order by price "
        return self.fetch(stmt)

    def seatsAvailable(self, flightno, price):
        """
        Check if there are any seats 
        available in a given scheduled flight

        self.db.seatsAvailable("AC158",2000.0)
        """
        stmt = "select seats " + \
        "from available_flights " + \
        "where flightno='%s' and price='%s'" % (flightno,str(price))
        return True if self.fetch(stmt)[0][0] > 0 else False

    def listFareInfoForFlight(self, flightno):
        stmt = "select * " + \
        "from flight_fares " + \
        "where flightno='%s'" % (flightno)
        
        return self.fetch(stmt)
        
    def getNextTicketNumber(self):
        stmt = "select max(tno) from tickets"
        tno = self.fetch(stmt)
        return int(tno[0][0]) + 1

    def getListOfSeatNames(self, flightno):
        stmt = "select seat " + \
        "from bookings " + \
        "where flightno='%s'" % (flightno)
        
        return self.fetch(stmt)
        

    def getListOfBookings(self, email):
        stmt = "select t.tno, trim(name), to_char(dep_date), paid_price " + \
        "from bookings b, tickets t " + \
        "where t.tno = b.tno and email='%s'" % (email)      

        return self.fetch(stmt)

    def getInfoAboutBooking(self, email, tno):
        stmt = "select t.tno, trim(name), trim(email), paid_price, flightno, fare, to_char(dep_date), seat " + \
        "from bookings b, tickets t " + \
        "where t.tno = b.tno and " + \
        "email = '%s' and t.tno = '%d'" %(email, tno)

        return self.fetch(stmt)
        

    def getSeatNameForFlight(self, flightno):
        # ref http://stackoverflow.com/questions/3996904/generate-random-integers-between-0-and-9
        listOfSeatNames = self.getListOfSeatNames(flightno)
        seatName = listOfSeatNames[0] if len(listOfSeatNames) > 0 else "1A"
        while(seatName in listOfSeatNames):
            seatName = str(randint(1,20))
            letter = randint(1,3)
            if letter == 1:
                seatName + "A"
            elif letter == 2:
                seatName + "B"            
            else:
                seatName + "C"
        return seatName

    def getFlightDate(self, flightno, dep_date):
        """
        Retrieve the date for a given flight
        in actual Date format (as opposed to string)
        """
        print(flightno, 'flightno')
        print(dep_date, 'dep_date')
        stmt = "SELECT dep_date " + \
                "FROM sch_flights " + \
                "WHERE flightno='%s' " % flightno + \
                "AND to_char(dep_date, 'DD-MON-YYYY')='%s' " % dep_date
        res = self.fetch(stmt)
        print(res)
        return self.fetch(stmt)[0][0]

    def addBooking(self, name, email, flightno, price, dep_date):
        """
        Add a new booking to the DB
        
        """
        #FIXME: assumes seat name is randomly 
        # generated number from 1-20 inclusive
        # with either A, B or C attached to the end


        tno = self.getNextTicketNumber()
        fares = self.listFareInfoForFlight(flightno)
        for i, f in enumerate(fares):
            print(i,f)
        
        option = input("Pick Fare Type: ")
        fare = fares[int(option)][1] # get fare type
        fare_price = fares[int(option)][3] # get fare price
        seat = self.getSeatNameForFlight(flightno)
        if (price != fare_price):
            price = fare_price
            print("Your new price is: " + str(price))

        stmt = "INSERT INTO tickets " + \
        "VALUES ('%d', '%s', '%s', '%d')" % (tno, name, email, price)
        self.update(stmt)

        dep_date = self.getFlightDate(flightno, dep_date)

#         stmt = "INSERT INTO bookings " + \
#         "VALUES ('%d', '%s', '%s',to_date('%s','DD-MON-YYYY'),'%s')" % (tno, flightno, fare, dep_date, seat)
#         self.update(stmt)

        stmt = "INSERT INTO bookings " + \
                "VALUES(:tno, :flightno, :fare, :dep_date, :seat)"
        cur = self.con.cursor()
        cur.prepare(stmt) 

        binds = {
                'tno' : tno,
                'flightno' : flightno,
                'fare' : fare,
                'dep_date' : dep_date,
                'seat' : seat,
                }
        cur.execute(None, binds)
        self.con.commit()

        return tno

    def deleteBooking(self, ticketno):
        """
        From a ticket number, delete corresponding
        rows in tickets and bookings
        """
        for table in ['bookings','tickets']:
            stmt  = "DELETE FROM %s " % table + \
                    "WHERE tno='%s' " % ticketno
            self.update(stmt)

    def flightExists(self, flightno, dep_date):
        """
        Given flight info,
        find out if there is a corresponding
        scheduled flight

        Returns a boolean
        """
        stmt = "SELECT flightno " + \
                "FROM sch_flights " + \
                "WHERE flightno='%s' " % flightno + \
                "AND to_char(dep_date, 'DD-MON-YYYY')='%s' " % dep_date
        return (self.fetch(stmt) != [])

    def recordActualTime(self, flightno, dep_date, actualTime, departure):
        """
        Update the actual arrival or departure 
        of a flight in the DB

        'departure' is a boolean that informs if the 
        time to be updated is the departure or arrival
        """
        if departure:
            col = 'act_dep_time'
        else:
            col = 'act_arr_time'

        stmt = "UPDATE sch_flights " + \
                "SET %s=to_date('%s', 'DD-MON-YYYY HH:MI') " % (col, actualTime) + \
                "WHERE flightno='%s' " % flightno + \
                "AND to_char(dep_date, 'DD-MON-YYYY')='%s' " % dep_date
        self.update(stmt)

    def getUser(self, email):
        """
        Fetch user(s)
        """
        stmt = "SELECT * FROM users U " + \
        "WHERE U.email='%s'" % email
        return self.fetch(stmt)

    def addUser(self, email, passwd):
        """
        Add a new user to the DB

        When first added, the last_login
        of the user is set to null
        """
        stmt = "INSERT INTO users " + \
        "VALUES ('%s', '%s', NULL)" % (email, passwd)
        self.update(stmt)

    def isAirlineAgent(self,email):
        """
        Check in the database if the given 
        user is an airline agent
        """
        stmt = "SELECT email FROM airline_agents " + \
                "WHERE email='%s' " % email
        return True if self.fetch(stmt) != [] else False

    def updateLastLogin(self, email):
        """
        Given a user email, updates
        the corresponding row with the 
        current date
        """
        stmt = "UPDATE users "  + \
        "SET last_login=SYSDATE " + \
        "WHERE email='%s'" % email
        self.update(stmt)


if __name__=="__main__":
    db = DB()

