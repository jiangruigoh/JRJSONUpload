from django.db import models
from _ml_locationgroup.models import Locationgroup
from _ml_itemmaster.models import Itemmaster
# Create your models here.
class ItemmasterBranchStock(models.Model):
    branch = models.ForeignKey(Locationgroup, models.DO_NOTHING, db_column='branch',related_name='itemmaster_branch_stock_locationgroup_key', primary_key=True)
    itemcode = models.ForeignKey(Itemmaster, models.DO_NOTHING, db_column='itemcode',related_name='itemmaster_branchstock_stock_itemmaster_itemcode_key')
    sellingprice = models.DecimalField(max_digits=14, decimal_places=2)
    stdcost = models.DecimalField(max_digits=14, decimal_places=4)
    averagecost = models.DecimalField(max_digits=14, decimal_places=4)
    lastcost = models.DecimalField(max_digits=14, decimal_places=4)
    fifocost = models.DecimalField(max_digits=14, decimal_places=4)
    qoh = models.DecimalField(db_column='QOH', max_digits=10, decimal_places=2)  # Field name made lowercase.
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=15)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=15)
    hq_update = models.IntegerField()
    price_inc_tax = models.DecimalField(max_digits=14, decimal_places=2)
    qoh_link = models.DecimalField(db_column='QOH_link', max_digits=10, decimal_places=2)  # Field name made lowercase.
    packsize = models.DecimalField(max_digits=10, decimal_places=4)
    ads = models.DecimalField(max_digits=10, decimal_places=2)
    ams = models.DecimalField(max_digits=10, decimal_places=2)
    aws = models.DecimalField(max_digits=10, decimal_places=2)
    days = models.DecimalField(max_digits=10, decimal_places=0)
    qty_po = models.DecimalField(max_digits=10, decimal_places=2)
    qty_req = models.DecimalField(max_digits=10, decimal_places=2)
    qty_so = models.DecimalField(max_digits=10, decimal_places=2)
    doh = models.DecimalField(max_digits=10, decimal_places=1)
    qty_pos = models.DecimalField(max_digits=10, decimal_places=2)
    qty_si = models.DecimalField(max_digits=10, decimal_places=2)
    date_start = models.DateField()
    date_stop = models.DateField()
    itemlink = models.ForeignKey(Itemmaster, models.DO_NOTHING, db_column='itemlink',related_name='itemmaster_branchstock_stock_itemmaster_itemlink_key')
    qty_opn = models.DecimalField(max_digits=10, decimal_places=2)
    qty_rec = models.DecimalField(max_digits=10, decimal_places=2)
    qty_other = models.DecimalField(max_digits=10, decimal_places=2)
    first_gr_date = models.DateField()
    last_gr_date = models.DateField()
    last_gr_qty = models.DecimalField(max_digits=10, decimal_places=1)
    price_today_mb = models.DecimalField(max_digits=14, decimal_places=2)
    price_today_na = models.DecimalField(max_digits=14, decimal_places=2)
    recalc_at = models.DateTimeField()
    qty_tbr = models.DecimalField(max_digits=10, decimal_places=2)
    doh_new = models.DecimalField(max_digits=10, decimal_places=0)
    rank_cat_qty = models.CharField(max_length=1)
    rank_cat_amt = models.CharField(max_length=1)
    qty_promo = models.DecimalField(max_digits=10, decimal_places=2)
    ads_rep = models.DecimalField(max_digits=10, decimal_places=2)
    branch_itemtype = models.CharField(max_length=35)
    day_promo = models.DecimalField(max_digits=10, decimal_places=0)
    qty_hp_out = models.DecimalField(max_digits=10, decimal_places=2)
    qty_ibt_sales = models.DecimalField(max_digits=10, decimal_places=2)
    qty_ibt_grn = models.DecimalField(max_digits=10, decimal_places=2)
    qty_avail = models.DecimalField(max_digits=10, decimal_places=2)
    last_po_date = models.DateField()
    last_po_qty = models.DecimalField(max_digits=10, decimal_places=1)
    last_po_vendor = models.CharField(max_length=15, blank=True, null=True)
    last_po_refno = models.CharField(max_length=20, blank=True, null=True)
    last_gr_vendor = models.CharField(max_length=15, blank=True, null=True)
    last_gr_refno = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'itemmaster_branch_stock'
        unique_together = (('branch', 'itemcode'),)
        ordering = ('itemcode',)

    def __str__(self):
        return self.itemcode

    def get_absolute_url(self):
        return f'/{self.itemcode}/' 