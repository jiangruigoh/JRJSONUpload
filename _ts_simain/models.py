from django.db import models

# Create your models here.
class Simain(models.Model):
    refno = models.CharField(db_column='RefNo', primary_key=True, max_length=15,editable=True)  # Field name made lowercase.
    docno = models.CharField(db_column='DocNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    invoicedate = models.DateField(db_column='InvoiceDate', blank=True, null=True)  # Field name made lowercase.
    deliverdate = models.DateField(db_column='DeliverDate', blank=True, null=True)  # Field name made lowercase.
    issuestamp = models.DateTimeField(db_column='IssueStamp', blank=True, null=True)  # Field name made lowercase.
    issuedby = models.CharField(db_column='IssuedBy', max_length=80, blank=True, null=True)  # Field name made lowercase.
    laststamp = models.DateTimeField(db_column='LastStamp', blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=15, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=60, blank=True, null=True)  # Field name made lowercase.
    add1 = models.CharField(db_column='Add1', max_length=60, blank=True, null=True)  # Field name made lowercase.
    add2 = models.CharField(db_column='Add2', max_length=60, blank=True, null=True)  # Field name made lowercase.
    add3 = models.CharField(db_column='Add3', max_length=60, blank=True, null=True)  # Field name made lowercase.
    attn = models.CharField(db_column='Attn', max_length=60, blank=True, null=True)  # Field name made lowercase.
    term = models.CharField(max_length=20, blank=True, null=True)
    tel = models.CharField(db_column='Tel', max_length=20, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='Fax', max_length=20, blank=True, null=True)  # Field name made lowercase.
    dadd1 = models.CharField(db_column='DAdd1', max_length=60, blank=True, null=True)  # Field name made lowercase.
    dadd2 = models.CharField(db_column='DAdd2', max_length=60, blank=True, null=True)  # Field name made lowercase.
    dadd3 = models.CharField(db_column='DAdd3', max_length=60, blank=True, null=True)  # Field name made lowercase.
    dattn = models.CharField(db_column='DAttn', max_length=60, blank=True, null=True)  # Field name made lowercase.
    dtel = models.CharField(db_column='DTel', max_length=20, blank=True, null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remark = models.TextField(db_column='Remark', blank=True, null=True)  # Field name made lowercase.
    subtotal1 = models.FloatField(db_column='SubTotal1', blank=True, null=True)  # Field name made lowercase.
    discount1 = models.FloatField(db_column='Discount1', blank=True, null=True)  # Field name made lowercase.
    discount1type = models.CharField(db_column='Discount1Type', max_length=1, blank=True, null=True)  # Field name made lowercase.
    subtotal2 = models.FloatField(db_column='SubTotal2', blank=True, null=True)  # Field name made lowercase.
    discount2 = models.FloatField(db_column='Discount2', blank=True, null=True)  # Field name made lowercase.
    discount2type = models.CharField(db_column='Discount2Type', max_length=1, blank=True, null=True)  # Field name made lowercase.
    total = models.FloatField(db_column='Total', blank=True, null=True)  # Field name made lowercase.
    billstatus = models.SmallIntegerField(db_column='BillStatus', blank=True, null=True)  # Field name made lowercase.
    disc1percent = models.FloatField(db_column='Disc1Percent', blank=True, null=True)  # Field name made lowercase.
    disc2percent = models.FloatField(db_column='Disc2Percent', blank=True, null=True)  # Field name made lowercase.
    subdeptcode = models.CharField(db_column='SubDeptCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    postby = models.CharField(max_length=80, blank=True, null=True)
    postdatetime = models.DateTimeField(blank=True, null=True)
    deflocation = models.CharField(max_length=10, blank=True, null=True)
    amtasdescription = models.CharField(db_column='AmtAsDescription', max_length=200, blank=True, null=True)  # Field name made lowercase.
    salesman = models.CharField(db_column='SALESMAN', max_length=30, blank=True, null=True)  # Field name made lowercase.
    export_account = models.CharField(db_column='EXPORT_ACCOUNT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    hq_update = models.SmallIntegerField(blank=True, null=True)
    converted_from_module = models.CharField(db_column='CONVERTED_FROM_MODULE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    converted_from_at = models.DateTimeField(db_column='CONVERTED_FROM_AT', blank=True, null=True)  # Field name made lowercase.
    converted_from_by = models.CharField(db_column='CONVERTED_FROM_BY', max_length=20, blank=True, null=True)  # Field name made lowercase.
    converted_from_guid = models.CharField(db_column='CONVERTED_FROM_GUID', max_length=32, blank=True, null=True)  # Field name made lowercase.
    export_at = models.DateTimeField(db_column='EXPORT_AT', blank=True, null=True)  # Field name made lowercase.
    export_by = models.CharField(db_column='EXPORT_BY', max_length=30, blank=True, null=True)  # Field name made lowercase.
    duedate = models.DateField(db_column='DueDate', blank=True, null=True)  # Field name made lowercase.
    deliverd_by = models.CharField(db_column='Deliverd_by', max_length=40, blank=True, null=True)  # Field name made lowercase.
    vehicle_no = models.CharField(db_column='Vehicle_no', max_length=30, blank=True, null=True)  # Field name made lowercase.
    doc_no = models.CharField(db_column='Doc_No', max_length=30, blank=True, null=True)  # Field name made lowercase.
    loc_group = models.CharField(max_length=20, blank=True, null=True)
    ibt = models.SmallIntegerField(blank=True, null=True)
    gst_tax_sum = models.FloatField(blank=True, null=True)
    tax_code_purchase = models.CharField(max_length=10, blank=True, null=True)
    tax_code_sales = models.CharField(max_length=10, blank=True, null=True)
    total_include_tax = models.FloatField(blank=True, null=True)
    tax_inclusive = models.SmallIntegerField(blank=True, null=True)
    doc_name_reg = models.CharField(max_length=80, blank=True, null=True)
    gst_tax_rate = models.FloatField(blank=True, null=True)
    multi_tax_code = models.SmallIntegerField(blank=True, null=True)
    refno2 = models.CharField(max_length=20, blank=True, null=True)
    surchg_tax_sum = models.FloatField(blank=True, null=True)
    gst_adj = models.FloatField(blank=True, null=True)
    ibt_gst = models.SmallIntegerField(blank=True, null=True)
    unpostby = models.CharField(max_length=80, blank=True, null=True)
    unpostdatetime = models.DateTimeField(blank=True, null=True)
    revision = models.IntegerField(blank=True, null=True)
    member_accno = models.CharField(max_length=20, blank=True, null=True)
    updatememberspoint = models.SmallIntegerField(db_column='UpdateMembersPoint', blank=True, null=True)  # Field name made lowercase.
    pointssum = models.FloatField(db_column='PointsSum', blank=True, null=True)  # Field name made lowercase.
    rounding_adj = models.FloatField(blank=True, null=True)
    roundadjneed = models.SmallIntegerField(db_column='RoundAdjNeed', blank=True, null=True)  # Field name made lowercase.
    ibt_complete = models.SmallIntegerField(blank=True, null=True)
    ibt_rec_amt = models.FloatField(blank=True, null=True)
    cardtype = models.CharField(max_length=10, blank=True, null=True)
    totaltax = models.FloatField(db_column='TotalTax', blank=True, null=True)  # Field name made lowercase.
    doc_status = models.CharField(max_length=20, blank=True, null=True)
    doc_type = models.CharField(max_length=20, blank=True, null=True)
    billto_name = models.CharField(max_length=60, blank=True, null=True)
    billto_reg_no = models.CharField(max_length=30, blank=True, null=True)
    billto_gst = models.CharField(max_length=30, blank=True, null=True)
    credit_available = models.FloatField(blank=True, null=True)
    tran_volume = models.FloatField(blank=True, null=True)
    tran_weight = models.FloatField(blank=True, null=True)
    doutlet_code = models.CharField(db_column='DOutlet_code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    add4 = models.CharField(db_column='Add4', max_length=60, blank=True, null=True)  # Field name made lowercase.
    dadd4 = models.CharField(db_column='DAdd4', max_length=60, blank=True, null=True)  # Field name made lowercase.
    si_paid = models.SmallIntegerField(blank=True, null=True)
    si_point_multiply = models.FloatField(blank=True, null=True)
    uploaded = models.IntegerField(blank=True, null=True)
    uploaded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'simain'
        ordering = ('refno','invoicedate')


    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return f'/{self.description}/' 