from django.db import models
from _mc_set_group.models import SetGroup
from _lib import panda
# Create your models here.
class SetGroupDept(models.Model):
    dept_guid = models.CharField(db_column='DEPT_GUID', unique=True, max_length=32,editable=False)  # Field name made lowercase.
    group_code = models.ForeignKey(SetGroup, models.DO_NOTHING, db_column='GROUP_CODE',related_name='set_group_code_key')  # Field name made lowercase.
    dept_code = models.CharField(db_column='DEPT_CODE', primary_key=True, max_length=6)  # Field name made lowercase.
    dept_desc = models.CharField(db_column='DEPT_DESC', max_length=40)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='CREATED_AT',editable=False)  # Field name made lowercase.
    created_by = models.CharField(db_column='CREATED_BY', max_length=30,editable=False)  # Field name made lowercase.
    updated_at = models.DateTimeField(db_column='UPDATED_AT',editable=False)  # Field name made lowercase.
    updated_by = models.CharField(db_column='UPDATED_BY', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'set_group_dept'
        ordering = ('group_code','dept_code')

    def __str__(self):
        return self.dept_code

    def get_absolute_url(self):
        return f'/{self.dept_code}/'

    def save(self, *args, **kwargs):
        print('self_group:',self.dept_guid)
        if self.dept_guid =='':
            self.dept_guid=panda.panda_uuid()
            self.created_at=panda.panda_today()
            self.created_by=self.updated_by
            self.updated_at=panda.panda_today()
        else:
            self.updated_at=panda.panda_today()
        super(SetGroupDept, self).save(*args, **kwargs)