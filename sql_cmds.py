#methods for interacting with sql database

import sqlite3
from time import time
import pandas as pd 
import os




data = pd.read_csv('NYSE-NASDAQ-TICKERS.csv')
tickerinfo = list(data.ticker)



#UNIQUEMENTIONS FUNCTIONS

UNIQUEMENTIONSFILE = 'uniqueMentions.db'

def createUniqueMentionsdb():
    open(UNIQUEMENTIONSFILE,'w+')

#updates uniqueMentions.db
def updateUniqueMentionsFile(inputDic):
    conn = sqlite3.connect(UNIQUEMENTIONSFILE)
    c = conn.cursor()
    current_tickers = getTableNames(c)

    for ticker in inputDic.keys():
        if ticker in current_tickers:
            c.execute('SELECT username FROM "'+ ticker+'"')
            l = [item[0] for item in c.fetchall()]
            for user in inputDic[ticker]:
                if user not in l:
                    c.execute('INSERT INTO "' + ticker + '" (username) VALUES ' + '("' + user + '")')
        else:
            c.execute('CREATE TABLE "' + ticker + '" (username)')
            for user in inputDic[ticker]:
                c.execute('INSERT INTO "' + ticker + '" (username) VALUES ' +'("' + user + '")')

    conn.commit()
    conn.close()


#checks if unique mentions exists
def checkUM():
    if os.path.exists('uniqueMentions.db'):
        print('uniqueMentions.db already created')
        return True
    else:
        print('does not have uniqueMention.db')
        return False

#takes a ticker and returns an empty list if ticker is not in uniqueMentions.db else returns a list of users from that ticker
def getUniqueUsers(ticker):
    conn = sqlite3.connect('uniqueMentions.db')
    c = conn.cursor()
    list_of_tickers = getTableNames(c)
    if ticker not in list_of_tickers:
        return []
    else:
        c.execute('SELECT * FROM "' + ticker + '"')
        return [item[0] for item in c.fetchall()]



#TIME SERIES FUNCTIONS
perHourList = ['totalComments','totalPosts','uniqueComments','uniquePosts']


#creates ts databases
def createTickerTimeSeriesDB():
    for x in perHourList:
        print('creating ' + x + '.db')
    #creates 4 data bases, each with 4 tables containing 1800 columns, 
    for f in perHourList:
        open(f + '.db','w+')
        conn = sqlite3.connect(f + '.db')
        c = conn.cursor()
        for table in ['table1','table2','table3','table4']:
            c.execute('CREATE TABLE ' + table + ' (unix_time)')
        
        listindex = 0
        for table in ['table1','table2','table3','table4']:
            count = 1
            while count % 1801 != 0:
                c.execute('ALTER TABLE ' + table + ' ADD COLUMN "' + tickerinfo[listindex] + '"')
                listindex += 1
                count += 1
                if listindex == len(tickerinfo):
                    break
            if listindex == len(tickerinfo):
                break
        conn.commit()
        conn.close()


#takes in a dictionary of dictionary with tickers as keys and the mentions per hour for that hour as values
#takes in the table name to be updated, 

def updateTS(nestedDic):
    current_time = time()

    for timeseries in nestedDic.keys():
        conn = sqlite3.connect(timeseries + '.db')
        c = conn.cursor()
        for table in ['table1','table2','table3','table4']:
            col_names = getColNames(c,table)
            strinput = str(current_time) + ','
            tickers_in_dict = nestedDic[timeseries].keys()
            for ticker in col_names:
                if ticker in tickers_in_dict:
                    strinput += str(nestedDic[timeseries][ticker]) + ','
                else:
                    strinput += str(0) + ','
            strinput = strinput[:-1]
            c.execute('INSERT INTO ' + table + ' VALUES (' + strinput + ')')
        conn.commit()
        conn.close()
        

#lazy function, checks if one of ['totalComments','totalPosts','uniqueComments','uniquePosts'] exists, if it does assumes all exist
def checkTS():
    if os.path.exists('totalComments.db'):
        print('time series db already created')
        return True
    else:
        print('does not have time series db')
        return False




#HELPER FUNCTIONS

#takes in a cursor object and returns a list of table names
def getTableNames(cursor):
    cursor.execute('SELECT name from sqlite_master where type = "table"')
    return [item[0] for item in cursor.fetchall()]


#takes in a curosr object and tableName and returns a list of column names NOT INCLUDING UNIX TIME col from that table
def getColNames(cursor,tableName):
    cursor.execute('select * from ' + tableName)
    return [item[0] for item in cursor.description[1:]]



