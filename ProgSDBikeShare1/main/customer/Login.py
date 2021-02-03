"""
the log in and register page
"""
import random
import sqlite3
from main.customer.customer import Customer


def login(entry1, entry2):
    name = entry1.get()
    password = entry2.get()

    db = sqlite3.connect('../../bicycle_db/db_file/bicycle.db')
    cursor = db.cursor()
    sql = "SELECT user_password FROM T_DM_USER WHERE user_name = {};".format("'" + name + "'")
    if password == cursor.execute(sql).fetchone()[0]:
        station_id = assign_nearest_station(get_user_location())
        print('Welcome ' + name)
        # cust = Customer(name, station_id)
        # cust.menu()
        valid_user = True
    else:
        print('Wrong id or password!')
        valid_user = False
    db.close()
    return valid_user


def register():
    name = input('Please input your username: ')
    password = input('Please input your password: ')



    db = sqlite3.connect('../../bicycle_db/db_file/bicycle.db')
    cursor = db.cursor()
    sql = "SELECT * FROM T_DM_USER WHERE user_name = {};".format(name)
    result = cursor.execute(sql).fetchone()
    # make sure the name is unique
    if not result:
        sql = "INSERT INTO T_DM_USER (USER_NAME, USER_ACCOUNT_BALANCE, USER_PASSWORD) VALUES('{}', {}, '{}');" \
            .format(name, 0, password)
        cursor.execute(sql)
        db.commit()
    else:
        print('username already exits!')
        menu()
    db.close()
    menu()


def menu():
    while True:
        try:
            user_input = int(input('Enter a number\n'
                                   '1)Register\n'
                                   '2)Log in\n'
                                   '3)quit\n'))
            if user_input == 1:
                register()
            elif user_input == 2:
                login()
            elif user_input == 3:
                quit()
            else:
                print('Invalid number!')
        except ValueError:
            print('Invalid input, please enter a number!')


def get_user_location():
    # connect to db
    db = sqlite3.connect('../../bicycle_db/db_file/bicycle.db')
    cursor = db.cursor()
    # get all station info
    station_info = cursor.execute("SELECT * FROM T_DM_CITY_STATION").fetchall()
    # store all the lat and lon info
    lat = []
    lon = []
    for item in station_info:
        lat.append(item[2])
        lon.append(item[3])
    lat.sort()
    lon.sort()
    # get the biggest and smallest lon and lat
    smallest_lat = lat[0]
    smallest_lon = lon[0]
    biggest_lat = lat[len(lat)-1]
    biggest_lon = lon[len(lon) - 1]
    # set those as the ranges for the user location
    user_lat = random.uniform(smallest_lat, biggest_lat)
    user_lon = random.uniform(smallest_lon, biggest_lon)
    return(user_lat,user_lon)


def assign_nearest_station(location_info):
    db = sqlite3.connect('../../bicycle_db/db_file/bicycle.db')
    cursor = db.cursor()
    # get all station info
    station_info = cursor.execute("SELECT * FROM T_DM_CITY_STATION").fetchall()
    # store distance from user
    distance_from_user = []
    for item in station_info:
        distance_from_user.append(abs(item[2] - location_info[0]) + abs(item[3]-location_info[1]))
    # get index of smallest value
    smallest = 100
    index = None
    for item in distance_from_user:
        if item < smallest:
            smallest = item
            index = distance_from_user.index(item)
    # get list of all stations
    all_stations = cursor.execute("SELECT * FROM T_DM_CITY_STATION").fetchall()
    # use index to get closest station
    station_id = all_stations[index][0]
    return station_id



if __name__ == "__main__":
    menu()