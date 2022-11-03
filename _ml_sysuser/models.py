from django.db import models

# Create your models here.
class Sysuser(models.Model):
    name = models.CharField(primary_key=True, max_length=15)
    pwd = models.CharField(max_length=15)
    issuedstamp = models.DateTimeField(db_column='issuedStamp')  # Field name made lowercase.
    laststamp = models.DateTimeField(db_column='lastStamp')  # Field name made lowercase.
    querydept = models.TextField(db_column='QueryDept')  # Field name made lowercase.
    fullname = models.CharField(db_column='FullName', max_length=60)  # Field name made lowercase.
    subdeptcode = models.CharField(db_column='SubDeptCode', max_length=6)  # Field name made lowercase.
    membermodule = models.IntegerField(db_column='MemberModule')  # Field name made lowercase.
    itemmaster = models.IntegerField(db_column='ItemMaster')  # Field name made lowercase.
    reportmodule = models.IntegerField(db_column='ReportModule')  # Field name made lowercase.
    freegiftmodule = models.IntegerField(db_column='FreeGiftModule')  # Field name made lowercase.
    pocketpcmodule = models.IntegerField(db_column='PocketPCModule')  # Field name made lowercase.
    groupcode = models.CharField(max_length=40)
    pwd_expirydate = models.DateField()
    sysuser_guid = models.CharField(max_length=32)
    loginlocked = models.SmallIntegerField(db_column='LoginLocked')  # Field name made lowercase.
    lastchangepassword = models.DateField(db_column='LastChangePassword')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sysuser'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.name}/'  