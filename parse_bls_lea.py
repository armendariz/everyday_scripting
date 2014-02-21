#!/usr/bin/env python
import urllib
import requests
import StringIO
import csv

la_area_type_url = 'ftp://ftp.bls.gov/pub/time.series/la/la.area_type'
urllib.urlretrieve(la_area_type_url, 'lea_area_type.csv')
infile = open('lea_area_type.csv')
csv_reader = csv.reader(infile, delimiter='\t')
headers = csv_reader.next()
lk_area_type = {}
for row in csv_reader:
    lk_area_type[row[0]] = row[1]
infile.close()


la_area_url = 'ftp://ftp.bls.gov/pub/time.series/la/la.area'
urllib.urlretrieve(la_area_url, 'lea_area.csv')
infile = open('lea_area.csv')
csv_reader = csv.reader(infile, delimiter='\t')
headers = csv_reader.next()
lk_area = {}
for row in csv_reader:
    lk_area[row[1]] = {
        'type': row[0],
        'name': row[2],
        'display_level': row[3],
        'selectable': row[4],
        'sort_sequence': row[5],
    }
infile.close()



la_data_url = 'ftp://ftp.bls.gov/pub/time.series/la/la.data.0.CurrentU10-14'
urllib.urlretrieve(la_data_url, 'lea_data_u_10_14.csv')
infile = open('lea_data_u_10_14.csv')
csv_reader = csv.reader(infile, delimiter='\t')
headers = csv_reader.next()
lk_data = {}
for row in csv_reader:
    if row[0] not in lk_data:
        lk_data[row[0]] = [
                {
                    'year': row[1],
                    'period': row[2],
                    'value': row[3],
                    'footnote_codes': row[4],
                },
        ]
    else:
        lk_data[row[0]].append(
            {
                'year': row[1],
                'period': row[2],
                'value': row[3],
                'footnote_codes': row[4],
            },
        )
infile.close()


outfile = open('decoded_reshaped.csv', 'w')
csv_writer = csv.writer(outfile)
geo_headers = [
    'series_id',
    'code',
    'name',
    'type',
]
v = lk_data.values()[0]
data_headers = ['%s%s' % (datum['year'], datum['period']) for datum in v]
headers = geo_headers + data_headers
csv_writer.writerow(headers)
for k,v in lk_data.items():
    geo_code =  k.strip()[3:11]
    name = lk_area[geo_code]['name']
    geo_type = lk_area_type[lk_area[geo_code]['type']]
    row = [k, geo_code, name, geo_type]
    for datum in v:
        row.append(datum['value'])
    csv_writer.writerow(row)
outfile.close()