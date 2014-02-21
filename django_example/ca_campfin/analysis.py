from ca_campfin.models import Contrib
from django.db import connection
import pandas as pd

def summary():
    '''
        $ python manage.py shell
        $ from ca_contrib.analysis import *
        $ summary()
    '''
    qs = Contrib.objects.all() # use the Django ORM to write the query
    sql_query = qs.query.sql_with_params()[0] # grab the raw sql out
    df = pd.io.sql.read_frame(sql_query, connection)
    print df.describe()
    