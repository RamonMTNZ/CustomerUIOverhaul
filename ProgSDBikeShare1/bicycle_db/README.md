__NOTE: Modify 2021.1.28__  
1. set all the time format to "%Y-%m-%d %H:%M:%S" -- Manos
2. Increase the amount of reporting times in one day -- Manos


__NOTE: Modify 2021.1.27__  

1. reset parameters as follow：--Liefeng Xiao
user_number = 300  
op_number = 8  
ma_number = 2  
STATION_number = 16  
bic_number = 200  
recharge_cnt = 700   
rental_cnt = 6000    
repair_cnt = 500   
  
2. reset the end_time in table T_USER_RENTAL_LOG ：--Fang Li
The most recent time is '2021-1-27 23:59:59'  

__NOTE: Modify 2021.1.26__  

1. update the bicycle.db, the lon and lat of the stations are corresponding to the lon and lat of Glasgow's metro and schools. There are 16 stations in total.

__NOTE: Modify 2021.1.22__  

1. change the location to station in the database 
2.T_DM_CITY_STATION: station_capicity can be empty, which means you can ignore this field, and I will delete it when we are sure we don't need it anymore

__NOTE: Modify 2021.1.20__  

# 1.Added the restriction of unique user names
The (user_name in T_DM_USER; op_name in T_DM_OPERATOR; ma_name in T_DM_MANAGER) add the limit of unique value, 
which cannot be duplicated, in order to get the user_id op_id ma_id more easier. 

# 2.Add three columns into T_DM_CITY_LOCATION
(1)
OP_ID: This column means : which operator is responsible for the location.This reduces the hassle of how to assign to which operator when the bicycle was broken.
(2)
LOCATION_CAPACITY: the maximum capacity of the location, when the the number of bicycle equls to it, other bicycles won't be park here.
(3)
BIC_CNT_NOW: the number of bicycle in the location now


# 3.Add one columns into T_BIC_REPAIR_LOG
LOCATION_ID: when the bicycle is broken, the location_id is where the location you park it in. And the operator can find it more easier.

# 4.columns comments
Because some columns indicating status aren't very clear, I write the comment in the bicycle.pdf, same as below

**T_DM_BICYCLE:**
BIC_USE_STATUS: 0->not use  ;1-> using
BIC_BROKEN_STATUS: 0->not broken ;1-> broken

**T_BIC_REPAIR_LOG:**
T_BIC_REPAIR_LOG: 0->not repair;1-> have repaired


# 5.in file py_sql_operator.py
I add the sql statements about 
(1)how to add a new bicycle 
and
(2)how to add a new location


6.in file py_sql_user.py
I add the sql statements about
(1)before the user end the trip, we should make sure that the the number of the location is full or not 



__NOTE2: you can start by looking at the readme.md file and the bicycle.pdf under and model_design files.__  

# PYs

**py_sql_manager.py**  
**py_sql_operator.py**  
**py_sql_use.py**  
#### Presentation
1.Give the call method for each function to the back end.  
2.I have written how each function of the corresponding module should call the database in the corresponding three files.  
3.These are the functions I can think of and if I have missed any, I will add them.

**py_create_data.py**  
#### Presentation
Create new data.
Note: As the data is generated randomly, it will be different each time it is executed, so please execute it carefully

**py_create_table.py**  
#### Presentation
Create the db file and also create the required tables;
It only needs to be executed when the system environment is completely new.
If there is already a db file, it does not need to be executed

# Files

**db_file**  
#### Presentation
Storing db files
#### Files, including datas
*bicycle.db*

**model_design**  
#### Presentation
Storing model design files
#### Files
*bicycle.ndm*  ##open it by Navicat, can generate sql statements directly
*bicycle.pdf*

**raw_data**  
#### Presentation
raw data for this system, create by py_create_data.py
For data verification quickly in case of errors.
#### Files
*csv file of the database name*










