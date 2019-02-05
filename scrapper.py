#! /usr/bin/env python3

import os
import sys
from bs4 import BeautifulSoup
import mysql.connector



def get_data_from_row(row):
    span_of_row = row.find_all('span')
    return (span_of_row[0].get_text(),span_of_row[1].get_text())

if __name__ == "__main__":

    soup = None
    list_of_data = list()
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as fp:
            soup = BeautifulSoup(fp, 'html.parser')
        table = soup.find('tbody')
        rows = table.find_all('tr')
        
        for i in (2, 14, 19, 27):
            list_of_data.append(get_data_from_row(rows[i]))

        result = soup.find('span',{'class':'diags_testrunning_testresulttext_PASS'}).get_text()
        list_of_data.append(('Result', result))

        math_test_table = soup.find_all('table',{'class':'diags_deviceInfoDialog_detailedSysinfoPane_testTable'})[4]
        math_register_test = math_test_table.find_all('th')
        list_of_data.append((math_register_test[0].get_text(),math_register_test[1].get_text()))

        mydb = mysql.connector.connect(host='localhost',user='root',passwd='xclaim')
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

