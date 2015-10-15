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
        # TODO: start the DB class
        pass

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
        # TODO: check if user is registered
        print("Logged in")
        self.userOptions()
        

    def signup(self):
        email = input("Email: ")
        # TODO: check if user is registered
        # If not, register the user
        passwd = input("Password: ")
        # record new user
        print("New user added")
        self.startScreen()

    def userOptions(self):

        prompt = "Please choose an option\n" + \
        "1 - Search for flights\n" + \
        "2 - Make a booking\n" + \
        "3 - List existing bookings\n" + \
        "4 - Cancel a booking\n" + \
        "5 - Logout\n"

        inp = ""
        while (not inp) or inp not in list('12345'):
            inp = input(prompt)

        if inp == '1':
            self.searchForFlight()
        elif inp == '2':
            self.makeBooking()
        elif inp == '3':
            self.listBookings()
        elif inp == '4':
            self.cancelBooking()
        else:
            print("Logged out")
            self.startScreen()

    def searchForFlight(self):
        pass

    def makeBooking(self):
        pass

    def listBookings(self):
        pass

    def cancelBooking(self):
        pass

# END OF UI CLASS

if __name__=="__main__":
    interface = UI()
    interface.start()
