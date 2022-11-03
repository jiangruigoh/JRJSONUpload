from django.db import models
from _lib import panda
from _mc_department.models import Department
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Subdept(models.Model):
    mcode = models.ForeignKey(Department, models.DO_NOTHING, db_column='MCode',related_name='subdept_key')  # Field name made lowercase.
    code = models.CharField(db_column='Code', primary_key=True, max_length=6)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=40)  # Field name made lowercase.
    running = models.IntegerField(db_column='Running')  # Field name made lowercase.
    memberpoints = models.DecimalField(db_column='MemberPoints', max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])  # Field name made lowercase.
    margin_min = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    margin_max = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    created_at = models.DateTimeField(db_column='CREATED_AT', null=True,editable=False)  # Field name made lowercase.
    created_by = models.CharField(db_column='CREATED_BY', max_length=30,editable=False)  # Field name made lowercase.
    updated_at = models.DateTimeField(db_column='UPDATED_AT', blank=True, null=True,editable=False)  # Field name made lowercase.
    updated_by = models.CharField(db_column='UPDATED_BY', max_length=30)  # Field name made lowercase.
    

    class Meta:
        managed = False
        db_table = 'subdept'
        ordering = ('code',)

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return f'/{self.code}/'  

    def save(self, *args, **kwargs):
        print('self_group:',self.created_by)
        if self.created_by =='':
            self.created_at=panda.panda_today()
            self.created_by=self.updated_by
            self.updated_at=panda.panda_today()
        else:
            self.updated_at=panda.panda_today()
        super(Subdept, self).save(*args, **kwargs)