# -*- coding: utf-8 -*-
"""
@Time    : 2021/1/16
@Author  : Yi Yan
@File    : py_sql_use.py
"""
"""
# Note: 
1.When operating the insert statement of the database, the PK of each table, i.e. the first field of each table
 are left alone, I set the function to automatically find the maximum number and then add 1 when inserting data,
 so that the operation will not create the problem of duplicate ids generated.
2.All times in the database are in the format '%Y/%m/%d %H:%M:%S', str
3.The (user_name in T_DM_USER; op_name in T_DM_OPERATOR; ma_name in T_DM_MANAGER) add the limit of unique value, 
which cannot be duplicated, in order to get the user_id,op_id, and ma_id more easier.
"""
import sqlite3
import datetime
import random

conn_ = sqlite3.connect('./db_file/bicycle.db')
c_ = conn_.cursor()

# ######user
"""
I was introduced to an app and first I needed to register to use it.
"""
# --Registration
# #need columns
user_name = 'test'
user_balance = 0
user_password = 'test'
sql_ = "INSERT INTO T_DM_USER (USER_NAME, USER_ACCOUNT_BALANCE, USER_PASSWORD) VALUES('{}', {}, '{}');"\
    .format(user_name, user_balance, user_password)
c_.execute(sql_)

"""
Registration number account, I'm going to log in.
"""
# --Log in
# #need columns
user_id = 1000001
sql_ = "SELECT user_id, user_password FROM T_DM_USER WHERE user_id = {};".format(user_id)
result_ = c_.execute(sql_).fetchall()
# Verify password based on results
result_[0][1]

"""
After registering, my account balance is now at 0 and I need to top up to use it.
"""
# --recharge
# #need columns
user_id = 1000001
recharge_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/%d %H:%M:%S")
recharge_amount = 10
sql_ = "INSERT INTO T_USER_RECHARGE_LOG (user_id, recharge_date, recharge_amount) VALUES({}, '{}', {});"\
    .format(user_id, recharge_date, recharge_amount)
c_.execute(sql_)

"""
I saw a car and I'm going to use it.
"""
# --rental
# #need columns
user_id = 1000099
bic_id = 5000003
# --1. see if he has any previous orders outstanding (unreturned or unpaid cars).
sql_ = "SELECT * FROM T_USER_RENTAL_LOG WHERE user_id = {} and (end_time IS NULL OR trip_amount IS NULL);"\
    .format(user_id)
result_ = c_.execute(sql_).fetchall()
# ###If len(result_)==0, then the car can be borrowed, otherwise an error is reported
if len(result_) != 0:
    print('Please complete your previous order first.')

# --2.See if the car he is borrowing is broken or has an outstanding (unpaid) previous order for that car
# if unpaid
sql_ = "SELECT * FROM T_USER_RENTAL_LOG WHERE bic_id = {} and (end_time IS NULL OR trip_amount IS NULL);"\
    .format(bic_id)
result_ = c_.execute(sql_).fetchall()
if len(result_) != 0:
    print('The previous order for this vehicle has not been completed, please use another bicycle..')
# if broken
sql_ = "SELECT * FROM T_DM_BICYCLE WHERE bic_id = {} and bic_broken_status = 1;".format(bic_id)
result_ = c_.execute(sql_).fetchall()
if len(result_) != 0:
    print('This car is broken down, please use another car.')
# --3.Once all the above verifications have been passed, it will show that the loan of the car was successful.
# ##and insert the usage information into the table T_USER_RENTAL_LOG.

# # need_columns
start_time = datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/%d %H:%M:%S")
# -- get start_STATION_id
sql_STATION = """SELECT STATION_ID FROM T_DM_BICYCLE WHERE BIC_ID = {};""".format(bic_id)
result_STATION = c_.execute(sql_STATION).fetchall()
# --insert rental to T_USER_RENTAL_LOG
sql_insert = """INSERT INTO T_USER_RENTAL_LOG (user_id, bic_id, start_time, start_STATION_id) 
                VALUES ({}, {}, '{}', {})""".format(user_id, bic_id, start_time, result_STATION[0][0])
c_.execute(sql_insert)
# --update T_DM_BICYCLE
sql_update = """UPDATE T_DM_BICYCLE SET bic_use_status = 1 where bic_id = {}""".format(bic_id)
c_.execute(sql_update)


"""
I arrived at my destination ready to return the car.
"""
# #need columns
user_id = 1000099
bic_id = 5000003
end_STATION_id = 4000009
end_time = datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/%d %H:%M:%S")
"""
add --2021.1.20
"""
# --1.the STATION is available
sql_get = """SELECT STATION_CAPACITY, BIC_CNT_NOW FROM T_DM_CITY_STATION WHERE bic = {}""".format(bic_id)
result_ = c_.execute(sql_get).fetchall()
if result_[0][1] == result_[0][0]:
    print("It's not available")
# --1.get trip_id
sql_get_trip_id = """SELECT trip_id FROM T_USER_RENTAL_LOG WHERE user_id = {} AND end_time is null;""".format(user_id)
trip_id = c_.execute(sql_get_trip_id).fetchall()[0][0]
# --2.end the trip
sql_end_trip = """UPDATE T_USER_RENTAL_LOG SET end_time = '{}', end_STATION_id = {} WHERE trip_id = {};"""\
    .format(end_time, end_STATION_id, trip_id)
c_.execute(sql_end_trip)
# --3.Payments
def cal_money(end_, start_):
    diff_sec = \
        (datetime.datetime.strptime(end_, "%Y/%m/%d %H:%M:%S") - datetime.datetime.strptime(start_, "%Y/%m/%d %H:%M:%S")).total_seconds()
    money_ = (diff_sec//60)*0.1
    if diff_sec % 60 != 0:
        money_ += 0.1
    return money_


# ##get trip_id
sql_get_trip_id = """SELECT trip_id FROM T_USER_RENTAL_LOG WHERE user_id = {} AND trip_amount is null;""".format(user_id)
trip_id = c_.execute(sql_get_trip_id).fetchall()[0][0]
# ##cal amount
sql_get_time = """SELECT start_time, end_time FROM T_USER_RENTAL_LOG WHERE trip_id = {};""".format(trip_id)
get_time = c_.execute(sql_get_time).fetchall()
amount_ = round(cal_money(get_time[0][1], get_time[0][0]), 1)
# ##update T_USER_RENTAL_LOG
sql_pay = """UPDATE T_USER_RENTAL_LOG SET trip_amount = {} WHERE trip_id = {};""".format(amount_, trip_id)
c_.execute(sql_end_trip)
c_.execute("""select * from T_USER_RENTAL_LOG where user_id=1000099""").fetchall()
# --4.update T_DM_BICYCLE
sql_update = """UPDATE T_DM_BICYCLE SET bic_use_status = 0 where bic_id = {}""".format(bic_id)
c_.execute(sql_update)


"""
I noticed that a car had broken down and I will report it.
"""
# #need columns
bic_id = 5000003
# --1.Check if the vehicle is in use, it is not reportable if it is in use.
sql_check = """SELECT BIC_USE_STATUS, BIC_BROKEN_STATUS FROM T_DM_BICYCLE WHERE BIC_ID = {}""".format(bic_id)
result_check = c_.execute(sql_check).fetchall()
if result_check[0][0] == 1:
    print('This bicyble has not completed its previous order, please report it when you have finished.')
elif result_check[0][1] == 1:
    print('The vehicle has been reported as faulty, please wait for repairs.')
else:
    pass
# --2.If the above checks pass, the maintenance record is inserted into the table.
# It is currently randomly generated.
report_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/%d %H:%M:%S")
result_op_id = c_.execute("""SELECT OP_ID FROM T_DM_OPERATOR""").fetchall()
op_id = random.choice([i[0] for i in result_op_id])
repair_status = 0
sql_ = """INSERT INTO T_BIC_REPAIR_LOG (bic_id, user_id, report_date, op_id, repair_status) 
        VALUES ({}, {}, '{}', {}, {})""".format(bic_id, user_id, report_date, op_id, repair_status)
c_.execute(sql_)
# --3.Change T_DM_BICYCLE:bic_broken_status
sql_update = """UPDATE T_DM_BICYCLE SET bic_broken_status = 1 WHERE bic_id = {}""".format(bic_id)
c_.execute(sql_update)



conn_.commit()
conn_.close()