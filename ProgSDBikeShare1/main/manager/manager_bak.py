import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geopandas
from mpl_toolkits.basemap import Basemap
import os


class mananger():

    # Initial fields for sql path and date
    def __init__(self):
        self.sql_path = os.path.join(os.path.dirname(__file__), "..", "..", "bicycle_db", "db_file", "bicycle.db")
        self.start = "2020/12"
        self.end = "2021/03"

    # The connection with database
    def connect(self, sql):
        """
        Connection of database of bicycle
        """
        with sqlite3.connect(self.sql_path) as db:
            tmp = pd.read_sql_query(sql, db)
        return tmp

    # show the plot with bar and geo map between the date
    def starting_population(self):
        """
        show the popular station by starting point.
        """
        # get station name and count the number of each station by join city_station table
        sql = f"SELECT COUNT(START_STATION_ID) as Number , STATION_NAME as Name from " \
              f"T_USER_RENTAL_LOG JOIN T_DM_CITY_STATION ON  T_DM_CITY_STATION.STATION_ID =  " \
              f"T_USER_RENTAL_LOG.START_STATION_ID WHERE START_TIME BETWEEN '{self.start} 'AND '{self.end}' " \
              f"GROUP BY START_STATION_ID  ORDER BY Number DESC LIMIT 10"
        # print(sql)
        tmp = self.connect(sql)
        plt.bar(tmp['Name'], tmp['Number'])
        plt.xticks(fontsize=5)
        plt.grid(True)

        # get the lon and lat and number to show on the map
        sql = f"SELECT LON,LAT, COUNT(START_STATION_ID) as Number from T_USER_RENTAL_LOG JOIN T_DM_CITY_STATION " \
              f"ON  T_DM_CITY_STATION.STATION_ID =  T_USER_RENTAL_LOG.START_STATION_ID " \
              f"WHERE START_TIME BETWEEN '{self.start}' AND '{self.end}' GROUP BY START_STATION_ID"

        tmp = self.connect(sql)

        df = geopandas.read_file('CA_2011_EoR_Glasgow_City.shp')
        df = df.to_crs(epsg=4326)

        df.plot(edgecolors='black')
        # Map (long, lat) to (x, y) for plotting
        plt.scatter(tmp['LAT'], tmp['LON'], (50 * tmp['Number'] / np.mean(tmp['Number'])), c='red', alpha=0.5,
                    zorder=10)
        # m.scatter(tmp['LAT'], tmp['LON'], tmp['Number'] ** 2, c='red', alpha=0.5, zorder=10)
        plt.show()

    # show the plot with bar and geo map between the date of end station
    def ending_population(self):
        """
                show the popular station by ending point.
        """

        # get station name and count the number of each station by join city_station table
        sql = f"SELECT END_STATION_ID as ID, COUNT(END_STATION_ID) as Number , STATION_NAME as Name from " \
              f"T_USER_RENTAL_LOG JOIN T_DM_CITY_STATION ON  T_DM_CITY_STATION.STATION_ID =  " \
              f"T_USER_RENTAL_LOG.END_STATION_ID WHERE START_TIME BETWEEN {self.start} AND {self.end} " \
              f"GROUP BY END_STATION_ID  ORDER BY Number DESC LIMIT 10"
        tmp = self.connect(sql)

        # get the lon and lat and number to show on the map
        sql = f"SELECT LON,LAT, COUNT(END_STATION_ID) as Number from T_USER_RENTAL_LOG JOIN T_DM_CITY_STATION " \
              f"ON  T_DM_CITY_STATION.STATION_ID =  T_USER_RENTAL_LOG.START_STATION_ID " \
              f"WHERE END_TIME BETWEEN '{self.start}' AND '{self.end}' GROUP BY END_STATION_ID"

        tmp = self.connect(sql)
        df = geopandas.read_file('CA_2011_EoR_Glasgow_City.shp')
        df = df.to_crs(epsg=4326)

        df.plot(edgecolors='black')
        # Map (long, lat) to (x, y) for plotting
        plt.scatter(tmp['LAT'], tmp['LON'], (50 * tmp['Number'] / np.mean(tmp['Number'])), c='red', alpha=0.5,
                    zorder=10)
        # m.scatter(tmp['LAT'], tmp['LON'], tmp['Number'] ** 2, c='red', alpha=0.5, zorder=10)
        plt.show()

    def top_user(self):
        """
                show the who is the biggest customer for us by usage
        """

        # get the data form rental table and
        sql = f"SELECT COUNT(T_USER_RENTAL_LOG.USER_ID) as Number , USER_NAME as Name from T_USER_RENTAL_LOG " \
              f"JOIN T_DM_USER ON  T_DM_USER.USER_ID =  T_USER_RENTAL_LOG.USER_ID " \
              f"WHERE START_TIME BETWEEN {self.start} AND {self.end} " \
              f"GROUP BY T_USER_RENTAL_LOG.USER_ID  " \
              f"ORDER BY Number DESC LIMIT 10"
        tmp = self.connect(sql)

        plt.bar(tmp['Name'], tmp['Number'])
        plt.xticks(fontsize=5)
        plt.grid(True)
        plt.show()

    def spent_most(self):
        """
                show the who is the biggest customer for us by money
        """

        sql = f"SELECT SUM(TRIP_AMOUNT) as Money  , USER_NAME as Name from T_USER_RENTAL_LOG JOIN T_DM_USER " \
              f"ON  T_DM_USER.USER_ID =  T_USER_RENTAL_LOG.USER_ID WHERE START_TIME BETWEEN {self.start} AND {self.end} " \
              f"GROUP BY T_USER_RENTAL_LOG.USER_ID  ORDER BY Money DESC LIMIT 10"

        tmp = self.connect(sql)

        plt.bar(tmp['Name'], tmp['Money'])
        plt.xticks(fontsize=5)
        plt.grid(True)
        plt.show()

    # def geo_report(self):
    #     date = self.date()
    #
    #     sql = f"SELECT LON,LAT, COUNT(START_STATION_ID) as Number from T_USER_RENTAL_LOG JOIN T_DM_CITY_STATION " \
    #           f"ON  T_DM_CITY_STATION.STATION_ID =  T_USER_RENTAL_LOG.START_STATION_ID WHERE START_TIME" \
    #           f" BETWEEN {date[0]} AND {date[1]} GROUP BY START_STATION_ID"
    #
    #     tmp = self.connect(sql)
    #
    #     df = geopandas.read_file('CA_2011_EoR_Glasgow_City.shp')
    #     df = df.to_crs(epsg=4326)
    #
    #     df.plot(edgecolors='black')
    #     # Map (long, lat) to (x, y) for plotting
    #     plt.scatter(tmp['LAT'], tmp['LON'], (50 * tmp['Number'] / np.mean(tmp['Number'])), c='red', alpha=0.5,
    #                 zorder=10)
    #     # m.scatter(tmp['LAT'], tmp['LON'], tmp['Number'] ** 2, c='red', alpha=0.5, zorder=10)
    #     plt.show()

    # make date to the right format
    def select_date(self):
        start_year = input("starting year ")
        start_month = input("starting month ")
        end_year = input("ending year ")
        end_month = input("ending month ")
        if int(start_month) < 10:
            start_month = "0" + start_month[-1]
        if int(end_month) < 10:
            end_month = "0" + end_month[-1]
        self.start = start_year + "\\" + start_month
        self.end = end_year + "\\" + end_month

    def monthly_report(self):
        sql = "SELECT  count(TRIP_ID) as Number , substr(START_TIME ,6,2)||substr(START_TIME ,1,4) as Date," \
              "SUM(TRIP_AMOUNT)as money FROM T_USER_RENTAL_LOG " \
              "GROUP BY (substr(START_TIME ,6,2)||substr(START_TIME ,1,4))"
        tmp = self.connect(sql)

        plt.plot(tmp['Date'], tmp['Number'], marker='o', mfc='black', linewidth=4)
        plt.plot(tmp['Date'], tmp['money'], 'orange', marker='o', mfc='black', linewidth=4)

        sql = "SELECT  count(REPAIR_ID) as Number , substr(REPORT_DATE ,6,2)||substr(REPORT_DATE ,1,4) as Date " \
              "FROM T_BIC_REPAIR_LOG GROUP BY (substr(REPORT_DATE ,6,2)||substr(REPORT_DATE ,1,4))"
        tmp = self.connect(sql)
        plt.plot(tmp['Date'], tmp['Number'], 'red', marker='o', mfc='black')
        plt.legend(['Rent frequency', 'Profit', 'Report'], loc=1)
        plt.show()

    def yearly_report(self):
        sql = "SELECT  count(TRIP_ID) as Number , substr(START_TIME ,1,4) as Date " \
              "FROM T_USER_RENTAL_LOG GROUP BY substr(START_TIME ,1,4)"
        tmp = self.connect(sql)

        plt.plot(tmp['Date'], tmp['Number'], marker='o', mfc='black', linewidth=4)
        plt.show()

    def operator_efficiency(self):
        sql = "SELECT  count(REPAIR_ID) as Number ,OP_NAME FROM T_BIC_REPAIR_LOG JOIN T_DM_OPERATOR " \
              "ON T_DM_OPERATOR.OP_ID =  T_BIC_REPAIR_LOG.OP_ID GROUP BY T_BIC_REPAIR_LOG.OP_ID"
        tmp = self.connect(sql)

        plt.pie(tmp['Number'], labels=tmp['OP_NAME'], autopct='%1.1f%%')
        plt.axis('equal')
        plt.show()

    def test(self):
        sql = "SELECT  count(REPAIR_ID) as Number ,OP_NAME FROM T_BIC_REPAIR_LOG JOIN T_DM_OPERATOR " \
              "ON T_DM_OPERATOR.OP_ID =  T_BIC_REPAIR_LOG.OP_ID GROUP BY T_BIC_REPAIR_LOG.OP_ID"
        tmp = self.connect(sql)
        return tmp

    def menu(self):
        """
        menu for option
        """

        print("1) show the starting station population")
        print("2) show the ending station population")
        print("3) show the top costumer who rent the most time")
        print("4) show the top costumer spent the most time")
        print("5) show the sales monthly report")
        print("6) show the sales yearly report")
        print("7) show the efficiency of operators")
        print("8) Select the date")

        selections = input()
        if selections == "1":
            self.starting_population()
        elif selections == "2":
            self.ending_population()
        elif selections == "3":
            self.top_user()
        elif selections == "4":
            self.spent_most()
        elif selections == "5":
            self.monthly_report()
        elif selections == "6":
            self.yearly_report()
        elif selections == "7":
            self.operator_efficiency()
        elif selections == "8":
            self.select_date()
        else:
            print("try again")
        pass


if __name__ == "__main__":
    m = mananger()
    while True:
        m.menu()
