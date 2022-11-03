from django.db import models
from _lib import panda
from django.db.models import Max
from django.core.validators import MaxValueValidator, MinValueValidator

from _mc_subdept.models import Subdept
# Create your models here.
class Category(models.Model):
    deptcode = models.CharField(db_column='DeptCode', max_length=6)  # Field name made lowercase.
    mcode = models.ForeignKey(Subdept, models.DO_NOTHING, db_column='MCode',related_name='category_key')  # Field name made lowercase.
    code = models.CharField(db_column='Code', primary_key=True, max_length=6,editable=False)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=40)  # Field name made lowercase.
    margin_min = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    margin_max = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    tax_code_purchase = models.CharField(max_length=10)
    tax_code_supply = models.CharField(max_length=10)
    margin = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00)])
    created_at = models.DateTimeField(db_column='CREATED_AT', null=True,editable=False)  # Field name made lowercase.
    created_by = models.CharField(db_column='CREATED_BY', max_length=30,editable=False)  # Field name made lowercase.
    updated_at = models.DateTimeField(db_column='UPDATED_AT', blank=True, null=True,editable=False)  # Field name made lowercase.
    updated_by = models.CharField(db_column='UPDATED_BY', max_length=30)  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'category'
        ordering = ('code',)


    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return f'/{self.code}/'  

    # def next_running_number:
    #     maxCode = Category.objects.all().aggregate(Max('code'))
    #     if maxCode=='':
    #         return 1
    #     else:
    #         return maxCode+1



    def save(self, *args, **kwargs):
        print('1234567')
        print('self_group:',self.code)
        if self.created_by =='':
            maxCode = Category.objects.all().aggregate(Max('code'))
            if maxCode=='':
                next_running_number = 1
            else:
                print('print maxcode', maxCode)
                print(type(maxCode))
                next_running_number = int(maxCode['code__max'])+1
            self.code='{:04}'.format(next_running_number)
            self.created_at=panda.panda_today()
            self.created_by=self.updated_by
            self.updated_at=panda.panda_today()
        else:
            self.updated_at=panda.panda_today()
        super(Category, self).save(*args, **kwargs)