from django.db import models

# Create your models here.
class Sichild(models.Model):
    refno = models.CharField(db_column='RefNo', primary_key=True, max_length=15)  # Field name made lowercase.
    line = models.IntegerField(db_column='Line')  # Field name made lowercase.
    entrytype = models.CharField(db_column='EntryType', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pricetype = models.CharField(db_column='PriceType', max_length=5, blank=True, null=True)  # Field name made lowercase.
    barcode = models.CharField(db_column='Barcode', max_length=30, blank=True, null=True)  # Field name made lowercase.
    itemcode = models.CharField(db_column='Itemcode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='Qty', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    um = models.CharField(db_column='UM', max_length=5, blank=True, null=True)  # Field name made lowercase.
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    disc1type = models.CharField(db_column='Disc1Type', max_length=1, blank=True, null=True)  # Field name made lowercase.
    disc1value = models.DecimalField(db_column='Disc1Value', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    disc2type = models.CharField(db_column='Disc2Type', max_length=1, blank=True, null=True)  # Field name made lowercase.
    disc2value = models.DecimalField(db_column='Disc2Value', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    netunitprice = models.DecimalField(db_column='NetUnitPrice', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    discamt = models.DecimalField(db_column='DiscAmt', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    totalprice = models.DecimalField(db_column='TotalPrice', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    packsize = models.FloatField(db_column='PackSize', blank=True, null=True)  # Field name made lowercase.
    colour = models.CharField(db_column='Colour', max_length=20, blank=True, null=True)  # Field name made lowercase.
    size = models.CharField(db_column='Size', max_length=20, blank=True, null=True)  # Field name made lowercase.
    brand = models.CharField(db_column='Brand', max_length=5, blank=True, null=True)  # Field name made lowercase.
    articleno = models.CharField(db_column='ArticleNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    sysqoh = models.FloatField(db_column='SysQOH', blank=True, null=True)  # Field name made lowercase.
    sysavgcost = models.FloatField(db_column='SysAvgCost', blank=True, null=True)  # Field name made lowercase.
    itemlink = models.CharField(db_column='ItemLink', max_length=20, blank=True, null=True)  # Field name made lowercase.
    amendment = models.IntegerField(db_column='Amendment', blank=True, null=True)  # Field name made lowercase.
    bulkqty = models.FloatField(db_column='BulkQty', blank=True, null=True)  # Field name made lowercase.
    umbulk = models.CharField(db_column='UMBulk', max_length=5, blank=True, null=True)  # Field name made lowercase.
    bqty = models.FloatField(db_column='BQty', blank=True, null=True)  # Field name made lowercase.
    pqty = models.FloatField(db_column='PQty', blank=True, null=True)  # Field name made lowercase.
    itemremark = models.TextField(db_column='ItemRemark', blank=True, null=True)  # Field name made lowercase.
    dept = models.CharField(db_column='Dept', max_length=5, blank=True, null=True)  # Field name made lowercase.
    subdept = models.CharField(db_column='SubDept', max_length=5, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=5, blank=True, null=True)  # Field name made lowercase.
    onhandqty = models.FloatField(db_column='OnHandQty', blank=True, null=True)  # Field name made lowercase.
    avgpesalesqty = models.FloatField(db_column='AvgPESalesQty', blank=True, null=True)  # Field name made lowercase.
    lastpesalesqty = models.FloatField(db_column='LastPESalesQty', blank=True, null=True)  # Field name made lowercase.
    sellingprice = models.FloatField(db_column='SellingPrice', blank=True, null=True)  # Field name made lowercase.
    mrank = models.CharField(max_length=1, blank=True, null=True)
    cartonprice = models.FloatField(blank=True, null=True)
    sorefno = models.CharField(max_length=15, blank=True, null=True)
    soline = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=10, blank=True, null=True)
    hq_update = models.SmallIntegerField(blank=True, null=True)
    purtolerance_std_plus = models.FloatField(db_column='PurTolerance_Std_plus', blank=True, null=True)  # Field name made lowercase.
    purtolerance_std_minus = models.FloatField(db_column='PurTolerance_Std_Minus', blank=True, null=True)  # Field name made lowercase.
    weighttraceqty = models.SmallIntegerField(db_column='WeightTraceQty', blank=True, null=True)  # Field name made lowercase.
    weighttraceqtyuom = models.CharField(db_column='WeightTraceQtyUOM', max_length=6, blank=True, null=True)  # Field name made lowercase.
    weighttraceqtycount = models.FloatField(db_column='WeightTraceQtyCount', blank=True, null=True)  # Field name made lowercase.
    gst_tax_type = models.CharField(max_length=5, blank=True, null=True)
    gst_tax_code = models.CharField(max_length=10, blank=True, null=True)
    gst_tax_rate = models.FloatField(blank=True, null=True)
    gst_tax_amount = models.FloatField(blank=True, null=True)
    price_include_tax = models.FloatField(blank=True, null=True)
    totalprice_include_tax = models.FloatField(db_column='TotalPrice_include_tax', blank=True, null=True)  # Field name made lowercase.
    discvalue = models.FloatField(blank=True, null=True)
    postdatetime_c = models.DateTimeField(blank=True, null=True)
    surchg_value = models.FloatField(blank=True, null=True)
    unitactprice = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    consign = models.SmallIntegerField(blank=True, null=True)
    surchg_disc_gst = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    itemtype = models.CharField(max_length=40, blank=True, null=True)
    costmarginvalue = models.FloatField(blank=True, null=True)
    costmargin = models.SmallIntegerField(blank=True, null=True)
    soldbyweight = models.SmallIntegerField(blank=True, null=True)
    points = models.FloatField(db_column='Points', blank=True, null=True)  # Field name made lowercase.
    lastcost = models.FloatField(blank=True, null=True)
    fifocost = models.FloatField(blank=True, null=True)
    cost_deduct = models.FloatField(blank=True, null=True)
    gst_manual = models.SmallIntegerField(blank=True, null=True)
    taxintno = models.IntegerField(db_column='TaxIntNo', blank=True, null=True)  # Field name made lowercase.
    taxcodemap = models.CharField(db_column='TaxCodeMap', max_length=15, blank=True, null=True)  # Field name made lowercase.
    taxvalue = models.FloatField(db_column='TaxValue', blank=True, null=True)  # Field name made lowercase.
    taxamount = models.FloatField(db_column='TaxAmount', blank=True, null=True)  # Field name made lowercase.
    taxamountvariance = models.FloatField(db_column='TaxAmountVariance', blank=True, null=True)  # Field name made lowercase.
    promo_refno = models.CharField(max_length=20, blank=True, null=True)
    claim_amt_unit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    item_volume = models.FloatField(blank=True, null=True)
    item_weight = models.FloatField(blank=True, null=True)
    ignore_price_rules = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sichild'
        unique_together = (('refno', 'line'),)
        ordering = ('refno',)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return f'/{self.description}/'