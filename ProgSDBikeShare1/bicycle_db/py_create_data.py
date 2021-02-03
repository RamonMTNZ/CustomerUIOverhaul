# -*- coding: utf-8 -*-
"""
@Time    : 2021/1/16
@Author  : Yi Yan
@File    : create_data.py
"""
import random
import pandas as pd
import math
import time
import datetime
import os
import sqlite3
import numpy as np

# parameters
user_number = 1000
op_number = 50
ma_number = 10
STATION_number = 100
bic_number = 1000
recharge_cnt = 2000
rental_cnt = 4000
repair_cnt = 1500


def random_date():
    a1 = (2020, 12, 1, 0, 0, 0, 0, 0, 0)
    a2 = (2021, 2, 20, 23, 59, 59, 0, 0, 0)
    start = time.mktime(a1)
    end = time.mktime(a2)
    t = random.randint(start, end)
    date = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(t))
    return date


def generate_random_gps(base_lon=None, base_lat=None, radius=None):
    radius_in_degrees = radius / 111300
    u = float(random.uniform(0.0, 1.0))
    v = float(random.uniform(0.0, 1.0))
    w = radius_in_degrees * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t)
    y = w * math.sin(t)
    longitude = y + base_lon
    latitude = x + base_lat
    return longitude, latitude


def cal_money(end_, start_):
    diff_sec = \
        (datetime.datetime.strptime(end_, "%Y/%m/%d %H:%M:%S") - datetime.datetime.strptime(start_, "%Y/%m/%d %H:%M:%S")).total_seconds()
    money_ = (diff_sec//60)*0.1
    if diff_sec % 60 != 0:
        money_ += 0.1
    return money_


# create data
"""
T_DM_USER
"""
# user_id
user_id = [i for i in range(1000000, 1000000+user_number)]
# user_name
li = [chr(i).lower() for i in range(ord("A"), ord("Z")+1)]
user_name = [''.join([random.choice(li) for b in range(5)]) for a in range(user_number)]
# USER_ACCOUNT_BALANCE should be calculated later
# password
user_password = [''.join([random.choice(li) for d in range(12)]) for c in range(user_number)]

"""
T_DM_MANAGER
"""
# ma_id
ma_id = [i for i in range(2000000, 2000000+ma_number)]
# ma_name
ma_name = [''.join([random.choice(li) for f in range(5)]) for e in range(ma_number)]
# password
ma_password = [''.join([random.choice(li) for h in range(12)]) for g in range(ma_number)]

"""
T_DM_OPERATOR
"""
# op_id
op_id = [i for i in range(3000000, 3000000+op_number)]
# op_name
op_name = [''.join([random.choice(li) for j in range(5)]) for i in range(op_number)]
# password
op_password = [''.join([random.choice(li) for m in range(12)]) for k in range(op_number)]

"""
T_DM_CITY_STATION
"""
# STATION_id
STATION_id = [i for i in range(4000000, 4000000+STATION_number)]
# STATION_name
STATION_name = ['LO_'+''.join([random.choice(li) for o in range(6)]) for n in range(STATION_number)]
# LON
# LAT
lon = []
lat = []
for i_1 in range(STATION_number):
    generate_ = generate_random_gps(base_lon=55.53, base_lat=4.15, radius=100000)
    lon.append(generate_[0])
    lat.append(generate_[1])
op_id_STATION = [random.choice(op_id) for i in range(STATION_number)]
STATION_capacity = [50 for i in range(STATION_number)]
# T_DM_CITY_STATION:BIC_CNT_NOW
# later

"""
T_DM_BICYCLE
"""
# BIC_ID
bic_id = [i for i in range(5000000, 5000000+bic_number)]
# STATION_id should be calculated later, according to the table T_USER_RENTAL_LOG
# bic_use_status
# bic_broken_status

"""
T_USER_RECHARGE_LOG
"""
# recharge_id
recharge_id = [i for i in range(6000000, 6000000+recharge_cnt)]
# USER_ID
user_id_recharge = [random.choice(user_id) for i in range(recharge_cnt)]
# RECHARGE_DATE
recharge_date = [random_date() for i in range(recharge_cnt)]
# RECHARGE_AMOUNT
recharge_amount = [random.randint(1, 20) for i in range(recharge_cnt)]

"""
T_USER_RENTAL_LOG
"""
# trip_id
trip_id = [i for i in range(7000000, 7000000+rental_cnt)]
user_id_trip = [random.choice(user_id) for i in range(rental_cnt)]
bic_id_trip = [random.choice(bic_id) for i in range(rental_cnt)]
start_time = [random_date() for i in range(rental_cnt)]
end_time = [datetime.datetime.strftime(datetime.datetime.strptime(start_time[i], "%Y/%m/%d %H:%M:%S") +
                                       datetime.timedelta(days=random.randint(5, 30)/1440), "%Y/%m/%d %H:%M:%S")
            for i in range(rental_cnt)]
start_STATION_id = [random.choice(STATION_id) for i in range(rental_cnt)]
end_STATION_id = [random.choice(STATION_id) for i in range(rental_cnt)]
# trip_amount: cal later according to the time, 1 minute 0.1 pound TBD

"""
T_BIC_REPAIR_LOG
"""
# repair_id
repair_id = [i for i in range(8000000, 8000000+repair_cnt)]
bic_id_repair = [random.choice(bic_id) for i in range(repair_cnt)]
user_id_repair = [random.choice(user_id) for i in range(repair_cnt)]
report_date = [random_date() for i in range(repair_cnt)]
# op_id_repair later
op_id_repair = [1 for i in range(repair_cnt)]
# STATION_id_repair later
STATION_id_repair = [1 for i in range(repair_cnt)]

repair_date = [str(datetime.datetime.strptime(start_time[i], "%Y/%m/%d %H:%M:%S") +
                   datetime.timedelta(days=random.randint(10, 72)/24)) for i in range(repair_cnt)]

# to dataframe
# T_DM_USER
df_user = pd.DataFrame([user_id, user_name, user_password]).T
df_user.columns = ['user_id', 'user_name', 'user_password']
# T_DM_OPERATOR
df_op = pd.DataFrame([op_id, op_name, op_password]).T
df_op.columns = ['op_id', 'op_name', 'op_password']
# T_DM_MANAGER
df_ma = pd.DataFrame([ma_id, ma_name, ma_password]).T
df_ma.columns = ['ma_id', 'ma_name', 'ma_password']
# T_DM_CITY_STATION
df_STATION = pd.DataFrame([STATION_id, STATION_name, lon, lat, op_id_STATION, STATION_capacity]).T
df_STATION.columns = ['STATION_id', 'STATION_name', 'lon', 'lat', 'op_id_STATION', 'STATION_capacity']
# T_DM_BICYCLE
df_bic = pd.DataFrame([bic_id]).T
df_bic.columns = ['bic_id']
# T_USER_RECHARGE_LOG
df_recharge = pd.DataFrame([recharge_id, user_id_recharge, recharge_date, recharge_amount]).T
df_recharge.columns = ['recharge_id', 'user_id_recharge', 'recharge_date', 'recharge_amount']
# T_BIC_REPAIR_LOG
df_repair = pd.DataFrame([repair_id, bic_id_repair, user_id_repair, report_date, op_id_repair, STATION_id_repair, repair_date]).T
df_repair.columns = ['repair_id', 'bic_id_repair', 'user_id_repair', 'report_date', 'op_id_repair', 'STATION_id_repair', 'repair_date']
# T_USER_RENTAL_LOG
df_trip = pd.DataFrame([trip_id, user_id_trip, bic_id_trip, start_time, end_time, start_STATION_id, end_STATION_id]).T
df_trip.columns = ['trip_id', 'user_id_trip', 'bic_id_trip', 'start_time', 'end_time', 'start_STATION_id',
                   'end_STATION_id']


"""
the last
"""
# T_BIC_REPAIR_LOG:repair_status
list_ = list(set(df_repair.bic_id_repair))
for i in range(30):
    bic_ = list_[i]
    df_bak = df_repair[df_repair.bic_id_repair == bic_]
    time_ = df_bak.report_date.max()
    if len(df_repair[(df_repair.bic_id_repair == bic_) & (df_repair.report_date == time_)]) == 1:
        index_ = df_repair[(df_repair.bic_id_repair == bic_) & (df_repair.report_date == time_)].index
        df_repair.loc[index_, 'repair_date'] = np.nan
df_repair['repair_status'] = df_repair.repair_date.apply(lambda x: 0 if pd.isna(x) else 1)
# T_USER_RENTAL_LOG:end_time
# set end_time to null random
for i in range(30):
    user_ = user_id[i]
    df_bak = df_trip[(df_trip.user_id_trip == user_) &
                     (~df_trip.user_id_trip.isin(df_repair[df_repair.repair_status == 0].bic_id_repair))]
    time_ = df_bak.end_time.max()
    if len(df_trip[(df_trip.user_id_trip == user_) & (df_trip.end_time == time_)]) == 1:
        index_ = df_trip[(df_trip.user_id_trip == user_) & (df_trip.end_time == time_)].index[0]
        df_trip.loc[index_, 'end_time'] = np.nan
        df_trip.loc[index_, 'end_STATION_id'] = np.nan
# T_USER_RENTAL_LOG: trip_amount
df_trip['trip_amount'] = \
    df_trip.apply(lambda x: cal_money(x.end_time, x.start_time) if not pd.isna(x.end_time) else np.nan, axis=1)
# T_DM_USER: USER_ACCOUNT_BALANCE
recharge_a = df_recharge[['user_id_recharge', 'recharge_amount']].groupby('user_id_recharge', as_index=False).sum()
use_a = df_trip[['user_id_trip', 'trip_amount']].groupby('user_id_trip', as_index=False).sum()
df_a = recharge_a.merge(use_a, left_on='user_id_recharge', right_on='user_id_trip', how='left')
df_a['user_account_balance'] = df_a.recharge_amount - df_a.trip_amount
df_user = df_user.merge(df_a[['user_id_recharge', 'user_account_balance']],
                        left_on='user_id', right_on='user_id_recharge', how='left')
del df_user['user_id_recharge']
df_user.user_account_balance = df_user.user_account_balance.apply(lambda x: 0 if pd.isna(x) else x)
# T_DM_BICYCLE:STATION_id, should be calculated later, according to the table T_USER_RENTAL_LOG
df_bak = df_trip.copy()
df_bak.end_STATION_id = df_bak.apply(lambda x: x.start_STATION_id if pd.isna(x.end_time) else x.end_STATION_id, axis=1)
df_bak.end_time = df_bak.end_time.fillna('2022/01/17 23:18:42')
df_bak = df_trip.groupby('bic_id_trip', as_index=False)['end_time'].max()
df_bak2 = df_trip.merge(df_bak, on=['bic_id_trip', 'end_time'], how='inner')
df_bic = df_bic.merge(df_bak2[['bic_id_trip', 'end_STATION_id']], left_on='bic_id', right_on='bic_id_trip', how='left')
del df_bic['bic_id_trip']
df_bic.columns = ['bic_id', 'STATION_id']
df_bic.STATION_id = df_bic.STATION_id.apply(lambda x: random.choice(STATION_id) if pd.isna(x) else x)
# T_DM_BICYCLE:bic_use_status
list_t = df_trip[df_trip.end_time.isna()].bic_id_trip.to_list()
df_bic['bic_use_status'] = df_bic.bic_id.apply(lambda x: 1 if x in list_t else 0)
# T_DM_BICYCLE:bic_broken_status
list_r = df_repair[df_repair.repair_date.isna()].bic_id_repair.to_list()
df_bic['bic_broken_status'] = df_bic.bic_id.apply(lambda x: 1 if x in list_r else 0)
# T_DM_CITY_STATION:BIC_CNT_NOW
df_bak = df_bic.groupby('STATION_id', as_index=False)['bic_id'].count()
df_bak.columns = ['STATION_id', 'bic_cnt_now']
df_STATION = df_STATION.merge(df_bak, on='STATION_id', how='left')

# T_BIC_REPAIR_LOG:STATION_id_repair
df_bak = df_trip[df_trip.end_time.notna()].groupby('bic_id_trip', as_index=False)['end_time'].max()
df_bak2 = df_trip.merge(df_bak, on=['bic_id_trip', 'end_time'], how='inner')
df_bak3 = df_bak2[['bic_id_trip', 'end_STATION_id']]
df_bak3.index = df_bak3.bic_id_trip
dict_ = df_bak3.end_STATION_id.to_dict()
df_repair.STATION_id_repair = df_repair.bic_id_repair.apply(lambda x: dict_[x] if x in dict_.keys() else random.choice(STATION_id))
# T_BIC_REPAIR_LOG:op_id_repair
df_bak = df_STATION.copy()
df_bak.index = df_bak.STATION_id
dict_ = df_bak.op_id_STATION.to_dict()
df_repair.op_id_repair = df_repair.STATION_id_repair.apply(lambda x: dict_[x])


# to csv
# T_DM_USER
df_user.to_csv('./raw_data/T_DM_USER.csv', index=False)
# T_DM_OPERATOR
df_op.to_csv('./raw_data/T_DM_OPERATOR.csv', index=False)
# T_DM_MANAGER
df_ma.to_csv('./raw_data/T_DM_MANAGER.csv', index=False)
# T_DM_CITY_STATION
df_STATION.to_csv('./raw_data/T_DM_CITY_STATION.csv', index=False)
# T_DM_BICYCLE
df_bic.to_csv('./raw_data/T_DM_BICYCLE.csv', index=False)
# T_USER_RECHARGE_LOG
df_recharge.to_csv('./raw_data/T_USER_RECHARGE_LOG.csv', index=False)
# T_USER_RENTAL_LOG
df_trip.to_csv('./raw_data/T_USER_RENTAL_LOG.csv', index=False)
# T_BIC_REPAIR_LOG
df_repair.to_csv('./raw_data/T_BIC_REPAIR_LOG.csv', index=False)


# insert date
conn_ = sqlite3.connect('./db_file/bicycle.db')
c_ = conn_.cursor()
file_ = os.listdir('./raw_data')
for i_file in file_:
    if i_file != 'bicycle.db':
        table_ = i_file.replace('.csv', '')
        # clear data
        sql_1 = 'delete from {};'.format(table_)
        c_.execute(sql_1)
        # insert data
        data_ = pd.read_csv('./raw_data/'+i_file)
        flag_ = '('+', '.join(['?' for i in range(data_.shape[1])])+')'
        sql_2 = 'insert into {} values {}'.format(table_, flag_)
        if i_file == 'T_DM_BICYCLE.csv':
            for i in data_.columns:
                data_[i] = data_[i].astype(str)
        c_.executemany(sql_2, data_.values)
    conn_.commit()

conn_.close()



