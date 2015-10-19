# import cx_Oracle as Or

class DB():
    """
    Connects to the database when created
    and performs all CRUD
    """

    def __init__(self):
        fi = open("credentials.txt")
        uname, upass = [line.strip() for line in fi.readlines()]
        # self.con = Or.connect(uname, upass, "gwynne.cs.ualberta.ca:1521/CRS")

    def fetch(self, stmt):
        """
        Execute a SQL SELECT statement
        """
        cur = self.con.cursor()
        cur.execute(stmt)
        res = cur.fetchall()
        cur.close()
        return res

    def getPassenger(self, name, email):
        """
        Return a list of all rows that match
        the name and email
        """
        stmt = "SELECT * FROM passenger" + \
        "WHERE email = %s " % email + \
        "AND name = %s " % name

        return self.fetch(stmt)

if __name__=="__main__":
    db = DB()

