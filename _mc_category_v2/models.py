from django.db import models

# Create your models here.
class Category(models.Model):
    deptcode = models.CharField(db_column='DeptCode', max_length=6)  # Field name made lowercase.
    mcode = models.CharField(db_column='MCode',max_length=6)  # Field name made lowercase.
    code = models.CharField(db_column='Code', primary_key=True, max_length=6)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=40)  # Field name made lowercase.
    margin_min = models.DecimalField(max_digits=5, decimal_places=2)
    margin_max = models.DecimalField(max_digits=5, decimal_places=2)
    tax_code_purchase = models.CharField(max_length=10)
    tax_code_supply = models.CharField(max_length=10)
    margin = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'category'
        ordering = ('deptcode','mcode','code',)

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return f'/{self.code}/'