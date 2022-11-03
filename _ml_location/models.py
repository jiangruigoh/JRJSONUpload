from django.db import models
from _ml_locationgroup.models import Locationgroup
# Create your models here.
class Location(models.Model):
    code = models.CharField(db_column='Code', primary_key=True, max_length=10)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50)  # Field name made lowercase.
    locgroup = models.ForeignKey(Locationgroup, models.DO_NOTHING, db_column='LocGroup',related_name='location_locationgroup_key')  # Field name made lowercase.
    salesloc = models.IntegerField(db_column='SalesLoc')  # Field name made lowercase.
    replenishlevel = models.IntegerField()
    replenishqty = models.IntegerField()
    badstock = models.IntegerField(db_column='BadStock')  # Field name made lowercase.
    remark = models.TextField(db_column='Remark', blank=True, null=True)  # Field name made lowercase.
    loc_address = models.TextField(blank=True, null=True)
    loc_tel = models.CharField(max_length=20, blank=True, null=True)
    loc_fax = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location'
        ordering = ('description',)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return f'/{self.description}/'  