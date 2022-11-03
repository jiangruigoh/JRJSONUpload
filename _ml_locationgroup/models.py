from django.db import models

# Create your models here.
class Locationgroup(models.Model):
    code = models.CharField(db_column='Code', primary_key=True, max_length=10)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=50, blank=True, null=True)  # Field name made lowercase.
    set_active = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'locationgroup'
        ordering = ('code',)

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return f'/{self.code}/'  