from django.db import models
from _ml_itemmaster.models import Itemmaster

# Create your models here.
class ItemmasterListedBranch(models.Model):
    itemcode = models.OneToOneField(Itemmaster, models.DO_NOTHING, db_column='itemcode',related_name='itemmaster_listed_branch_key', primary_key=True)
    branch = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=15)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=15)
    itemtype = models.CharField(db_column='ItemType', max_length=35)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'itemmaster_listed_branch'
        unique_together = (('itemcode', 'branch'),)
        ordering = ('itemcode',)

    def __str__(self):
        return self.itemcode

    def get_absolute_url(self):
        return f'/{self.itemcode}/'  