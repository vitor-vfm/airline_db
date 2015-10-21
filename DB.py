import cx_Oracle as Or

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
        print("inside fetch")
        print("stmt:")
        print(stmt)
        cur.execute(stmt)
        res = cur.fetchall()
        print("res", res)
        cur.close()
        return res

    def update(self, stmt):
        """
        Execute a SQL INSERT or UPDATE statement
        """
        cur = self.con.cursor()
        print("inside update")
        print("stmt:")
        print(stmt)
        cur.execute(stmt)
        self.con.commit()
        cur.close()
        

    def getPassenger(self, name, email):
        """
        Return a list of all rows that match
        the name and email
        """
        stmt = "SELECT * FROM passenger " + \
        "WHERE email = '%s' " % email + \
        "AND name = '%s';" % name

        return self.fetch(stmt)

    def addPassenger(self, name, email, country):
        """
        Add a new passenger to the DB
        """
        stmt = "INSERT INTO passengers " + \
        "VALUES ('%s', '%s', '%s')" % (email, name, country) + \
        ";"
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

    def getFlights(self, source, dest, departure, sortByCons=False):
        """
        Retrieve all flights (or pair of flights) available
        with the specifications
        """
        stmt = "(select flightno1, flightno2, layover, price, dep_time, arr_time, 1 nCons " + \
                "from connections " + \
                "where to_char(dep_date,'YYYY-MM-DD')='%s' and src='%s' and dst='%s') " % (departure, source, dest) + \
                "union " + \
                "(select flightno flightno1, '' flightno2, 0 layover, price, dep_time, arr_time, 0 nCons " + \
                "from available_flights " + \
                "where to_char(dep_date,'YYYY-MM-DD')='%s' and src='%s' and dst='%s') " % (departure, source, dest)
        if sortByCons:
            stmt += "order by nCons, price "
        else:
            stmt += "order by price "
        return self.fetch(stmt)

    def seatsAvailable(self, flightno):
        """
        Check if there are any seats 
        available in a given scheduled flight
        """
        return True

    def addBooking(flightno, passemail):
        pass

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

