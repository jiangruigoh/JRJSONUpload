from django.db import models
from _ml_itemmaster.models import Itemmaster
# Create your models here.
class ItemmasterOthersinfo(models.Model):
    oinfo_guid = models.CharField(primary_key=True, max_length=32)
    itemcode = models.OneToOneField(Itemmaster, models.DO_NOTHING, db_column='itemcode',related_name='itemaster_othersinfo_itemmaster_key')
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=15)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=15)
    remarks = models.TextField(blank=True, null=True)
    organic_certified = models.IntegerField(db_column='Organic_Certified')  # Field name made lowercase.
    non_gmo = models.IntegerField(db_column='Non_GMO')  # Field name made lowercase.
    no_colouring = models.IntegerField(db_column='No_Colouring')  # Field name made lowercase.
    gluten_free = models.IntegerField(db_column='Gluten_Free')  # Field name made lowercase.
    plant_based = models.IntegerField(db_column='Plant_Based')  # Field name made lowercase.
    pesticide_free = models.IntegerField(db_column='Pesticide_Free')  # Field name made lowercase.
    direct_from_farm = models.IntegerField(db_column='Direct_from_Farm')  # Field name made lowercase.
    free_range = models.IntegerField(db_column='Free_Range')  # Field name made lowercase.
    lactose_free = models.IntegerField(db_column='Lactose_Free')  # Field name made lowercase.
    keto_friendly = models.IntegerField(db_column='Keto_Friendly')  # Field name made lowercase.
    vegan = models.IntegerField(db_column='Vegan')  # Field name made lowercase.
    festive = models.IntegerField(db_column='Festive')  # Field name made lowercase.
    non_halal = models.IntegerField(db_column='Non_Halal')  # Field name made lowercase.
    product_size = models.DecimalField(db_column='Product_Size', max_digits=10, decimal_places=4)  # Field name made lowercase.
    product_uom = models.CharField(db_column='Product_UOM', max_length=10)  # Field name made lowercase.
    denominator = models.DecimalField(db_column='Denominator', max_digits=10, decimal_places=4)  # Field name made lowercase.
    per_serving = models.DecimalField(db_column='Per_Serving', max_digits=10, decimal_places=2)  # Field name made lowercase.
    serve_size = models.DecimalField(db_column='Serve_Size', max_digits=10, decimal_places=2)  # Field name made lowercase.
    serve_size_uom = models.CharField(db_column='Serve_Size_UOM', max_length=10)  # Field name made lowercase.
    avg_weight = models.DecimalField(db_column='Avg_Weight', max_digits=10, decimal_places=2)  # Field name made lowercase.
    avg_weight_uom = models.CharField(db_column='Avg_Weight_UOM', max_length=10)  # Field name made lowercase.
    avg_weight_denominator = models.DecimalField(db_column='Avg_Weight_Denominator', max_digits=10, decimal_places=4)  # Field name made lowercase.
    avg_weight_price = models.DecimalField(db_column='Avg_Weight_Price', max_digits=10, decimal_places=2)  # Field name made lowercase.
    estore_tag = models.IntegerField(db_column='EStore_Tag')  # Field name made lowercase.
    estore_available = models.IntegerField(db_column='EStore_Available')  # Field name made lowercase.
    estore_qty = models.DecimalField(db_column='EStore_Qty', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'itemmaster_othersinfo'
        ordering = ('itemcode',)

    def __str__(self):
        return self.itemcode

    def get_absolute_url(self):
        return f'/{self.itemcode}/'  