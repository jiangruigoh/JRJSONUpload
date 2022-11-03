from django.db import models
#from _ml_supcus.models import Supcus
# Create your models here.
class SupcusBranch(models.Model):
    branch_guid = models.CharField(unique=True, primary_key=True,max_length=32)
    supcus_guid = models.CharField(unique=True, max_length=32)#ForeignKey(Supcus, models.DO_NOTHING, db_column='supcus_guid', primary_key=True,related_name='supcus_branch_key')
    loc_group = models.CharField(max_length=10)
    set_active = models.IntegerField()
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=15)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=15)
    is_ibt = models.IntegerField()
    limit_control_amt = models.FloatField()
    debit_acc_code = models.CharField(max_length=15)
    credit_acc_code = models.CharField(max_length=15)
    isict = models.IntegerField(db_column='isICT')  # Field name made lowercase.
    acc_code = models.CharField(max_length=15)
    is_gst = models.IntegerField()
    supbulkqty = models.FloatField(db_column='SupBulkQty')  # Field name made lowercase.
    outlet_ord_d1 = models.IntegerField(db_column='Outlet_Ord_D1')  # Field name made lowercase.
    outlet_ord_d2 = models.IntegerField(db_column='Outlet_Ord_D2')  # Field name made lowercase.
    outlet_ord_d3 = models.PositiveIntegerField(db_column='Outlet_Ord_D3')  # Field name made lowercase.
    outlet_ord_d4 = models.IntegerField(db_column='Outlet_Ord_D4')  # Field name made lowercase.
    outlet_ord_d5 = models.IntegerField(db_column='Outlet_Ord_D5')  # Field name made lowercase.
    outlet_ord_d6 = models.IntegerField(db_column='Outlet_Ord_D6')  # Field name made lowercase.
    outlet_ord_d7 = models.IntegerField(db_column='Outlet_Ord_D7')  # Field name made lowercase.
    po_min_amt = models.DecimalField(db_column='PO_min_amt', max_digits=14, decimal_places=2)  # Field name made lowercase.
    block_po = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'supcus_branch'
        # unique_together = (('supcus_guid', 'loc_group'),)
        unique_together = (('supcus_guid'),)

        ordering = ('supcus_guid',)

    def __str__(self):
        return self.supcus_guid

    def get_absolute_url(self):
        return f'/{self.supcus_guid}/'  