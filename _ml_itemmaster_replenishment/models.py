from django.db import models
from _ml_itemmaster.models import Itemmaster
# Create your models here.
class ItemmasterReplenishment(models.Model):
    im_rep_guid = models.CharField(max_length=32)
    itemcode = models.OneToOneField(Itemmaster, models.DO_NOTHING, db_column='itemcode', primary_key=True,related_name='itemmaster_replenishment_itemmaster_key')
    concept = models.CharField(max_length=32)
    min_qty = models.DecimalField(max_digits=10, decimal_places=4)
    max_qty = models.DecimalField(max_digits=10, decimal_places=4)
    display_qty = models.DecimalField(max_digits=10, decimal_places=4)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=15)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'itemmaster_replenishment'
        unique_together = (('itemcode', 'concept'),)
        ordering = ('itemcode',)

    def __str__(self):
        return self.itemcode

    def get_absolute_url(self):
        return f'/{self.itemcode}/'  