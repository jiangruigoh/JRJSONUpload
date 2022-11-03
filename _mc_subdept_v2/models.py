from django.db import models

# Create your models here.
class Subdept(models.Model):
    mcode = models.CharField(db_column='MCode',max_length=6)  # Field name made lowercase.
    code = models.CharField(db_column='Code', primary_key=True, max_length=6)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=40)  # Field name made lowercase.
    running = models.IntegerField(db_column='Running')  # Field name made lowercase.
    memberpoints = models.DecimalField(db_column='MemberPoints', max_digits=5, decimal_places=2)  # Field name made lowercase.
    margin_min = models.DecimalField(max_digits=5, decimal_places=2)
    margin_max = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'subdept'
        ordering = ('mcode','code','description',)

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return f'/{self.code}/' 