
import os
import petl
import pymssql
import configparser
import requests
import datetime
import json
import decimal

# get data from configuration file
config = configparser.ConfigParser()
config.read('ETLDemo.ini')

# read settings from configuration file
startDate = config['CONFIG']['startDate']
url = config['CONFIG']['url']
destServer = config['CONFIG']['server']
destDatabase = config['CONFIG']['database']

# request data from URL
BOCResponse = requests.get(url+startDate)
# print (BOCResponse.text)

# initialize list of lists for data storage
BOCDates = []
BOCRates = []

# check response status and process BOC JSON object
if (BOCResponse.status_code == 200):
    BOCRaw = json.loads(BOCResponse.text)

    # extract observation data into column arrays
    for row in BOCRaw['observations']:
        BOCDates.append(datetime.datetime.strptime(row['d'],'%Y-%m-%d'))
        BOCRates.append(decimal.Decimal(row['FXUSDCAD']['v']))

    # create petl table from column arrays and rename the columns
    exchangeRates = petl.fromcolumns([BOCDates,BOCRates],header=['date','rate'])

    # print (exchangeRates)

    # load expense document
    expenses = petl.io.xlsx.fromxlsx('Expenses.xlsx',sheet='Github')

    # join tables
    expenses = petl.outerjoin(exchangeRates,expenses,key='date')

    # fill down missing values
    expenses = petl.filldown(expenses,'rate')

    # remove dates with no expenses
    expenses = petl.select(expenses,lambda rec: rec.USD != None)

    # add CDN column
    expenses = petl.addfield(expenses,'CAD', lambda rec: decimal.Decimal(rec.USD) * rec.rate)
    
    # intialize database connection
    dbConnection = pymssql.connect(server=destServer,database=destDatabase)

    # populate Expenses database table
    petl.io.todb (expenses,dbConnection,'Expenses')
    print (expenses)

