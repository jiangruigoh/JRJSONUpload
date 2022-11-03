from django.db import models
from _ml_itemmaster.models import Itemmaster
from _ml_locationgroup.models import Locationgroup
# Create your models here.
class ItemmasterBlockByBranch(models.Model):
    itemcode = models.ForeignKey(Itemmaster, models.DO_NOTHING, db_column='itemcode',related_name='itemmaster_block_by_branch_itemmaster_key', primary_key=True)
    branch = models.ForeignKey(Locationgroup, models.DO_NOTHING, db_column='branch',related_name='itemmaster_block_by_branch_locationgroup_key')
    sales_order = models.IntegerField()
    purchase_order = models.IntegerField()
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=15)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=15)
    ibt = models.IntegerField()
    cn = models.IntegerField()
    dn = models.IntegerField()
    cpo = models.IntegerField()
    pos = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'itemmaster_block_by_branch'
        unique_together = (('itemcode', 'branch'),)
        ordering = ('itemcode','branch',)

    def __str__(self):
        return str(self.itemcode)

    def get_absolute_url(self):
        return f'/{self.itemcode}/'  