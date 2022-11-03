from django.db import models

# Create your models here.
class Allcode(models.Model):
    type = models.CharField(db_column='Type', primary_key=True, max_length=5)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=5)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ctype = models.CharField(db_column='CType', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ccode = models.CharField(db_column='CCode', max_length=5, blank=True, null=True)  # Field name made lowercase.
    defaultcode = models.SmallIntegerField(db_column='DefaultCode', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'allcode'
        unique_together = (('type', 'code'),)
        ordering = ('code',)

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return f'/{self.code}/'  