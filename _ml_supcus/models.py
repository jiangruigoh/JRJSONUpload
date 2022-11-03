from django.db import models

# Create your models here.
class Supcus(models.Model):
    type = models.CharField(db_column='Type', max_length=1)  # Field name made lowercase.
    code = models.CharField(db_column='Code', primary_key=True, max_length=15)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=60)  # Field name made lowercase.
    add1 = models.CharField(db_column='Add1', max_length=60)  # Field name made lowercase.
    add2 = models.CharField(db_column='Add2', max_length=60)  # Field name made lowercase.
    add3 = models.CharField(db_column='Add3', max_length=60)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=20)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=20)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=25)  # Field name made lowercase.
    postcode = models.CharField(db_column='Postcode', max_length=6)  # Field name made lowercase.
    tel = models.CharField(db_column='Tel', max_length=20)  # Field name made lowercase.
    fax = models.CharField(db_column='Fax', max_length=20)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=60)  # Field name made lowercase.
    mobile = models.CharField(db_column='Mobile', max_length=12)  # Field name made lowercase.
    term = models.CharField(db_column='Term', max_length=30)  # Field name made lowercase.
    paymentday = models.IntegerField(db_column='PaymentDay')  # Field name made lowercase.
    bankacc = models.CharField(db_column='BankAcc', max_length=35)  # Field name made lowercase.
    creditlimit = models.DecimalField(db_column='CreditLimit', max_digits=10, decimal_places=2)  # Field name made lowercase.
    monitorcredit = models.SmallIntegerField(db_column='MonitorCredit')  # Field name made lowercase.
    remark = models.TextField(db_column='Remark', blank=True, null=True)  # Field name made lowercase.
    pointbf = models.DecimalField(db_column='PointBF', max_digits=10, decimal_places=2)  # Field name made lowercase.
    pointcumm = models.DecimalField(db_column='PointCumm', max_digits=10, decimal_places=2)  # Field name made lowercase.
    pointsum = models.DecimalField(db_column='PointSum', max_digits=10, decimal_places=2)  # Field name made lowercase.
    member = models.SmallIntegerField(db_column='Member')  # Field name made lowercase.
    memberno = models.CharField(max_length=20)
    expirydate = models.DateField(db_column='ExpiryDate')  # Field name made lowercase.
    cyclevisit = models.IntegerField(db_column='CycleVisit')  # Field name made lowercase.
    deliveryterm = models.IntegerField()
    issuedstamp = models.DateTimeField(db_column='IssuedStamp')  # Field name made lowercase.
    laststamp = models.DateTimeField(db_column='LastStamp')  # Field name made lowercase.
    dadd1 = models.CharField(max_length=60)
    dadd2 = models.CharField(max_length=60)
    dadd3 = models.CharField(max_length=60)
    dattn = models.CharField(max_length=60)
    dtel = models.CharField(max_length=20)
    dfax = models.CharField(max_length=20)
    email = models.CharField(max_length=60)
    accountcode = models.CharField(db_column='AccountCode', max_length=15)  # Field name made lowercase.
    accpdebit = models.CharField(db_column='AccPDebit', max_length=10)  # Field name made lowercase.
    accpcredit = models.CharField(db_column='AccPCredit', max_length=10)  # Field name made lowercase.
    calduedateby = models.CharField(db_column='CalDueDateby', max_length=30)  # Field name made lowercase.
    supcusgroup = models.CharField(db_column='supcusGroup', max_length=20)  # Field name made lowercase.
    region = models.CharField(max_length=10)
    pcode = models.CharField(max_length=10)
    add4 = models.CharField(db_column='Add4', max_length=60)  # Field name made lowercase.
    contact2 = models.CharField(db_column='Contact2', max_length=60)  # Field name made lowercase.
    dadd4 = models.CharField(db_column='DAdd4', max_length=60)  # Field name made lowercase.
    poprice_method = models.CharField(max_length=7)
    stockday_min = models.IntegerField()
    stockday_max = models.IntegerField()
    stock_returnable = models.IntegerField()
    stock_return_cost_type = models.CharField(max_length=10)
    autoclosepo = models.IntegerField(db_column='AutoClosePO')  # Field name made lowercase.
    consign = models.IntegerField(db_column='Consign')  # Field name made lowercase.
    block = models.IntegerField(db_column='Block')  # Field name made lowercase.
    exclude_orderqty_control = models.IntegerField()
    supcus_guid = models.CharField(unique=True, max_length=32)
    acc_no = models.CharField(max_length=20)
    ord_w1 = models.IntegerField(db_column='Ord_W1')  # Field name made lowercase.
    ord_w2 = models.IntegerField(db_column='Ord_W2')  # Field name made lowercase.
    ord_w3 = models.IntegerField(db_column='Ord_W3')  # Field name made lowercase.
    ord_w4 = models.IntegerField(db_column='Ord_W4')  # Field name made lowercase.
    ord_d1 = models.IntegerField(db_column='Ord_D1')  # Field name made lowercase.
    ord_d2 = models.IntegerField(db_column='Ord_D2')  # Field name made lowercase.
    ord_d3 = models.IntegerField(db_column='Ord_D3')  # Field name made lowercase.
    ord_d4 = models.IntegerField(db_column='Ord_D4')  # Field name made lowercase.
    ord_d5 = models.IntegerField(db_column='Ord_D5')  # Field name made lowercase.
    ord_d6 = models.IntegerField(db_column='Ord_D6')  # Field name made lowercase.
    ord_d7 = models.IntegerField(db_column='Ord_D7')  # Field name made lowercase.
    rec_method_1 = models.IntegerField(db_column='Rec_Method_1')  # Field name made lowercase.
    rec_method_2 = models.IntegerField(db_column='Rec_Method_2')  # Field name made lowercase.
    rec_method_3 = models.IntegerField(db_column='Rec_Method_3')  # Field name made lowercase.
    rec_method_4 = models.IntegerField(db_column='Rec_Method_4')  # Field name made lowercase.
    rec_method_5 = models.IntegerField(db_column='Rec_Method_5')  # Field name made lowercase.
    pur_expiry_days = models.IntegerField()
    grn_baseon_pocost = models.IntegerField()
    ord_set_global = models.IntegerField(db_column='Ord_set_global')  # Field name made lowercase.
    rules_code = models.CharField(max_length=20)
    po_negative_qty = models.IntegerField()
    grpo_variance_qty = models.DecimalField(max_digits=10, decimal_places=2)
    grpo_variance_price = models.DecimalField(max_digits=10, decimal_places=2)
    price_include_tax = models.IntegerField()
    delivery_early_in_day = models.PositiveIntegerField()
    delivery_late_in_day = models.PositiveIntegerField()
    tax_code = models.CharField(max_length=10)
    gst_start_date = models.DateField()
    gst_no = models.CharField(max_length=15)
    reg_no = models.CharField(max_length=25)
    name_reg = models.CharField(max_length=80)
    multi_tax_rate = models.IntegerField()
    grn_allow_negative_margin = models.IntegerField()
    rebate_as_inv = models.IntegerField()
    discount_as_inv = models.IntegerField()
    poso_line_max = models.PositiveIntegerField()
    apply_actual_cn = models.IntegerField()
    purchasednamtastaxinv = models.IntegerField(db_column='PurchaseDNAmtAsTaxInv')  # Field name made lowercase.
    member_accno = models.CharField(max_length=20)
    promorebateastaxinv = models.IntegerField(db_column='PromoRebateAsTaxInv')  # Field name made lowercase.
    roundingadjust = models.IntegerField(db_column='RoundingAdjust')  # Field name made lowercase.
    mobile_po = models.IntegerField()
    auto_grn_mobile_po = models.IntegerField()
    min_expiry_day = models.IntegerField()
    currency_code = models.CharField(max_length=5)
    sstdefaultcode = models.CharField(db_column='SSTDefaultCode', max_length=15)  # Field name made lowercase.
    sstdefaulttaxintno = models.IntegerField(db_column='SSTDefaultTaxIntNo')  # Field name made lowercase.
    ssteffectivedate = models.DateField(db_column='SSTEffectiveDate')  # Field name made lowercase.
    sstregno = models.CharField(db_column='SSTRegNo', max_length=20)  # Field name made lowercase.
    replenish_date = models.CharField(max_length=12)
    replenish_stockbalance = models.IntegerField()
    b2b_registration = models.IntegerField()
    cdi = models.IntegerField()
    cpm = models.IntegerField()
    auto_price_change = models.IntegerField()
    promo_date = models.IntegerField()
    pos_sales = models.IntegerField()
    sales_agent = models.CharField(max_length=30)
    stk_rtn_collect_day = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'supcus'
        unique_together = (('code', 'supcus_guid'),)
        ordering = ('code',)

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return f'/{self.code}/'  