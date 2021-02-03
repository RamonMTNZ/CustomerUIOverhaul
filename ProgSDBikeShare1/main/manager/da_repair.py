import sqlite3
from sqlite3.dbapi2 import Timestamp
import matplotlib.pyplot as plt
import os
import datetime
import pandas as pd

#### UTILITY ####

REPAIR_DB = "T_BIC_REPAIR_LOG"


# Forces the user to select one out of a collection of possible options
def getSelection(possibleOptions):
    select = input("Your choice: ")
    while select not in possibleOptions:
        print(f"Invalid option. Please select a number between 1 and {len(possibleOptions)}: ", end="")
        select = input()
    return select


# makes sure the user selected a valid date
def selectDate():
    # uses datetime to check if unput is correct
    valid = False
    while not valid:
        try:
            date = datetime.datetime(int(input("Enter year: ")),
                                     int(input("Enter month: ")),
                                     int(input("Enter day: ")))

            valid = True  # correct date
        except ValueError as e:
            print(e)

    return date


# run any sql query against database and return results
def runSQL(sql: str):
    # always finds the correct path to the database file
    DB_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "bicycle_db", "db_file", "bicycle.db")

    with sqlite3.connect(DB_FILE) as db:
        cr = db.cursor()

    # run query and return results
    cr.execute(sql)
    results = cr.fetchall()
    db.close()

    return results


def mapDateToDays(x):
    dateMs = datetime.date


#### ANALYTICS #####


# statistics about reports
def reports():
    print("""\n\nSelect an option from the menu:
    1. Daily analysis
    2. Hourly analysis
    3. Back""")

    select = getSelection(["1", "2", "3"])

    if select == "1":
        # Daily analysis
        print("~~Enter start date~~")
        start_date = selectDate()

        print("~~Enter end date~~")
        end_date = selectDate()

        # GET repaidID and report date from repair log between the dates of interest and ordered by date
        response = runSQL("SELECT REPAIR_ID, REPORT_DATE FROM " + REPAIR_DB + \
                          " WHERE REPORT_DATE BETWEEN '" + \
                          start_date.strftime("%Y/%m/%d %H:%M:%S") + \
                          "' AND '" + \
                          end_date.strftime("%Y/%m/%d %H:%M:%S") + \
                          "' ORDER BY REPORT_DATE")

        # Map reports to days
        res = pd.DataFrame(response, columns=['id', 'date'])
        res['date'] = res['date'].map(lambda x: (datetime.datetime.strptime(x,
                                                                            '%Y/%m/%d %H:%M:%S').timestamp() - start_date.timestamp()) // 86400)

        # count each day's reports
        results = res.groupby('date').count()
        x = [datetime.datetime.fromtimestamp(start_date.timestamp() + int(d) * 86400).strftime("%Y-%m-%d") for d in
             results.index]

        # plot results
        plt.subplot(211)
        plt.bar(x, results['id'], )
        plt.ylabel = "# Reports"
        plt.xlabel = "Days"
        plt.xticks(x, rotation="vertical")
        plt.show()



    elif select == "2":
        # TODO: hourly analysis
        print("!!!!!!!TODO")

    # go back to menu after completion
    menu()


# statistics about biks
def bikes():
    # TODO
    print("!!!!!!!!!!TODO")

    # go back to menu after completion
    menu()


#### MAIN ####

# main menu for repair statistics
def menu():
    print("""\n\n~~REPAIR STATISTICS~~
Select an option from the menu:
    1. Statistics about the defectiveness reports
    2. Statistics about the bicycles
    3. Back""")

    select = getSelection(["1", "2", "3"])

    # run corresponding function
    if select == "1":
        reports()
    elif select == "2":
        bikes()
    else:
        return


if __name__ == "__main__":
    menu()
