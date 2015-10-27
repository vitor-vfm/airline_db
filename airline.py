#! /usr/bin/python3

import sys
from subprocess import call
import re
from DB import DB

class UI():
    """
    Contains all the user interface.
    Reads and processes user input
    and calls the database
    """

    def __init__(self):
        self.flights = []
        self.bookings = []
        self.roundTrips = []

        try:
            self.db = DB()
        except:
            print("It seems that there is no credentials.txt file. Please create one")
            sys.exit()

        ###### test booking for 'make a booking feature'
        # checked and it works
        # self.db.addBooking("Uma", "s@test", "AC158", "100", "22-Dec-2015")

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

    def getDate(self, prompt):
        """
        Receive a date from the user
        and check for errors
        
        Format: DD-MON-YYYY
        """
        pattern = r"^[0-9]{2}-[A-Z]{3}-[0-9]{4}$"
        while True:
            date = input(prompt).upper()
            if re.match(pattern, date):
                break
            else:
                print("Not a valid date")
        return date


    def userOptions(self):

        prompt = "Please choose an option\n" + \
        "1 - Search for flights\n" + \
        "2 - Search for round-trips\n" + \
        "3 - Make a booking\n" + \
        "4 - Make a booking for round-trips\n" + \
        "5 - List existing bookings\n" + \
        "6 - Cancel a booking\n" + \
        "7 - Logout\n"

        if self.isAgent:
            prompt += "8 - Record flight departure\n" + \
                    "9 - Record flight arrival\n"
            availableOptions = list('123456789')
        else:
            availableOptions = list('1234567')

        inp = ""
        while (not inp) or inp not in availableOptions:
            inp = input(prompt)

        if inp == '1':
            self.searchForFlight()
        elif inp == '2':
            self.searchForRoundTrips()
        elif inp == '3':
            self.makeBooking()
        elif inp == '4':
            self.makeBookingForRoundTrips()
        elif inp == '5':
            self.listBookings()
        elif inp == '6':
            self.cancelBooking()
        elif inp == '8':
            self.recordDeparture()
        elif inp == '9':
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


    def searchForRoundTrips(self):
        """
        Look for round trips that in the dates and locations
        specified by the user

        Save them in an attribute for later reference
        """
        self.departure = self.getDate("Enter departure date (DD-Mon-YYYY): ")
        self.return_date = self.getDate("Enter return date (DD-Mon-YYYY): ")
        sourceForward = self.validateAirport(input("Enter source airport: "))
        destForward = self.validateAirport(input("Enter destination airport: "))
        
        self.roundTrips = self.db.getRoundTrips(sourceForward, destForward, self.departure, self.return_date)

        self.printRoundTrips()

        self.userOptions()


    def searchForFlight(self):
        """
        Ask the user for input and search for corresponding flight
        """
        self.departure = self.getDate("Enter departure date (DD-Mon-YYYY): ")
        source = self.validateAirport(input("Enter source airport: "))
        dest = self.validateAirport(input("Enter destination airport: "))
        option = input("Do you want to sort by connections (y/n)? ")
        
        self.flights = self.db.getFlights(source, dest, self.departure, (option == "y"))

        self.printFlights()

        self.userOptions()


    def printRoundTrips(self):
        """
        Display list of round trips to the user
        """
        if not self.roundTrips:
            print("Sorry, there isn't any flight available for you")
            return

        print("(forwardFlight1, forwardFlight2, departure_time, forwardSource, forwardDestination, forwardFlight1Seats1, forwardFlight1Seats2 backwardFlight1, backwardFlight2, departure_time, backwardSource, backwardDestination, backwardFlightSeats1, backwardFlightSeats2, price)")
        for i, f in enumerate(self.roundTrips):
            print(i, f)



    def printFlights(self):
        """
        Display list of flights to the user
        """
        if not self.flights:
            print("Sorry, there isn't any flight available for you")
            return

        print("(flight 1, flight 2, source, destination, layover, " + \
                "price, time of departure, time of arrival, number of " + \
                "connections, seats in flight 1, seats in flight 2)")
        for i, f in enumerate(self.flights):
            print(i, f)

    def makeBookingForRoundTrips(self):
        if not self.roundTrips:
            print("Please search for a round trip before booking it.")
            self.userOptions()
            return

        option = input("Pick a round trip flight number: ")
        roundTripInfo = self.roundTrips[int(option)]

        name = input("Passenger name: ")
        passinfo = self.db.getPassenger(name, self.email)
        if not passinfo:
            print("Passenger not in system. Adding passenger")
            country = input("Please input passenger's country: ")
            self.db.addPassenger(name, self.email, country)
        
        # corresponds to flightno, price, seats 
        
        # forward
        tripInfo1 = [roundTripInfo[0], roundTripInfo[14], roundTripInfo[5], self.departure]
        # FIXME: we need to determine departure date of the second flight in the connection
        # right now we just using original, user speicifed dep_date for both
        tripInfo2 = [roundTripInfo[1], roundTripInfo[14], roundTripInfo[6], self.departure]

        # backward
        tripInfo3 = [roundTripInfo[7], roundTripInfo[14], roundTripInfo[12], self.return_date]
        # FIXME: we need to determine departure date of the second flight in the connection
        # right now we just using original, user speicifed return_date for both
        tripInfo4 = [roundTripInfo[8], roundTripInfo[14], roundTripInfo[13], self.return_date]


        for flightno, price, seats, dep_date in [tripInfo1, tripInfo2, tripInfo3, tripInfo4]:   
            if flightno == None or seats == None:
                print("Single connection")
                continue

            if int(seats) == 0:
                print("No seats available.")
                return

            ticket = self.db.addBooking(name, self.email, flightno, price, dep_date)
            if ticket:
                print("Success.")
                print("Your ticket number is ", ticket)

        self.userOptions()


    def makeBooking(self):
        # FIXME: add error checking, and support for flight2

        if not self.flights:
            print("Please search for a flight before booking it.")
            self.userOptions()
            return

        option = input("Pick a flight number: ")
        flightInfo = self.flights[int(option)]

        name = input("Passenger name: ")
        passinfo = self.db.getPassenger(name, self.email)
        if not passinfo:
            print("Passenger not in system. Adding passenger")
            country = input("Please input passenger's country: ")
            self.db.addPassenger(name, self.email, country)
        

        # corresponds to flightno, price, seats 
        flightInfo1 = [flightInfo[0], flightInfo[5], flightInfo[9]]
        flightInfo2 = [flightInfo[1], flightInfo[5], flightInfo[10]]

        for flightno, price, seats in [flightInfo1, flightInfo2]:   
            if flightno == None or seats == None:
                print("Single connection")
                continue

            if int(seats) == 0:
                print("No seats available.")
                return

            ticket = self.db.addBooking(name, self.email, flightno, price, self.departure)
            if ticket:
                print("Success.")
                print("Your ticket number is ", ticket)

        self.userOptions()

    def listBookings(self):
        """
        Save the list of bookings in
        self.bookings and print it
        """
        self.bookings = self.db.getListOfBookings(self.email)
        if not self.bookings:
            print("No bookings")
            self.userOptions()

        print("(ticket number, name, departure_date, " +
                "paid price)")
        for i, f in enumerate(self.bookings):
            print(i, f)

        option = input("Would like more info about any of the bookings (y/n)? ")
        if option.lower() == "y":
            option = -1
            while option not in range(len(self.bookings)):
                option = int(input("Choose one of the bookings for more info: "))
            tno = self.bookings[option][0]
            print(tno)
            print("(ticket number, passenger, passenger email, paid price, flight, fare, departure date, seat)")
            tnoInfo = self.db.getInfoAboutBooking(self.email, int(tno))
            print(tnoInfo)        

        self.userOptions()

    def printBookings(self):
        if not self.bookings:
            print("No bookings")
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
            print("Please list bookings first")
            self.userOptions()
        else:
            print("Here are your bookings")
            self.printBookings()
            option = -1
            while option not in range(len(self.bookings)):
                option = int(input("Which one would you like to cancel? "))
            ticketno = self.bookings[option][0]
            self.db.deleteBooking(ticketno)
            print("Done")
            self.userOptions()

    def recordDeparture(self):
        """
        Record in the system actual departure
        of a given flight
        """
        flightno = input("Inform which flight departed: ").upper()
        dep_date = self.getDate("Inform the flight's scheduled departure day (DD-MON-YYYY): ")
        if not self.db.flightExists(flightno,dep_date):
            print("That is not a scheduled flight")
            self.userOptions()
        else:
            actual_departure = input("Inform date and time of departure " + \
                    "(DD-MON-YYYY HH:MI): ")
            self.db.recordActualTime(flightno, dep_date, actual_departure, departure=True)
            print("Done")
            self.userOptions()


    def recordArrival(self):
        """
        Record in the system actual arrival
        of a given flight
        """
        flightno = input("Inform which flight arrived: ").upper()
        dep_date = self.getDate("Inform the flight's scheduled departure day (DD-MON-YYYY): ")

        if not self.db.flightExists(flightno,dep_date):
            print("That is not a scheduled flight")
            self.userOptions()
        else:
            actual_arrival = input("Inform date and time of arrival (DD-MON-YYYY HH:MI): ")
            self.db.recordActualTime(flightno, dep_date, actual_arrival, departure=False)
            print("Done")
            self.userOptions()



# END OF UI CLASS

if __name__=="__main__":
    interface = UI()
    interface.start()
