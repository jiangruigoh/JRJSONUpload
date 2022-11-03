from django.db import models

# Create your models here.
class DbnoteBatchInfo(models.Model):
    dbnote_guid = models.CharField(primary_key=True, max_length=32)
    customer_guid = models.CharField(max_length=32)
    batch_no = models.CharField(max_length=30, blank=True, null=True)
    sup_code = models.CharField(max_length=20, blank=True, null=True)
    sup_name = models.CharField(max_length=80, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=20, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=20, blank=True, null=True)
    converted = models.SmallIntegerField(blank=True, null=True)
    b2b_dn_refno = models.CharField(max_length=20, blank=True, null=True)
    converted_by = models.CharField(max_length=20, blank=True, null=True)
    converted_at = models.DateTimeField(blank=True, null=True)
    canceled = models.SmallIntegerField(blank=True, null=True)
    canceled_at = models.DateTimeField(blank=True, null=True)
    canceled_by = models.CharField(max_length=20, blank=True, null=True)
    send_print = models.SmallIntegerField(blank=True, null=True)
    location = models.CharField(max_length=20, blank=True, null=True)
    sub_location = models.CharField(max_length=20, blank=True, null=True)
    loc_group = models.CharField(max_length=10, blank=True, null=True)
    hq_update = models.SmallIntegerField(blank=True, null=True)
    posted = models.SmallIntegerField(blank=True, null=True)
    posted_by = models.CharField(max_length=20, blank=True, null=True)
    posted_at = models.DateTimeField(blank=True, null=True)
    doc_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    uploaded = models.SmallIntegerField(blank=True, null=True)
    uploaded_at = models.DateTimeField(blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True)
    accepted_by = models.CharField(max_length=60, blank=True, null=True)
    accepted_at = models.DateTimeField(blank=True, null=True)
    cancel_remark = models.CharField(max_length=60, blank=True, null=True)
    email_send = models.SmallIntegerField(blank=True, null=True)
    amount = models.FloatField(db_column='Amount', blank=True, null=True)  # Field name made lowercase.
    gst_tax_sum = models.FloatField(blank=True, null=True)
    unpostby = models.CharField(max_length=80, blank=True, null=True)
    unpostdatetime = models.DateTimeField(blank=True, null=True)
    action_date = models.DateField(blank=True, null=True)
    uploaded_image = models.IntegerField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    cross_ref = models.CharField(max_length=32, blank=True, null=True)
    cross_ref_module = models.CharField(max_length=32, blank=True, null=True)
    subdept = models.CharField(max_length=15, blank=True, null=True)
    srbtodn_days = models.SmallIntegerField(blank=True, null=True)
    srb_accept_days = models.SmallIntegerField(blank=True, null=True)
    strb_json_info = models.JSONField(blank=True, null=True)
    strb_json_report = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dbnote_batch_info'
        ordering = ('batch_no',)
 
    def __str__(self):
        return self.dbnote_guid
 
    def get_absolute_url(self):
        return f'/{self.dbnote_guid}/'  