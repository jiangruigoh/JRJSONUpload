from django.db import models
from _lib import panda
# Create your models here.
class Department(models.Model):
    code = models.CharField(db_column='Code', primary_key=True, max_length=6)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=40, blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='CREATED_AT', null=True,editable=False)  # Field name made lowercase.
    created_by = models.CharField(db_column='CREATED_BY', max_length=30,editable=False)  # Field name made lowercase.
    updated_at = models.DateTimeField(db_column='UPDATED_AT', blank=True, null=True,editable=False)  # Field name made lowercase.
    updated_by = models.CharField(db_column='UPDATED_BY', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'department'
        ordering = ('code',)

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return f'/{self.code}/'  

    def save(self, *args, **kwargs):
        print('self_group:',self.code)
        if self.created_by =='':
            self.created_at=panda.panda_today()
            self.created_by=self.updated_by
            self.updated_at=panda.panda_today()
        else:
            self.updated_at=panda.panda_today()
        super(Department, self).save(*args, **kwargs)