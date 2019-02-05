#! /usr/bin/env python3

import os
import sys
from bs4 import BeautifulSoup
import mysql.connector

# Default username and password for my machine.
# Change it according to yours.
MYSQL_USER = 'root'
MYSQL_PASSWD = 'xclaim'

def get_data_from_row(row):
    # Each of the table row has two spans
    # One holds the key value and other holds the data
    span_of_row = row.find_all('span')
    return (span_of_row[0].get_text(),span_of_row[1].get_text())

if __name__ == "__main__":
    

    soup = None
    list_of_data = list()
    
    # Run only if input html file is provided
    if len(sys.argv) > 1:

        with open(sys.argv[1]) as fp:
            soup = BeautifulSoup(fp, 'html.parser')
        table = soup.find('tbody')
        rows = table.find_all('tr')
        
        # (2, 14, 19, 27) corresponds to the table rows
        # from where the data is to be scrapped.
        for i in (2, 14, 19, 27):
            list_of_data.append(get_data_from_row(rows[i]))
        
        # Span for test result can be checked with the class name.
        result = soup.find('span',{'class':'diags_testrunning_testresulttext_PASS'}).get_text()
        list_of_data.append(('Result', result))
        
        # There are may tables with the same class.
        # 5th number of the table corresponds to math test register. 
        math_test_table = soup.find_all('table',{'class':'diags_deviceInfoDialog_detailedSysinfoPane_testTable'})[4]
        math_register_test = math_test_table.find_all('th')
        list_of_data.append((math_register_test[0].get_text(),math_register_test[1].get_text()))
        
        # Mysql connection to start a connection
        # The default username and password are used here.
        # Could be passed directly without the need of global variable
        mydb = mysql.connector.connect(host='localhost',user=MYSQL_USER,passwd=MYSQL_PASSWD)
        my_cursor = mydb.cursor()
        my_cursor.execute('create DATABASE IF NOT EXISTS scrapeddata')
        my_cursor.execute('use scrapeddata')
        my_cursor.execute("create TABLE IF NOT EXISTS scrap (datakey varchar(50), datavalues varchar(50))")

        add_data = 'insert into scrap (datakey,datavalues) VALUES ("{}","{}")'
        for key,value in list_of_data:
            my_cursor.execute(add_data.format(key,value))
        mydb.commit()
        my_cursor.close()
        mydb.close()

    else:
        print("No input file.")
        sys.exit(1)

