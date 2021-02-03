# -*- coding: utf-8 -*-
"""
@Time    : 2021/1/16
@Author  : Yi Yan
@File    : create_table.py
"""
import sqlite3

conn_ = sqlite3.connect('./db_file/bicycle.db')
c_ = conn_.cursor()
# create table
c_.execute("""CREATE TABLE T_DM_CITY_STATION (
STATION_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
STATION_NAME varchar(50) NOT NULL,
LON float NOT NULL,
LAT float NOT NULL,
OP_ID doublt NOT NULL,
STATION_CAPACITY double,
BIC_CNT_NOW double NOT NULL
);""")

c_.execute("""CREATE TABLE T_DM_BICYCLE (
BIC_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
STATION_ID double NOT NULL,
BIC_USE_STATUS tinyint NOT NULL,
BIC_BROKEN_STATUS tinyint NOT NULL
);""")

c_.execute("""CREATE TABLE T_DM_USER (
USER_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
USER_NAME varchar(50) NOT NULL unique,
USER_PASSWORD varchar(50) NOT NULL,
USER_ACCOUNT_BALANCE double NOT NULL
);""")

c_.execute("""CREATE TABLE T_DM_OPERATOR (
OP_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
OP_NAME varchar(50)  NOT NULL unique,
OP_PASSWORD varchar(50) NOT NULL
);""")

c_.execute("""CREATE TABLE T_DM_SYS_FILE (
FILE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
FILE_STATION varchar(255) NOT NULL,
DESC varchar(255) NULL
);""")

c_.execute("""CREATE TABLE T_USER_RENTAL_LOG (
TRIP_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
USER_ID double NOT NULL,
BIC_ID double NOT NULL,
START_TIME varchar(255) NOT NULL,
END_TIME varchar(255) NULL,
START_STATION_ID double NULL,
END_STATION_ID double NULL,
TRIP_AMOUNT double NULL
);""")

c_.execute("""CREATE TABLE T_USER_RECHARGE_LOG (
RECHARGE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
USER_ID double NOT NULL,
RECHARGE_DATE varchar(255) NULL,
RECHARGE_AMOUNT double NOT NULL
);""")

c_.execute("""CREATE TABLE T_BIC_REPAIR_LOG (
REPAIR_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
BIC_ID double NOT NULL,
USER_ID double NOT NULL,
REPORT_DATE varchar(255) NOT NULL,
OP_ID double NOT NULL,
STATION_ID double NOT NULL,
REPAIR_DATE varchar(255) NULL,
REPAIR_STATUS tinyint NOT NULL
);""")

c_.execute("""CREATE TABLE T_DM_MANAGER (
MA_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
MA_NAME varchar(50) NOT NULL unique,
MA_PASSWORD varchar(50) NOT NULL
);""")
conn_.commit()
conn_.close()