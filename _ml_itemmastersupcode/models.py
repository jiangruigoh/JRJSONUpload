from django.db import models
from _ml_itemmaster.models import Itemmaster
from _ml_supcus.models import Supcus
# Create your models here.
class Itemmastersupcode(models.Model):
    itemcode = models.ForeignKey(Itemmaster, models.DO_NOTHING, db_column='Itemcode',related_name='itemmastersupcode_itemmaster_key')  # Field name made lowercase.
    code = models.ForeignKey(Supcus, models.DO_NOTHING, db_column='Code', primary_key=True,related_name='itemmastersupcode_supcus_key')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=60)  # Field name made lowercase.
    supitemcode = models.CharField(db_column='SupItemCode', max_length=30)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='Created_at')  # Field name made lowercase.
    created_by = models.CharField(db_column='Created_by', max_length=15)  # Field name made lowercase.
    updated_at = models.DateTimeField(db_column='Updated_at')  # Field name made lowercase.
    updated_by = models.CharField(db_column='Updated_by', max_length=15)  # Field name made lowercase.
    item_desc = models.CharField(db_column='ITEM_DESC', max_length=40)  # Field name made lowercase.
    suplastprice = models.DecimalField(db_column='SupLastPrice', max_digits=12, decimal_places=4)  # Field name made lowercase.
    supstdprice = models.DecimalField(db_column='SupStdPrice', max_digits=12, decimal_places=4)  # Field name made lowercase.
    disc1type = models.CharField(db_column='Disc1Type', max_length=1)  # Field name made lowercase.
    disc1value = models.DecimalField(db_column='Disc1Value', max_digits=10, decimal_places=2)  # Field name made lowercase.
    disc2type = models.CharField(db_column='Disc2Type', max_length=1)  # Field name made lowercase.
    disc2value = models.DecimalField(db_column='Disc2Value', max_digits=10, decimal_places=2)  # Field name made lowercase.
    netunitprice = models.DecimalField(db_column='NetUnitPrice', max_digits=10, decimal_places=4)  # Field name made lowercase.
    cartonprice = models.DecimalField(db_column='CartonPrice', max_digits=10, decimal_places=4)  # Field name made lowercase.
    block_order = models.IntegerField()
    priority_vendor = models.IntegerField()
    none_return = models.IntegerField()
    supbulkqty = models.DecimalField(db_column='SupBulkQty', max_digits=10, decimal_places=4)  # Field name made lowercase.
    suprspaftertax = models.DecimalField(db_column='SupRSPAfterTax', max_digits=10, decimal_places=2)  # Field name made lowercase.
    suprspbeforetax = models.DecimalField(db_column='SupRSPBeforeTax', max_digits=10, decimal_places=2)  # Field name made lowercase.
    future_effdate = models.DateField(db_column='future_EffDate')  # Field name made lowercase.
    future_itemtype = models.CharField(db_column='future_ItemType', max_length=35)  # Field name made lowercase.
    future_supstdprice = models.DecimalField(db_column='future_SupStdPrice', max_digits=10, decimal_places=4)  # Field name made lowercase.
    future_supdisc1type = models.CharField(db_column='future_SupDisc1Type', max_length=1)  # Field name made lowercase.
    future_supdisc1value = models.DecimalField(db_column='future_SupDisc1Value', max_digits=10, decimal_places=2)  # Field name made lowercase.
    future_supdisc2type = models.CharField(db_column='future_SupDisc2Type', max_length=1)  # Field name made lowercase.
    future_supdisc2value = models.DecimalField(db_column='future_SupDisc2Value', max_digits=10, decimal_places=2)  # Field name made lowercase.
    future_netunitprice = models.DecimalField(db_column='future_NetUnitPrice', max_digits=10, decimal_places=4)  # Field name made lowercase.
    future_cartonprice = models.DecimalField(db_column='future_CartonPrice', max_digits=10, decimal_places=4)  # Field name made lowercase.
    orderlotsize = models.DecimalField(db_column='OrderLotSize', max_digits=10, decimal_places=4)  # Field name made lowercase.
    taxintno = models.IntegerField(db_column='TaxIntNo')  # Field name made lowercase.
    taxcode = models.CharField(db_column='TaxCode', max_length=15)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'itemmastersupcode'
        unique_together = (('itemcode', 'priority_vendor'), ('code', 'itemcode'),)
        ordering = ('itemcode',)

    def __str__(self):
        return self.itemcode

    def get_absolute_url(self):
        return f'/{self.itemcode}/'  