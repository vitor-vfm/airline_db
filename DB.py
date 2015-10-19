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
        cur = self.con.cursor()
        cur.execute(stmt)
        cur.close()
        

    def getPassenger(self, name, email):
        """
        Return a list of all rows that match
        the name and email
        """
        stmt = "SELECT * FROM passenger " + \
        "WHERE email = %s " % email + \
        "AND name = %s " % name

        return self.fetch(stmt)

    def addPassenger(self, name, email, country):
        """
        Add a new passenger to the DB
        """
        stmt = "INSERT INTO passenger "
        "VALUES('%s', '%s', '%s')" % (email, name, country)
        self.update(stmt)

    def getUser(self, email):
        """
        Fetch user(s)
        """
        stmt = "SELECT * FROM users "
        "WHERE email = %s " % email
        return self.fetch(stmt)

    def updateLastLogin(self, email):
        """
        Given a user email, updates
        the corresponding row with the 
        current date
        """
        stmt = "UPDATE users " 
        "SET last_login=SYSDATE "
        "WHERE email=%s" % email
        self.update(stmt)


if __name__=="__main__":
    db = DB()

