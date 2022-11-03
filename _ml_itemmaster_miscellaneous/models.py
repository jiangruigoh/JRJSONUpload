from django.db import models
from _ml_itemmaster.models import Itemmaster
# Create your models here.
class ItemmasterMiscellaneous(models.Model):
    mis_guid = models.CharField(primary_key=True, max_length=32)
    itemcode = models.ForeignKey(Itemmaster, models.DO_NOTHING, db_column='itemcode',related_name='itemmaster_miscellaneous_itemmaster_key')
    seq = models.IntegerField()
    text1 = models.CharField(max_length=60)
    value1 = models.DecimalField(max_digits=10, decimal_places=2)
    text2 = models.CharField(max_length=60)
    value2 = models.DecimalField(max_digits=10, decimal_places=2)
    remark = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=15)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=15)
    set_active = models.IntegerField()
    misc_group = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'itemmaster_miscellaneous'
        unique_together = (('itemcode', 'misc_group'),)
        ordering = ('itemcode',)

    def __str__(self):
        return self.itemcode

    def get_absolute_url(self):
        return f'/{self.itemcode}/'  