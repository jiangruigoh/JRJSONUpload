from django.db import models
from _ml_itemmaster.models import Itemmaster
# Create your models here.
class ItemmasterItemtype(models.Model):
    itemcode = models.ForeignKey(Itemmaster, models.DO_NOTHING, db_column='itemcode',related_name='itemmaster_itemtype_itemmaster_key')
    itemtype_guid = models.CharField(primary_key=True, max_length=32)
    concept = models.CharField(max_length=32)
    itemtype = models.CharField(max_length=35)
    date_from = models.DateField()
    date_to = models.DateField()
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=15)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=15)
    cancel = models.IntegerField()
    cancel_at = models.DateTimeField()
    last_refno = models.CharField(max_length=20)
    future_eff_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'itemmaster_itemtype'
        ordering = ('itemcode',)

    def __str__(self):
        return self.itemcode

    def get_absolute_url(self):
        return f'/{self.itemcode}/'  