from ca_campfin.models import Contrib
from dateutil.parser import parse
import csv

def load():
    '''
        from the main django_example do this:
        $ python manage.py shell
        $ from ca_campfin.load import *
        $ load()
    '''
    infile = open('ca_campfin/data/contribs.csv') # django is wired to use the folder where manage.py is housed as the base folder. This is a relative path from that point.
    csv_reader = csv.reader(infile, delimiter='\t')
    headers = csv_reader.next()
    for row in csv_reader:
        if row: # if the row isn't empty
            insert = Contrib()
            insert.name = row[0]
            insert.payment_type = row[1]
            insert.city = row[2]
            insert.state = row[3]
            insert.zip_code = row[4]
            if row[5]: # if this field isn't blank
                insert.id_number = row[5]
            insert.employer = row[6]
            insert.occupation = row[7]
            insert.amount = row[8]
            insert.transaction_date = row[9]
            insert.filed_date = row[10]
            insert.transaction_number = row[11]
            insert.fltamount = row[8].replace('$', '').replace(',', '').replace('(', '-').replace(')', '')
            if row[9]: # if this field isn't blank
                insert.dtdate = parse(row[9]).date().isoformat()
            insert.save()
    infile.close()
