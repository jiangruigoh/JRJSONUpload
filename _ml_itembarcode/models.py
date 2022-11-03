from django.db import models
from _ml_itemmaster.models import Itemmaster
# Create your models here.
class Itembarcode(models.Model):
    itemcode = models.ForeignKey(Itemmaster, models.DO_NOTHING, db_column='Itemcode', primary_key=True,related_name='itembarcode_itemmaster_key')  # Field name made lowercase.
    barcode = models.CharField(db_column='Barcode', unique=True, max_length=30)  # Field name made lowercase.
    issuestamp = models.DateTimeField(db_column='IssueStamp', blank=True, null=True)  # Field name made lowercase.
    laststamp = models.DateTimeField(db_column='LastStamp', blank=True, null=True)  # Field name made lowercase.
    newforscript = models.SmallIntegerField(db_column='NewForScript', blank=True, null=True)  # Field name made lowercase.
    bardesc = models.CharField(db_column='barDesc', max_length=50)  # Field name made lowercase.
    barremark = models.CharField(db_column='barRemark', max_length=60, blank=True, null=True)  # Field name made lowercase.
    barprice = models.DecimalField(db_column='barPrice', max_digits=10, decimal_places=2)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    changedby = models.CharField(db_column='ChangedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'itembarcode'
        unique_together = (('itemcode', 'barcode'),)
        ordering = ('itemcode',)

    def __str__(self):
        return self.itemcode

    def get_absolute_url(self):
        return f'/{self.itemcode}/'  