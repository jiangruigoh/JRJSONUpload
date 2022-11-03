from django.db import models

# Create your models here.
class Companyprofile(models.Model):
    companyname = models.CharField(db_column='CompanyName', primary_key=True, max_length=60)  # Field name made lowercase.
    address1 = models.CharField(db_column='Address1', max_length=40)  # Field name made lowercase.
    address2 = models.CharField(db_column='Address2', max_length=40)  # Field name made lowercase.
    tel = models.CharField(db_column='Tel', max_length=30)  # Field name made lowercase.
    fax = models.CharField(db_column='Fax', max_length=30)  # Field name made lowercase.
    ashq = models.IntegerField(db_column='asHQ')  # Field name made lowercase.
    locgroup_branch = models.CharField(max_length=10)
    locgroup_dc = models.CharField(max_length=10)
    comp_code = models.CharField(max_length=5)
    system_start_date = models.DateField()
    gst_no = models.CharField(max_length=15)
    address3 = models.CharField(db_column='Address3', max_length=40)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=30)  # Field name made lowercase.
    postalcode = models.CharField(max_length=10)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    gst_start_date = models.DateField()
    comp_reg_no = models.CharField(max_length=25)
    tax_inclusive = models.SmallIntegerField()
    gst_submission_cycle = models.IntegerField()
    item_runningno_type = models.CharField(max_length=10)
    item_runningno_digit = models.IntegerField()
    sst_start_date = models.DateField()
    gst_end_date = models.DateField()
    sst_no = models.CharField(max_length=20)
    sst_end_date = models.DateField()
    item_runningno_itemlinkrunno = models.SmallIntegerField()
    company_guid = models.CharField(max_length=32)
    outlet_guid = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'companyprofile'
        ordering = ('locgroup_branch',)

    def __str__(self):
        return self.locgroup_branch

    def get_absolute_url(self):
        return f'/{self.locgroup_branch}/' 