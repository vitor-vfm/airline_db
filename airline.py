#! /usr/bin/python3

import sys
from DB import DB

class UI():
    """
    Contains all the user interface.
    Reads and processes user input
    and calls the database
    """

    def __init__(self):
        self.db = DB()
        self.flights = []
        self.bookings = []

    def start(self):
        print("Welcome to the airline system")
        self.startScreen()

    def startScreen(self):

        prompt = "Please choose an option\n" + \
        "1 - Login\n" + \
        "2 - Sign up\n" + \
        "3 - Exit\n"

        inp = ""
        while (not inp) or inp not in list('123'):
            inp = input(prompt)

        if inp == '1':
            self.login()
        elif inp == '2':
            self.signup()
        else:
            sys.exit(0)

    def login(self):
        email = input("Email: ")
        passwd = input("Password: ")
        user = self.db.getUser(email)
        if not user:
            print("User not registered. Please sign up")
            self.startScreen()
        else:
            print("Logged in")
            self.email = email
            self.isAgent = self.db.isAirlineAgent(self.email)
            self.userOptions()
        

    def signup(self):
        email = input("Email: ")
        user = self.db.getUser(email)
        if not user:
            passwd = input("Password: ")
            self.db.addUser(email,passwd)
            print("New user added")
        else:
            print("Email already in use")
        self.startScreen()

    def logout(self):
        self.db.updateLastLogin(self.email)
        self.email = ""
        self.isAgent = False
        print("Logged out")
        self.startScreen()


    def userOptions(self):

        prompt = "Please choose an option\n" + \
        "1 - Search for flights\n" + \
        "2 - Make a booking\n" + \
        "3 - List existing bookings\n" + \
        "4 - Cancel a booking\n" + \
        "5 - Logout\n"

        if self.isAgent:
            prompt += "6 - Record flight departure\n" + \
                    "7 - Record flight arrival\n"
            availableOptions = list('1234567')
        else:
            availableOptions = list('12345')

        inp = ""
        while (not inp) or inp not in availableOptions:
            inp = input(prompt)

        if inp == '1':
            self.searchForFlight()
        elif inp == '2':
            self.makeBooking()
        elif inp == '3':
            self.listBookings()
        elif inp == '4':
            self.cancelBooking()
        elif inp == '6':
            self.recordDeparture()
        elif inp == '7':
            self.recordArrival()
        else:
            self.logout()

    def validateAirport(self, air):
        """
        Verify user input for airport
        """
        air = air.upper()
        if not self.db.airportExists(air):
            airports = self.db.getSimilarAirports(air)
            if not airports:
                print("There isn't any airport with that name")
                self.userOptions()
            print("Please select the right airport: ")
            for i, a in enumerate(airports):
                print(i, a)
            option = input("Pick a number: ")
            air = airports[int(option)][0]
        return air

    def searchForFlight(self):
        """
        Ask the user for input and search for corresponding flight
        """
        departure = input("Enter departure date (YYYY-MM-DD): ")
        source = self.validateAirport(input("Enter source airport: "))
        dest = self.validateAirport(input("Enter destination airport: "))
        option = input("Do you want to sort by connections (y/n)? ")
        
        self.flights = self.db.getFlights(source, dest, departure, (option == "y"))

        self.printFlights()

        self.userOptions()

    def printFlights(self):
        """
        Display list of flights to the user
        """
        if not self.flights:
            print("Sorry, there isn't any flight available for you")
            return

        print("(flight 1, flight 2, source, destination, layover, price, time of departure, time of arrival, number of connections, seats in flight 1, seats in flight 2)")
        for i, f in enumerate(self.flights):
            print(i, f)


    def makeBooking(self, flightno):
        name = input("Passenger name: ")
        passinfo = self.db.getPassenger(name, self.email)
        if not passinfo:
            print("Passenger not in system. Adding passenger")
            country = input("Please input passenger's country")
            self.db.addPassenger(name, self.email, country)
            ticket = self.db.addBooking(name, self.email, flightno)
        if ticket:
            print("Success")
            print("Your ticket number is ", ticket)

    def listBookings(self):
        """
        Save the list of bookings in
        self.bookings
        """
        pass

    def printBookings(self):
        if not self.bookings:
            print("You haven't selected bookings yet")
            return

        print("(ticket no, passenger, departure date, price)")
        for i, f in enumerate(self.bookings):
            print(i, f)

    def cancelBooking(self):
        """
        Select a booking from the list
        and cancel it
        """
        if not self.bookings:
            # TODO: make this more usable
            print("Please list bookings first")
            self.userOptions()
        else:
            print("Here are your bookings")
            self.printBookings()
            option = input("Which one would you like to cancel?")
            ticketno = self.bookings[int(option)][0]
            self.db.deleteBooking(ticketno)
            print("Done")
            self.userOptions()

    def recordDeparture(self):
        """
        Record in the system actual departure
        of a given flight
        """
        pass

    def recordArrival(self):
        """
        Record in the system actual arrival
        of a given flight
        """
        pass



# END OF UI CLASS

if __name__=="__main__":
    interface = UI()
    interface.start()
