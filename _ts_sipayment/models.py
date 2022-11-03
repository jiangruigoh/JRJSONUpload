from django.db import models

# Create your models here.
class SiPayment(models.Model):
    refno = models.CharField(db_column='RefNo', primary_key=True, max_length=20)  # Field name made lowercase.
    line = models.FloatField(db_column='Line')  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=10, blank=True, null=True)  # Field name made lowercase.
    bizdate = models.DateField(db_column='BizDate', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=20, blank=True, null=True)
    paytype = models.CharField(db_column='PayType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    paydescription = models.CharField(db_column='PayDescription', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cardtype = models.CharField(db_column='CardType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cardno = models.CharField(db_column='Cardno', max_length=30, blank=True, null=True)  # Field name made lowercase.
    carddate = models.DateField(db_column='CardDate', blank=True, null=True)  # Field name made lowercase.
    cardapproval = models.CharField(db_column='CardApproval', max_length=50, blank=True, null=True)  # Field name made lowercase.
    voucherno = models.CharField(db_column='VoucherNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    payamt = models.FloatField(db_column='PayAmt', blank=True, null=True)  # Field name made lowercase.
    appliedamt = models.FloatField(db_column='AppliedAmt', blank=True, null=True)  # Field name made lowercase.
    value_factor = models.FloatField(db_column='Value_Factor', blank=True, null=True)  # Field name made lowercase.
    retention_amt = models.FloatField(db_column='Retention_amt', blank=True, null=True)  # Field name made lowercase.
    hq_update = models.SmallIntegerField(blank=True, null=True)
    loc_group = models.CharField(max_length=20, blank=True, null=True)
    currencycode = models.CharField(db_column='CurrencyCode', max_length=6, blank=True, null=True)  # Field name made lowercase.
    exchangevalue = models.FloatField(db_column='ExchangeValue', blank=True, null=True)  # Field name made lowercase.
    exchangerate = models.FloatField(db_column='ExchangeRate', blank=True, null=True)  # Field name made lowercase.
    merchant_no = models.CharField(max_length=20, blank=True, null=True)
    updatememberspoint = models.SmallIntegerField(db_column='UpdateMembersPoint', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'si_payment'
        unique_together = (('refno', 'line'),)
        ordering = ('refno',)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return f'/{self.description}/' 