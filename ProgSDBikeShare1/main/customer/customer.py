from datetime import datetime
import random
import sqlite3
from tkinter import messagebox

from main.utils import get_time_date

"""
customer page
"""
class Customer:


    def __init__(self, username, station):
        self.username = username
        self.station = station

    def init_rent_interface(self, combobox):
        # connect to db
        db = sqlite3.connect('../../bicycle_db/db_file/bicycle.db')
        cursor = db.cursor()

        # fetch user id by searching up by their username
        user_id = cursor.execute("SELECT user_id from T_DM_USER WHERE user_name = ?", (self.username,)).fetchone()[0]

        # check user is valid to rent a bike
        if not self.rent_bike_check_user_validity(user_id):
            message = ("You cannot currently rent a bike. This may be because:"
                  "\n 1) You have a currently ongoing rental"
                  "\n or"
                  "\n 2) Your account balance is negative"
                  "\n Please fix these issues and try again.")
            self.dialog_warning()
        else:
            # display all bicycles that are a) are located at current terminal b) are not being used c) are not broken (all 3)
            cursor.execute(
                "SELECT * FROM T_DM_BICYCLE WHERE STATION_ID = ? AND BIC_USE_STATUS = 0 AND BIC_BROKEN_STATUS = 0",
                (self.station,))
            result = cursor.fetchall()

            # Tell the user how many bikes are available and list them
            print("There are " + str(len(result)) + " Bicycles available at this location!")
            list_available_bikes = []
            for x in range(0, len(result)):
                list_available_bikes.append(str(x + 1) + ". Bicycle ID: " + str(result[x][0]))
            combobox['values'] = list_available_bikes






    def rentBike(self):
        # connect to db
        db = sqlite3.connect('../../bicycle_db/db_file/bicycle.db')
        cursor = db.cursor()



        # fetch user id by searching up by their username
        user_id = cursor.execute("SELECT user_id from T_DM_USER WHERE user_name = ?", (self.username,)).fetchone()[0]

        # check user is valid to rent a bike
        if not self.rent_bike_check_user_validity(user_id):
            print("You cannot currently rent a bike. This may be because:"
                  "\n 1) You have a currently ongoing rental"
                  "\n or"
                  "\n 2) Your account balance is negative"
                  "\n Please fix these issues and try again.")
            return None

        # display all bicycles that are a) are located at current terminal b) are not being used c) are not broken (all 3)
        cursor.execute("SELECT * FROM T_DM_BICYCLE WHERE STATION_ID = ? AND BIC_USE_STATUS = 0 AND BIC_BROKEN_STATUS = 0",
                       (self.station,))
        result = cursor.fetchall()

        # Tell the user how many bikes are available and list them
        print("There are " + str(len(result)) + " Bicycles available at this location!")
        list_available_bikes = []
        for x in range(0, len(result)):
            list_available_bikes.append(str(x + 1) + ". Bicycle ID: " + str(result[x][0]))

        # Allow the user to choose one and validate their selection
        valid_selection = False
        while not valid_selection:
            for item in list_available_bikes:
                print(item)
            selection_str = input("What bike do you want? \n Leave blank to get assigned a random one : ")
            if selection_str == "":
                selection = random.randrange(1, len(result))
                valid_selection = True
                break

            selection = int(selection_str)
            if 0 <= selection <= len(result):
                valid_selection = True
                selection -= 1
            else:
                print("Please select a valid bike!")

        # set the bike ID to the user's selection
        id_chosen_bike = result[selection][0]

        # Use the bike ID to mark the bike as used on the database (set BIC_USE_STATUS to 1)
        cursor.execute("UPDATE T_DM_BICYCLE SET BIC_USE_STATUS = '1' WHERE BIC_ID = ?", (id_chosen_bike,))

        # Update the T_USER_RENTAL_LOG table (enter trip id, user id,bike id, start time, end time (null), start location,
        # end location (null), trip amount (null))
        cursor.execute(
            "INSERT INTO T_USER_RENTAL_LOG (TRIP_ID, USER_ID, BIC_ID, START_TIME, END_TIME, START_STATION_ID, "
            "END_STATION_ID, TRIP_AMOUNT ) "
            "VALUES ((SELECT MAX(TRIP_ID) + 1 FROM T_USER_RENTAL_LOG), ?, ?, ?, NULL, ?, NULL, NULL)",
            (user_id, id_chosen_bike, get_time_date(), self.station,))

        print("Thank you for using our services, please pick up bike " + str(id_chosen_bike) + " located in this station!")

        # close and commit
        db.commit()
        db.close()


    def returnBike(self):
        SECONDS_IN_MINUTE = 60

        # connect ot the db
        db = sqlite3.connect('../../bicycle_db/db_file/bicycle.db')
        cursor = db.cursor()



        # fetch user id by searching up by their username
        user_id = cursor.execute("SELECT user_id from T_DM_USER WHERE user_name = ?", (self.username,)).fetchone()[0]

        # check user's rental logs if they have one proceed, otherwise, exit
        cursor.execute("SELECT *  FROM T_USER_RENTAL_LOG WHERE user_id = ?", (user_id,))
        prev_rental = cursor.fetchall()

        # get the last rental
        prev_rental = prev_rental[len(prev_rental) - 1]
        is_rental_ongoing = prev_rental[4] is None and prev_rental[4] is None and prev_rental[4] is None
        if not is_rental_ongoing:
            print("You have no ongoing rentals! ")
            return 0

        # get the start and end date and calc the fee (.1 * minutes)
        start_date_string = prev_rental[3]
        start_date = datetime.strptime(start_date_string, "%Y-%m-%d %H:%M:%S")
        total_time = datetime.strptime(get_time_date(), "%Y-%m-%d %H:%M:%S") - start_date
        fee = (total_time.total_seconds() // SECONDS_IN_MINUTE) / 10
        print("The fee for your rental is " + str(fee))
        trip_id = prev_rental[0]

        # update the rental log table to show final location, end time and fee
        cursor.execute("UPDATE T_USER_RENTAL_LOG SET END_TIME = ?, END_STATION_ID = ? , TRIP_AMOUNT = ? WHERE TRIP_ID = ?",
                       (get_time_date(), self.station, fee, trip_id))

        # get the bike id
        bike_id = prev_rental[2]

        # update the current bike to not used and change location
        cursor.execute("UPDATE T_DM_BICYCLE SET BIC_USE_STATUS = 0, STATION_ID = ? WHERE BIC_ID = ?", (self.station, bike_id,))

        # get user balance
        balance = cursor.execute("SELECT USER_ACCOUNT_BALANCE FROM T_DM_USER WHERE USER_ID = ?", (user_id,)).fetchone()[0]
        balance = int(balance) - fee

        # deduct fee from the user's account
        cursor.execute("UPDATE  T_DM_USER SET USER_ACCOUNT_BALANCE = ? WHERE USER_ID = ?", (balance, user_id,))

        # Show current balance
        print("Your current balance is: " + str(balance))

        # close and commit
        db.commit()
        db.close()


    def recharge(self):
        print('recharge page')
        db = sqlite3.connect('../../bicycle_db/db_file/bicycle.db')
        cursor = db.cursor()
        balance = \
            cursor.execute(
                "SELECT USER_ACCOUNT_BALANCE FROM T_DM_USER WHERE user_name='{}'".format(self.username)).fetchone()[0]
        print('Your current balance is ' + str(balance) + ' pounds')

        try:
            num = float(input('Please input the money you want to recharge: '))
            if num <= 0:
                print('Invalid number!')
                self.recharge()
            else:
                date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
                # todo: add session?
                '''update the recharge log table'''
                user_id = \
                    cursor.execute("SELECT user_id FROM T_DM_USER WHERE user_name = '{}';".format(self.username)).fetchone()[0]
                sql = "INSERT INTO T_USER_RECHARGE_LOG (user_id, recharge_date, recharge_amount) VALUES({}, '{}', {});".format(
                    user_id, date, num)
                cursor.execute(sql)
                db.commit()

                '''update the user balance '''
                sql = "UPDATE T_DM_USER SET USER_ACCOUNT_BALANCE=USER_ACCOUNT_BALANCE+{} WHERE user_name='{}';".format(num,
                                                                                                                       self.username)
                cursor.execute(sql)
                db.commit()

                '''print success message and the current balance'''
                print('You have recharged ' + str(num) + ' successfully!')
                balance = \
                    cursor.execute(
                        "SELECT USER_ACCOUNT_BALANCE FROM T_DM_USER WHERE user_id={}".format(user_id)).fetchone()[0]
                print('Your current balance is ' + str(balance) + ' pounds')
                self.menu()

        except ValueError:
            print('Please enter a number!')
            self.recharge()

        db.close()


    def reportRepair(self):
        print('repair report page')
        '''get the user id , bike id , operator id'''
        db = sqlite3.connect('../../bicycle_db/db_file/bicycle.db')
        cursor = db.cursor()

        user_id = \
            cursor.execute("SELECT user_id FROM T_DM_USER WHERE user_name = '{}';".format(self.username)).fetchone()[0]
        op_id = cursor.execute("SELECT OP_ID FROM T_DM_CITY_STATION WHERE STATION_ID={}".format(self.station)).fetchone()[0]

        '''check if there is a current rental'''
        result = cursor.execute(
            "SELECT BIC_ID , TRIP_ID FROM T_USER_RENTAL_LOG WHERE user_id={} AND end_time is NULL".format(
                user_id)).fetchone()

        if result is None:
            print('You have no current rental')
            self.menu()
        else:
            bike_id = result[0]
            trip_id = result[1]

        '''update the bike BIC_USE_STATUS and BIC_BROKEN_STATUS'''
        sql = "UPDATE T_DM_BICYCLE SET BIC_USE_STATUS=0 AND BIC_BROKEN_STATUS=1 WHERE BIC_ID={}".format(bike_id)
        cursor.execute(sql)

        '''create new repair log'''
        current_date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO T_BIC_REPAIR_LOG (bic_id, user_id, report_date, op_id, station_id, repair_status) VALUES ({}, " \
              "{}, '{}', {}, {},{})".format(bike_id, user_id, current_date, op_id, self.station, 0)
        cursor.execute(sql)

        '''update the rental log so that user do not have to pay'''
        sql = "UPDATE T_USER_RENTAL_LOG SET END_TIME='{}' , END_STATION_ID={} , TRIP_AMOUNT=0 where TRIP_ID={}".format(
            current_date, self.station, trip_id)
        cursor.execute(sql)
        db.commit()
        db.close()
        print('You have reported the bike as defective and this rental is free!')
        self.menu()


    def menu(self):
        """

        :param username: the login username used for sql
        :return:
        """

        while True:
            try:
                user_input = int(input('Enter the a number:\n'
                                       '1)Rent a bike\n'
                                       '2)Return a bike\n'
                                       '3)Report repair\n'
                                       '4)Recharge\n'
                                       '5)Quit\n'))
                if user_input == 1:
                    self.rentBike()
                elif user_input == 2:
                    self.returnBike()
                elif user_input == 3:
                    self.reportRepair()
                elif user_input == 4:
                    self.recharge()
                elif user_input == 5:
                    quit()
                else:
                    print('Invalid number')
            except ValueError:
                print('Invalid input!')


    def rent_bike_check_user_validity(self, user_id):
        has_no_ongoing_rentals = None
        has_positive_balance = None
        # check that the user has mo ongoing rentals and doesn't has a negative balance
        # connect to th db
        db = sqlite3.connect('../../bicycle_db/db_file/bicycle.db')
        cursor = db.cursor()
        # check if user has an previous rentals
        cursor.execute("SELECT end_time  FROM T_USER_RENTAL_LOG WHERE user_id = ?", (user_id,))
        all_prev_rentals = cursor.fetchall()
        has_previous_rentals = len(all_prev_rentals) > 0
        if has_previous_rentals:
            has_no_ongoing_rentals = not (None in all_prev_rentals[len(all_prev_rentals) - 1])
        else:
            has_no_ongoing_rentals = True

        # check that the user has a positive account balance
        amount = cursor.execute("SELECT USER_ACCOUNT_BALANCE FROM T_DM_USER WHERE USER_ID = ?", (user_id,)).fetchone()[0]
        has_positive_balance = (amount >= 0)

        return has_no_ongoing_rentals and has_positive_balance













