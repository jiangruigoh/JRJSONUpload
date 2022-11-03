from django.db import models
from _mc_category.models import Category
from _mc_allcode.models import Allcode
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Itemmaster(models.Model):
    itemcode = models.CharField(db_column='Itemcode', primary_key=True, max_length=20)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=40)  # Field name made lowercase.
    desshort = models.CharField(db_column='DesShort', max_length=40)  # Field name made lowercase.
    itemlink = models.CharField(db_column='ItemLink', max_length=20)  # Field name made lowercase.
    openingqty = models.DecimalField(db_column='OpeningQty', max_digits=10, decimal_places=4)  # Field name made lowercase.
    openingamt = models.DecimalField(db_column='OpeningAmt', max_digits=10, decimal_places=2)  # Field name made lowercase.
    receivedqty = models.DecimalField(db_column='ReceivedQty', max_digits=10, decimal_places=4)  # Field name made lowercase.
    receivedamt = models.DecimalField(db_column='ReceivedAmt', max_digits=10, decimal_places=2)  # Field name made lowercase.
    hamperinqty = models.DecimalField(db_column='HamperInQty', max_digits=10, decimal_places=4)  # Field name made lowercase.
    hamperinamt = models.DecimalField(db_column='HamperInAmt', max_digits=10, decimal_places=2)  # Field name made lowercase.
    hamperoutqty = models.DecimalField(db_column='HamperOutQty', max_digits=10, decimal_places=4)  # Field name made lowercase.
    hamperoutamt = models.DecimalField(db_column='HamperOutAmt', max_digits=10, decimal_places=2)  # Field name made lowercase.
    adjustinqty = models.DecimalField(db_column='AdjustInQty', max_digits=10, decimal_places=4)  # Field name made lowercase.
    adjustinamt = models.DecimalField(db_column='AdjustInAmt', max_digits=10, decimal_places=2)  # Field name made lowercase.
    adjustoutqty = models.DecimalField(db_column='AdjustOutQty', max_digits=10, decimal_places=4)  # Field name made lowercase.
    adjustoutamt = models.DecimalField(db_column='AdjustOutAmt', max_digits=10, decimal_places=2)  # Field name made lowercase.
    creditqty = models.DecimalField(db_column='CreditQty', max_digits=10, decimal_places=4)  # Field name made lowercase.
    creditamt = models.DecimalField(db_column='CreditAmt', max_digits=10, decimal_places=2)  # Field name made lowercase.
    debitqty = models.DecimalField(db_column='DebitQty', max_digits=10, decimal_places=4)  # Field name made lowercase.
    debitamt = models.DecimalField(db_column='DebitAmt', max_digits=10, decimal_places=2)  # Field name made lowercase.
    salestempqty = models.DecimalField(db_column='SalesTempQty', max_digits=10, decimal_places=4)  # Field name made lowercase.
    salestempamt = models.DecimalField(db_column='SalesTempAmt', max_digits=10, decimal_places=2)  # Field name made lowercase.
    salesqty = models.DecimalField(db_column='SalesQty', max_digits=10, decimal_places=4)  # Field name made lowercase.
    salesamt = models.DecimalField(db_column='SalesAmt', max_digits=10, decimal_places=2)  # Field name made lowercase.
    orderedqty = models.DecimalField(db_column='OrderedQty', max_digits=10, decimal_places=4)  # Field name made lowercase.
    orderedamt = models.DecimalField(db_column='OrderedAmt', max_digits=10, decimal_places=2)  # Field name made lowercase.
    onhandqty = models.DecimalField(db_column='OnHandQty', max_digits=10, decimal_places=4)  # Field name made lowercase.
    onhandamt = models.DecimalField(db_column='OnHandAmt', max_digits=10, decimal_places=2)  # Field name made lowercase.
    commitqty = models.DecimalField(db_column='CommitQty', max_digits=10, decimal_places=4)  # Field name made lowercase.
    commitamt = models.DecimalField(db_column='CommitAmt', max_digits=10, decimal_places=2)  # Field name made lowercase.
    actualqty = models.DecimalField(db_column='ActualQty', max_digits=10, decimal_places=4)  # Field name made lowercase.
    actualamt = models.DecimalField(db_column='ActualAmt', max_digits=10, decimal_places=2)  # Field name made lowercase.
    dept = models.CharField(db_column='Dept', max_length=6)  # Field name made lowercase.
    subdept = models.CharField(db_column='SubDept', max_length=6)  # Field name made lowercase.
    category = models.ForeignKey(Category, models.DO_NOTHING, db_column='Category',related_name='itemmaster_category_key')  # Field name made lowercase.
    manufacturer = models.CharField(db_column='Manufacturer', max_length=10)  # Field name made lowercase.
    brand = models.CharField(db_column='Brand', max_length=10)  # Field name made lowercase.
    colour = models.CharField(db_column='Colour', max_length=20)  # Field name made lowercase.
    size = models.CharField(db_column='Size', max_length=20)  # Field name made lowercase.
    packsize = models.DecimalField(db_column='PackSize', max_digits=10, decimal_places=4)  # Field name made lowercase.
    um = models.ForeignKey(Allcode, models.DO_NOTHING, db_column='UM',related_name='itemmaster_um_key')  # Field name made lowercase.
    bulkqty = models.DecimalField(db_column='BulkQty', max_digits=10, decimal_places=4)  # Field name made lowercase.
    umbulk = models.CharField(db_column='UMBulk', max_length=5)  # Field name made lowercase.
    articleno = models.CharField(db_column='ArticleNo', max_length=20)  # Field name made lowercase.
    safetylevel = models.DecimalField(db_column='SafetyLevel', max_digits=10, decimal_places=2)  # Field name made lowercase.
    reorderlevel = models.DecimalField(db_column='ReorderLevel', max_digits=10, decimal_places=2)  # Field name made lowercase.
    reorderqty = models.DecimalField(db_column='ReorderQty', max_digits=10, decimal_places=2)  # Field name made lowercase.
    maxlevel = models.DecimalField(db_column='MaxLevel', max_digits=10, decimal_places=2)  # Field name made lowercase.
    origin = models.CharField(db_column='Origin', max_length=10)  # Field name made lowercase.
    rsp_inc_tax = models.DecimalField(db_column='RSP_inc_tax', max_digits=14, decimal_places=2)  # Field name made lowercase.
    margin = models.DecimalField(max_digits=7, decimal_places=4)
    price_include_tax = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.00)])
    sellingprice = models.DecimalField(db_column='SellingPrice', max_digits=10, decimal_places=2,validators=[MinValueValidator(0.00)])  # Field name made lowercase.
    stdcost = models.DecimalField(db_column='StdCost', max_digits=10, decimal_places=4,validators=[MinValueValidator(0.00)])  # Field name made lowercase.
    averagecost = models.DecimalField(db_column='AverageCost', max_digits=10, decimal_places=4)  # Field name made lowercase.
    lastcost = models.DecimalField(db_column='LastCost', max_digits=10, decimal_places=4)  # Field name made lowercase.
    fifocost = models.DecimalField(db_column='FIFOCost', max_digits=14, decimal_places=4)  # Field name made lowercase.
    minprice = models.DecimalField(db_column='MinPrice', max_digits=10, decimal_places=2)  # Field name made lowercase.
    maxoff = models.PositiveIntegerField(db_column='MaxOff')  # Field name made lowercase.
    openitem = models.IntegerField(db_column='OpenItem')  # Field name made lowercase.
    disable = models.IntegerField(db_column='Disable')  # Field name made lowercase.
    consign = models.PositiveIntegerField(db_column='Consign')  # Field name made lowercase.
    point = models.DecimalField(db_column='Point', max_digits=10, decimal_places=4)  # Field name made lowercase.
    remark = models.CharField(max_length=200, blank=True, null=True)
    card = models.IntegerField(db_column='Card')  # Field name made lowercase.
    cardcharges = models.DecimalField(db_column='CardCharges', max_digits=10, decimal_places=2)  # Field name made lowercase.
    bom = models.SmallIntegerField(db_column='BOM')  # Field name made lowercase.
    bomcost = models.DecimalField(db_column='BOMCost', max_digits=10, decimal_places=4)  # Field name made lowercase.
    promoselect = models.SmallIntegerField(db_column='PromoSelect')  # Field name made lowercase.
    promotype = models.CharField(db_column='PromoType', max_length=1)  # Field name made lowercase.
    promovalue = models.DecimalField(db_column='PromoValue', max_digits=10, decimal_places=2)  # Field name made lowercase.
    soldbyweight = models.IntegerField(db_column='SoldByWeight')  # Field name made lowercase.
    transinqty = models.DecimalField(db_column='TransInQty', max_digits=10, decimal_places=4)  # Field name made lowercase.
    transinamt = models.DecimalField(db_column='TransInAmt', max_digits=10, decimal_places=2)  # Field name made lowercase.
    transoutqty = models.DecimalField(db_column='TransOutQty', max_digits=10, decimal_places=4)  # Field name made lowercase.
    transoutamt = models.DecimalField(db_column='TransOutAmt', max_digits=10, decimal_places=2)  # Field name made lowercase.
    createdate = models.DateField(db_column='CreateDate')  # Field name made lowercase.
    matrixcode = models.CharField(db_column='MatrixCode', max_length=20)  # Field name made lowercase.
    sprice2 = models.DecimalField(db_column='SPrice2', max_digits=10, decimal_places=2)  # Field name made lowercase.
    sprice3 = models.DecimalField(db_column='SPrice3', max_digits=10, decimal_places=2)  # Field name made lowercase.
    sprice4 = models.DecimalField(db_column='SPrice4', max_digits=10, decimal_places=2)  # Field name made lowercase.
    sprice5 = models.DecimalField(db_column='SPrice5', max_digits=10, decimal_places=2)  # Field name made lowercase.
    distype2 = models.CharField(db_column='DisType2', max_length=1)  # Field name made lowercase.
    distype3 = models.CharField(db_column='DisType3', max_length=1)  # Field name made lowercase.
    distype4 = models.CharField(db_column='DisType4', max_length=1)  # Field name made lowercase.
    distype5 = models.CharField(db_column='DisType5', max_length=1)  # Field name made lowercase.
    disvalue2 = models.DecimalField(db_column='DisValue2', max_digits=10, decimal_places=2)  # Field name made lowercase.
    disvalue3 = models.DecimalField(db_column='DisValue3', max_digits=10, decimal_places=2)  # Field name made lowercase.
    disvalue4 = models.DecimalField(db_column='DisValue4', max_digits=10, decimal_places=2)  # Field name made lowercase.
    disvalue5 = models.DecimalField(db_column='DisValue5', max_digits=10, decimal_places=2)  # Field name made lowercase.
    issuestamp = models.DateTimeField(db_column='IssueStamp')  # Field name made lowercase.
    laststamp = models.DateTimeField(db_column='LastStamp')  # Field name made lowercase.
    newforscript = models.IntegerField(db_column='NewForScript')  # Field name made lowercase.
    weightfactor = models.IntegerField(db_column='WeightFactor')  # Field name made lowercase.
    weightprice = models.DecimalField(db_column='WeightPrice', max_digits=10, decimal_places=2)  # Field name made lowercase.
    barcodetype = models.CharField(db_column='BarcodeType', max_length=1)  # Field name made lowercase.
    itembarcode = models.CharField(db_column='ItemBarcode', max_length=30)  # Field name made lowercase.
    costmargin = models.IntegerField()
    costmarginvalue = models.DecimalField(max_digits=10, decimal_places=4)
    mlast = models.DecimalField(max_digits=10, decimal_places=4)
    mlastdaily = models.DecimalField(db_column='mlastDaily', max_digits=10, decimal_places=4)  # Field name made lowercase.
    mavg = models.DecimalField(max_digits=10, decimal_places=4)
    mavgdaily = models.DecimalField(db_column='mavgDaily', max_digits=10, decimal_places=4)  # Field name made lowercase.
    mcum = models.DecimalField(max_digits=10, decimal_places=4)
    mcumdaily = models.DecimalField(db_column='mcumDaily', max_digits=10, decimal_places=4)  # Field name made lowercase.
    mcummonthly = models.DecimalField(db_column='mcumMonthly', max_digits=10, decimal_places=4)  # Field name made lowercase.
    mrank = models.CharField(db_column='mRank', max_length=1)  # Field name made lowercase.
    markupamt = models.DecimalField(max_digits=10, decimal_places=2)
    markdownamt = models.DecimalField(max_digits=10, decimal_places=2)
    mlastdiff = models.DecimalField(max_digits=10, decimal_places=4)
    cartonprice = models.DecimalField(max_digits=10, decimal_places=2)
    mrankamt = models.CharField(db_column='mRankAmt', max_length=1)  # Field name made lowercase.
    lastopenqty = models.DecimalField(max_digits=10, decimal_places=4)
    lastopenamt = models.DecimalField(max_digits=10, decimal_places=2)
    usedate = models.IntegerField()
    cost_code = models.CharField(max_length=30)
    purtolerance_std_plus = models.DecimalField(db_column='PurTolerance_Std_plus', max_digits=10, decimal_places=4)  # Field name made lowercase.
    purtolerance_std_minus = models.DecimalField(db_column='PurTolerance_Std_Minus', max_digits=10, decimal_places=4)  # Field name made lowercase.
    weighttraceqty = models.SmallIntegerField(db_column='WeightTraceQty')  # Field name made lowercase.
    weighttraceqtyuom = models.CharField(db_column='WeightTraceQtyUOM', max_length=6)  # Field name made lowercase.
    itemtype = models.CharField(db_column='ItemType', max_length=35)  # Field name made lowercase.
    zero_price = models.IntegerField()
    mempoint_base_on_qty = models.IntegerField()
    item_package = models.IntegerField()
    vendor_code = models.CharField(max_length=15)
    trace_sn = models.IntegerField()
    tax_code_purchase = models.CharField(max_length=10)
    tax_code_supply = models.CharField(max_length=10)
    costratio = models.DecimalField(db_column='CostRatio', max_digits=5, decimal_places=2)  # Field name made lowercase.
    yieldratio = models.DecimalField(db_column='YieldRatio', max_digits=5, decimal_places=2)  # Field name made lowercase.
    price_type = models.CharField(max_length=30)
    costmargintype = models.CharField(db_column='CostMarginType', max_length=1)  # Field name made lowercase.
    taxintno = models.IntegerField(db_column='TaxIntNo')  # Field name made lowercase.
    taxcode = models.CharField(db_column='TaxCode', max_length=15)  # Field name made lowercase.
    unit_weight = models.DecimalField(max_digits=10, decimal_places=8)
    unit_length = models.DecimalField(max_digits=10, decimal_places=8)
    unit_width = models.DecimalField(max_digits=10, decimal_places=8)
    unit_height = models.DecimalField(max_digits=10, decimal_places=8)
    unit_volume = models.DecimalField(max_digits=10, decimal_places=8)
    bestbuy = models.IntegerField(db_column='BestBuy')  # Field name made lowercase.
    rec_price_inc_tax = models.DecimalField(max_digits=14, decimal_places=2)
    non_inventory = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'itemmaster'
        ordering = ('itemcode',)

    def __str__(self):
        return self.itemcode

    def get_absolute_url(self):
        return f'/{self.itemcode}/' 