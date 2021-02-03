# -*- coding: utf-8 -*-
"""
@Time    : 2021/1/16
@Author  : Yi Yan
@File    : sql_demo.py
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

# ######manager
"""
Registration
"""
# #need columns
ma_name = 'test'
ma_password = 'test'
sql_ = "INSERT INTO T_DM_MANAGER (ma_name, ma_password) VALUES('{}', '{}');"\
    .format(ma_name, ma_password)
c_.execute(sql_)

"""
Log in
"""
# #need columns
ma_id = 2000000
sql_ = "SELECT ma_id, ma_password FROM T_DM_MANAGER WHERE ma_id = {};".format(ma_id)
result_ = c_.execute(sql_).fetchall()
# Verify password based on results
result_[0][1]

conn_.commit()
conn_.close()

"""
This module is a visualization, tell me when you need it and I'll write the sql
"""