#!/usr/bin/env python
import urllib
import sqlite3
import os
import csv
from datetime import datetime
from nameparser import HumanName # nameparser module available here -- http://code.google.com/p/python-nameparser/


## connect to an SQLite3 database
conn = sqlite3.connect('contribs.sqlite', isolation_level=None) # creates the db file if it doesn't already exist. we set isolation_level to None so that we are in autocommit mode. that way the UPDATES are applied without further ado
c = conn.cursor() # open the lines of communication with the database

date_stamp = datetime.strftime(datetime.now(), '%Y%m%d')

# set-up a date stamped folder to hold the data in
if os.path.isdir(date_stamp): # test to see if the folder already exists
    try:
        cmd = 'rm -rf %s' % date_stamp # try deleteing the folder
        os.system(cmd)
    except:
        cmd = 'rmdir /S %s' % date_stamp # if the above fails try the Windows command line way. If both fail, the script fails
        os.system(cmd)

os.mkdir(date_stamp)
file_path = os.path.join(date_stamp, 'contribs.csv')

## fetch the data
url = 'http://cal-access.sos.ca.gov/Campaign/Committees/DetailContributionsReceivedExcel.aspx?id=1340976&session=2011'
try:
    urllib.urlretrieve(url, file_path)
    print 'fetched data, see %s' % file_path
except:
    print 'failed to fetch data'


file_path = os.path.join(date_stamp, 'contribs.csv')
infile = open(file_path) # open the csv file
handle = csv.reader(infile, delimiter='\t') # use the csv module to parse the csv
headers = handle.next() # grab the header row
infile.close() # close the csv file now that we're done

## test to see if the table already exists
sql_statement = '''
    SELECT name FROM sqlite_master WHERE type='table' AND name="%s_raw_contribs"
''' % date_stamp
cmd = c.execute(sql_statement)
results = cmd.fetchall()
if len(results) == 1:
    print 'table already exists, nuking it'
    sql_statement = "DROP TABLE `%s_raw_contribs`" % date_stamp
    cmd = c.execute(sql_statement)

## create a table using the headers of the csv file
sql_statement = "CREATE TABLE `%s_raw_contribs` (" % date_stamp

## loop through the headers and use them to craft the rest of the sql statement
for i in range(len(headers)):
    sql_friendly_header = headers[i].lower().replace(' ', '_') # index into the headers list, get rid of the spaces and change it from upper to lower case
    if i == len(headers)-1:
        creation_statement_piece = '%s TEXT' % sql_friendly_header # test to see if you are at the last element in the list. if you are, then you need to leave the comma out
    else:
        creation_statement_piece = '%s TEXT,' % sql_friendly_header
    sql_statement += creation_statement_piece
sql_statement += ');' # put the finishing touch on the sql statement
c.execute(sql_statement) # use the sql statement we just wrote to create the table


file_path = os.path.join(date_stamp, 'contribs.csv')
infile = open(file_path) # open the csv file
handle = csv.reader(infile, delimiter='\t') # use the csv module to parse the csv
headers = handle.next() # grab the header row
for h in handle: # loop through the data and insert it into the table
    if len(h) == 12:
        sql_statement = '''
            INSERT INTO `%s_raw_contribs` VALUES( "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s" );
        ''' % (date_stamp, h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7], h[8], h[9], h[10], h[11])
        c.execute(sql_statement)
    else:
        print 'skipped row with %s columns' % len(h)
infile.close() # close the csv file now that we're done
print 'loaded up %s rows' % handle.line_num


sql_query = 'ALTER TABLE `%s_raw_contribs` ADD COLUMN fltAmount DECIMAL(16,2)' % date_stamp # create a new column to house the numeric data. right now it saved as a string value
c.execute(sql_query)
sql_query = 'SELECT rowid, amount, fltAmount from `%s_raw_contribs`' % date_stamp # grab the rows, 
execute_query = c.execute(sql_query)
rows = execute_query.fetchall()
for row in rows:
    new_amount = row[1].replace('$', '').replace(',', '')
    print '%s\t%s\t%s' % (row[0], row[1], new_amount) # i printed out the amounts while i was writing the script. no need for it now
    sql_query = 'UPDATE `%s_raw_contribs` SET fltAmount = %s WHERE rowid= %s' % (date_stamp, new_amount, row[0])
    c.execute(sql_query)

sql_command = '''
    SELECT SUM(amount), SUM(fltAmount) FROM `%s_raw_contribs`
''' % date_stamp
execute_query = c.execute(sql_command)
row_list = execute_query.fetchall()
result_row = row_list[0]
str_amount = result_row[0]
flt_amount = result_row[1]
print '%s\t%s' % (str_amount, flt_amount)

try:
    new_field_list = ['title', 'fname', 'middle', 'lname', 'suffix', ]
    for field in new_field_list:
        sql_query = ''' ALTER TABLE `%s_raw_contribs` ADD %s TEXT  ''' % (date_stamp, field)
        c.execute(sql_query)
except:
    print 'fields already exist'
sql_select_command = ''' SELECT rowid, name_of_contributor FROM `%s_raw_contribs` WHERE employer <> '' AND occupation <> '' ''' % date_stamp # every sqlite table automatically has a unique row id you can use
execute_query = c.execute(sql_select_command)
rows = execute_query.fetchall()
for row in rows:
    row_id = row[0]
    name = row[1] # python lists start counting at 0 and the full name of the contributor is the second column in the sql select statement
    parsed_name = HumanName(name)
    sql_command = '''
        UPDATE `%s_raw_contribs` SET title = '%s', fname = '%s', middle = '%s', lname = '%s', suffix = '%s' WHERE rowid = %s
    ''' % (
           date_stamp, 
           parsed_name.title,
           parsed_name.first,
           parsed_name.middle,
           parsed_name.last,
           parsed_name.suffix,
           row_id,
           )
    c.execute(sql_command)

sql_command = "SELECT rowid, name_of_contributor, title, fname, middle, lname, suffix FROM `%s_raw_contribs`;" % (date_stamp)
execute_query = c.execute(sql_command)
row_list = execute_query.fetchall()
for row in row_list:
    print '%s\t%s\t%s\t%s\t%s\t%s' % (row[0], row[1], row[2], row[3], row[4], row[5])

