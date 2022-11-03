from django.db import models
from _lib import panda
# Create your models here.
class SetGroup(models.Model):
    group_guid = models.CharField(db_column='GROUP_GUID', unique=True, max_length=32,editable=False)  # Field name made lowercase. Primary GUID ensure editable=False
    group_code = models.CharField(db_column='GROUP_CODE', primary_key=True, max_length=10)  # Field name made lowercase.
    group_desc = models.CharField(db_column='GROUP_DESC', max_length=40)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='CREATED_AT', null=True,editable=False)  # Field name made lowercase.
    created_by = models.CharField(db_column='CREATED_BY', max_length=30,editable=False)  # Field name made lowercase.
    updated_at = models.DateTimeField(db_column='UPDATED_AT', blank=True, null=True,editable=False)  # Field name made lowercase.
    updated_by = models.CharField(db_column='UPDATED_BY', max_length=30)  # Field name made lowercase.
    group_code_acc = models.CharField(max_length=20,blank=True)
    code_acc = models.CharField(max_length=20,blank=True)

    class Meta:
        managed = False
        db_table = 'set_group'
        ordering = ('group_code',)

    def __str__(self):
        return self.group_code

    def get_absolute_url(self):
        return f'/{self.group_code}/' 



    def save(self, *args, **kwargs):
        print('self_group:',self.group_guid)
        if self.group_guid =='':
            self.group_guid=panda.panda_uuid()
            self.created_at=panda.panda_today()
            self.created_by=self.updated_by
            self.updated_at=panda.panda_today()
        else:
            self.updated_at=panda.panda_today()
        super(SetGroup, self).save(*args, **kwargs)