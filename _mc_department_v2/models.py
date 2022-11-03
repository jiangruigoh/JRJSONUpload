from django.db import models

# Create your models here.
class Department(models.Model):
    code = models.CharField(db_column='Code', max_length=6, primary_key=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=40, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'department'
        ordering = ('code',)

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return f'/{self.description}/'  