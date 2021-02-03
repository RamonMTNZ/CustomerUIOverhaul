# -*- coding: utf-8 -*-
"""
@Time    : 2021/1/16
@Author  : Yi Yan
@File    : py_sql_oprator.py
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

"""
Functions:
Track the STATION of all bikes in the city. (3 marks)
Repair a defective bike. ( 1 marks)
move bikes to different STATIONs around the city asneeded. ( 2marks)
"""
import sqlite3
import datetime
import random

conn_ = sqlite3.connect('./db_file/bicycle.db')
c_ = conn_.cursor()

# ######oprator
"""
Registration
"""
# #need columns
op_name = 'test'
op_password = 'test'
sql_ = "INSERT INTO T_DM_OPERATOR (op_name, op_password) VALUES('{}', '{}');"\
    .format(op_name, op_password)
c_.execute(sql_)

"""
Log in
"""
# #need columns
op_id = 3000011
sql_ = "SELECT op_id, op_password FROM T_DM_OPERATOR WHERE op_id = {};".format(op_id)
result_ = c_.execute(sql_).fetchall()
# Verify password based on results
result_[0][1]


"""
Track the STATION of all bikes in the city. (3 marks)
"""
# #need columns
bic_id = 5000003

sql_ = """SELECT A.bic_id, A.STATION_id, B.lon, B.lat FROM T_DM_BICYCLE A INNER JOIN T_DM_CITY_STATION B ON 
            A.STATION_ID = B.STATION_ID WHERE A.bic_id = {} ;""".format(bic_id)
result_ = c_.execute(sql_).fetchall()


"""
Repair a defective bike. ( 1 marks)
"""
# #need columns
op_id = 3000011
repair_id =8000000
# -- The page shows all vehicles in need of repair for this operator.
sql_to_to = """SELECT * FROM T_BIC_REPAIR_LOG WHERE op_id = {}""".format(op_id)
result_to_do = c_.execute(sql_to_to).fetchall()


# --Select a repair_id to repair
# --1.Insert repair time and modify order status
repair_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/%d %H:%M:%S")
sql_update = """UPDATE T_BIC_REPAIR_LOG SET repair_date = '{}', repair_status =1 WHERE repair_id = {}""".format(repair_date, repair_id)
c_.execute(sql_update)
# --2.Change T_DM_BICYCLE:bic_broken_status
sql_update = """UPDATE T_DM_BICYCLE SET bic_broken_status = 0 WHERE bic_id = {}""".format(bic_id)
c_.execute(sql_update)

"""
move bikes to different STATIONs around the city asneeded. ( 2marks)
"""
bic_id = 5000003
new_STATION_id = 4000015
sql_ = """UPDATE T_DM_BICYCLE SET STATION_id = {} WHERE bic_id = {}; """.format(new_STATION_id, bic_id)
c_.execute(sql_)


"""
how to add a new bicycle
add --2021.1.20
"""
# ##need columns
STATION_id = 123
bic_user_status = 0
bic_broken_status = 0

sql_ = """INSERT INTO T_DM_BICYCLE(STATION_id, bic_user_status, bic_broken_status) VALUES ({}, {}, {})"""\
    .format(STATION_id, bic_user_status, bic_broken_status)

c_.execute(sql_)

"""
how to add a new STATION
add --2021.1.20
"""
# ##need columns
STATION_name = 'test'
lon = 123
lat = 123
op_id = 123
STATION_capacity = 50
bic_cnt_now = 0

sql_ = """INSERT INTO T_DM_CITY_STATION(STATION_name, lon, lat, op_id, STATION_capacity, bic_cnt_now) VALUES 
        ('{}', {}, {}, {}, {})""".format(STATION_name, lon, lat, op_id, STATION_capacity, bic_cnt_now)
c_.execute(sql_)

conn_.commit()
conn_.close()