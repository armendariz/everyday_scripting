from django.db import models

# Create your models here.
class Contrib(models.Model):
    name = models.CharField(max_length=255L, blank=True, null=True)
    payment_type = models.CharField(max_length=255L, blank=True, null=True)
    city = models.CharField(max_length=255L, blank=True, null=True)
    state = models.CharField(max_length=255L, blank=True, null=True)
    zip_code = models.CharField(max_length=255L, blank=True, null=True)
    id_number = models.CharField(max_length=255L, blank=True, null=True)
    employer = models.CharField(max_length=255L, blank=True, null=True)
    occupation = models.CharField(max_length=255L, blank=True, null=True)
    amount = models.CharField(max_length=255L, blank=True, null=True)
    transaction_date = models.CharField(max_length=255L, blank=True, null=True)
    filed_date = models.CharField(max_length=255L, blank=True, null=True)
    transaction_number = models.CharField(max_length=255L, blank=True, null=True)
    
    ## using varchar field types above to preserve original data
    ## using the fields below for to house the converted fields
    fltamount = models.DecimalField(max_digits=16, decimal_places=2, null=True)
    dtdate = models.DateField(null=True)
