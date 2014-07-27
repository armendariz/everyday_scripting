#!/usr/bin/env python
import MySQLdb
import os

# Good for backing up old data you aren't working with anymore.
# You can always reimport the raw data files if you have the structure ready to go

conn = MySQLdb.Connection(host="localhost", user="", passwd='')
#conn = MySQLdb.Connection(db="payroll", host="localhost", user="", passwd='')
mysql = conn.cursor()

cnt = mysql.execute('show databases')
print '%s databases'

database_names = mysql.fetchall()

for db_name in database_names:
    n = db_name[0]
    if n == 'information_schema':
        pass
    else:
        if os.path.isdir(n):
            cmd = 'rm -rf %s' % n
            os.system(cmd)
        os.mkdir(n)
        mysql.execute('use %s' % n)
        table_cnt = mysql.execute('show tables')
        print '%s has %s tables' % (n, table_cnt)
        
        table_list = mysql.fetchall()
        for table in table_list:
            t = table[0]
            outfile_name = '%s.sql' % t
            outfile_path = os.path.join(n, outfile_name)
            outfile = open(outfile_path, 'w')
            
            mysql.execute('SHOW CREATE TABLE `%s`' % t)
            create_table_result = mysql.fetchall()
            create_table_sql = create_table_result[0][1]
            outfile.write(create_table_sql)
            outfile.close()
