# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccCode(models.Model):
    type = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    debit = models.CharField(max_length=20)
    credit = models.CharField(max_length=20)
    outlet = models.CharField(max_length=10)
    div_acc_code = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acc_code'
        unique_together = (('type', 'name', 'outlet'),)


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


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class Category(models.Model):
    deptcode = models.CharField(db_column='DeptCode', max_length=6)  # Field name made lowercase.
    mcode = models.ForeignKey('Subdept', models.DO_NOTHING, db_column='MCode')  # Field name made lowercase.
    code = models.CharField(db_column='Code', primary_key=True, max_length=6)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=40)  # Field name made lowercase.
    margin_min = models.DecimalField(max_digits=5, decimal_places=2)
    margin_max = models.DecimalField(max_digits=5, decimal_places=2)
    tax_code_purchase = models.CharField(max_length=10)
    tax_code_supply = models.CharField(max_length=10)
    margin = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(db_column='CREATED_AT')  # Field name made lowercase.
    created_by = models.CharField(db_column='CREATED_BY', max_length=30)  # Field name made lowercase.
    updated_at = models.DateTimeField(db_column='UPDATED_AT')  # Field name made lowercase.
    updated_by = models.CharField(db_column='UPDATED_BY', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'category'


class Companyprofile(models.Model):
    companyname = models.CharField(db_column='CompanyName', primary_key=True, max_length=60)  # Field name made lowercase.
    address1 = models.CharField(db_column='Address1', max_length=40)  # Field name made lowercase.
    address2 = models.CharField(db_column='Address2', max_length=40)  # Field name made lowercase.
    tel = models.CharField(db_column='Tel', max_length=30)  # Field name made lowercase.
    fax = models.CharField(db_column='Fax', max_length=30)  # Field name made lowercase.
    ashq = models.IntegerField(db_column='asHQ')  # Field name made lowercase.
    locgroup_branch = models.CharField(max_length=10)
    locgroup_dc = models.CharField(max_length=10)
    comp_code = models.CharField(max_length=5)
    system_start_date = models.DateField()
    gst_no = models.CharField(max_length=15)
    address3 = models.CharField(db_column='Address3', max_length=40)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=30)  # Field name made lowercase.
    postalcode = models.CharField(max_length=10)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    gst_start_date = models.DateField()
    comp_reg_no = models.CharField(max_length=25)
    tax_inclusive = models.SmallIntegerField()
    gst_submission_cycle = models.IntegerField()
    item_runningno_type = models.CharField(max_length=10)
    item_runningno_digit = models.IntegerField()
    sst_start_date = models.DateField()
    gst_end_date = models.DateField()
    sst_no = models.CharField(max_length=20)
    sst_end_date = models.DateField()
    item_runningno_itemlinkrunno = models.SmallIntegerField()
    company_guid = models.CharField(max_length=32)
    outlet_guid = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'companyprofile'


class Department(models.Model):
    code = models.CharField(db_column='Code', primary_key=True, max_length=6)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=40)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='CREATED_AT')  # Field name made lowercase.
    created_by = models.CharField(db_column='CREATED_BY', max_length=30)  # Field name made lowercase.
    updated_at = models.DateTimeField(db_column='UPDATED_AT')  # Field name made lowercase.
    updated_by = models.CharField(db_column='UPDATED_BY', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'department'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Itembarcode(models.Model):
    itemcode = models.OneToOneField('Itemmaster', models.DO_NOTHING, db_column='Itemcode', primary_key=True)  # Field name made lowercase.
    barcode = models.CharField(db_column='Barcode', unique=True, max_length=30)  # Field name made lowercase.
    newforscript = models.SmallIntegerField(db_column='NewForScript', blank=True, null=True)  # Field name made lowercase.
    bardesc = models.CharField(db_column='barDesc', max_length=40)  # Field name made lowercase.
    barremark = models.CharField(db_column='barRemark', max_length=60, blank=True, null=True)  # Field name made lowercase.
    barprice = models.DecimalField(db_column='barPrice', max_digits=10, decimal_places=2)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    issuestamp = models.DateTimeField(db_column='IssueStamp', blank=True, null=True)  # Field name made lowercase.
    changedby = models.CharField(db_column='ChangedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    laststamp = models.DateTimeField(db_column='LastStamp', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'itembarcode'
        unique_together = (('itemcode', 'barcode'),)


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
    category = models.ForeignKey(Category, models.DO_NOTHING, db_column='Category')  # Field name made lowercase.
    manufacturer = models.CharField(db_column='Manufacturer', max_length=10)  # Field name made lowercase.
    brand = models.CharField(db_column='Brand', max_length=10)  # Field name made lowercase.
    colour = models.CharField(db_column='Colour', max_length=20)  # Field name made lowercase.
    size = models.CharField(db_column='Size', max_length=20)  # Field name made lowercase.
    packsize = models.DecimalField(db_column='PackSize', max_digits=10, decimal_places=4)  # Field name made lowercase.
    um = models.ForeignKey(Allcode, models.DO_NOTHING, db_column='UM')  # Field name made lowercase.
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
    price_include_tax = models.DecimalField(max_digits=10, decimal_places=2)
    sellingprice = models.DecimalField(db_column='SellingPrice', max_digits=10, decimal_places=2)  # Field name made lowercase.
    stdcost = models.DecimalField(db_column='StdCost', max_digits=10, decimal_places=4)  # Field name made lowercase.
    averagecost = models.DecimalField(db_column='AverageCost', max_digits=10, decimal_places=4)  # Field name made lowercase.
    lastcost = models.DecimalField(db_column='LastCost', max_digits=10, decimal_places=4)  # Field name made lowercase.
    fifocost = models.DecimalField(db_column='FIFOCost', max_digits=14, decimal_places=4)  # Field name made lowercase.
    minprice = models.DecimalField(db_column='MinPrice', max_digits=10, decimal_places=2)  # Field name made lowercase.
    maxoff = models.PositiveIntegerField(db_column='MaxOff')  # Field name made lowercase.
    openitem = models.IntegerField(db_column='OpenItem')  # Field name made lowercase.
    disable = models.IntegerField(db_column='Disable')  # Field name made lowercase.
    consign = models.PositiveIntegerField(db_column='Consign')  # Field name made lowercase.
    point = models.DecimalField(db_column='Point', max_digits=10, decimal_places=4)  # Field name made lowercase.
    remark = models.TextField(blank=True, null=True)
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


class ItemmasterBlockByBranch(models.Model):
    itemcode = models.OneToOneField(Itemmaster, models.DO_NOTHING, db_column='itemcode', primary_key=True)
    branch = models.ForeignKey('Locationgroup', models.DO_NOTHING, db_column='branch')
    sales_order = models.IntegerField()
    purchase_order = models.IntegerField()
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=15)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=15)
    ibt = models.IntegerField()
    cn = models.IntegerField()
    dn = models.IntegerField()
    cpo = models.IntegerField()
    pos = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'itemmaster_block_by_branch'
        unique_together = (('itemcode', 'branch'),)


class ItemmasterBranchStock(models.Model):
    branch = models.OneToOneField('Locationgroup', models.DO_NOTHING, db_column='branch', primary_key=True)
    itemcode = models.ForeignKey(Itemmaster, models.DO_NOTHING, db_column='itemcode')
    sellingprice = models.DecimalField(max_digits=14, decimal_places=2)
    stdcost = models.DecimalField(max_digits=14, decimal_places=4)
    averagecost = models.DecimalField(max_digits=14, decimal_places=4)
    lastcost = models.DecimalField(max_digits=14, decimal_places=4)
    fifocost = models.DecimalField(max_digits=14, decimal_places=4)
    qoh = models.DecimalField(db_column='QOH', max_digits=10, decimal_places=2)  # Field name made lowercase.
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=15)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=15)
    hq_update = models.IntegerField()
    price_inc_tax = models.DecimalField(max_digits=14, decimal_places=2)
    qoh_link = models.DecimalField(db_column='QOH_link', max_digits=10, decimal_places=2)  # Field name made lowercase.
    packsize = models.DecimalField(max_digits=10, decimal_places=4)
    ads = models.DecimalField(max_digits=10, decimal_places=2)
    ams = models.DecimalField(max_digits=10, decimal_places=2)
    aws = models.DecimalField(max_digits=10, decimal_places=2)
    days = models.DecimalField(max_digits=10, decimal_places=0)
    qty_po = models.DecimalField(max_digits=10, decimal_places=2)
    qty_req = models.DecimalField(max_digits=10, decimal_places=2)
    qty_so = models.DecimalField(max_digits=10, decimal_places=2)
    doh = models.DecimalField(max_digits=10, decimal_places=1)
    qty_pos = models.DecimalField(max_digits=10, decimal_places=2)
    qty_si = models.DecimalField(max_digits=10, decimal_places=2)
    date_start = models.DateField()
    date_stop = models.DateField()
    itemlink = models.ForeignKey(Itemmaster, models.DO_NOTHING, db_column='itemlink')
    qty_opn = models.DecimalField(max_digits=10, decimal_places=2)
    qty_rec = models.DecimalField(max_digits=10, decimal_places=2)
    qty_other = models.DecimalField(max_digits=10, decimal_places=2)
    first_gr_date = models.DateField()
    last_gr_date = models.DateField()
    last_gr_qty = models.DecimalField(max_digits=10, decimal_places=1)
    price_today_mb = models.DecimalField(max_digits=14, decimal_places=2)
    price_today_na = models.DecimalField(max_digits=14, decimal_places=2)
    recalc_at = models.DateTimeField()
    qty_tbr = models.DecimalField(max_digits=10, decimal_places=2)
    doh_new = models.DecimalField(max_digits=10, decimal_places=0)
    rank_cat_qty = models.CharField(max_length=1)
    rank_cat_amt = models.CharField(max_length=1)
    qty_promo = models.DecimalField(max_digits=10, decimal_places=2)
    ads_rep = models.DecimalField(max_digits=10, decimal_places=2)
    branch_itemtype = models.CharField(max_length=35)
    day_promo = models.DecimalField(max_digits=10, decimal_places=0)
    qty_hp_out = models.DecimalField(max_digits=10, decimal_places=2)
    qty_ibt_sales = models.DecimalField(max_digits=10, decimal_places=2)
    qty_ibt_grn = models.DecimalField(max_digits=10, decimal_places=2)
    qty_avail = models.DecimalField(max_digits=10, decimal_places=2)
    last_po_date = models.DateField()
    last_po_qty = models.DecimalField(max_digits=10, decimal_places=1)
    last_po_vendor = models.CharField(max_length=15, blank=True, null=True)
    last_po_refno = models.CharField(max_length=20, blank=True, null=True)
    last_gr_vendor = models.CharField(max_length=15, blank=True, null=True)
    last_gr_refno = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'itemmaster_branch_stock'
        unique_together = (('branch', 'itemcode'),)


class ItemmasterItemtype(models.Model):
    itemcode = models.ForeignKey(Itemmaster, models.DO_NOTHING, db_column='itemcode')
    itemtype_guid = models.CharField(primary_key=True, max_length=32)
    concept = models.CharField(max_length=32)
    itemtype = models.CharField(max_length=35)
    date_from = models.DateField()
    date_to = models.DateField()
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=15)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=15)
    cancel = models.IntegerField()
    cancel_at = models.DateTimeField()
    last_refno = models.CharField(max_length=20)
    future_eff_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'itemmaster_itemtype'


class ItemmasterListedBranch(models.Model):
    itemcode = models.OneToOneField(Itemmaster, models.DO_NOTHING, db_column='itemcode', primary_key=True)
    branch = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=15)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=15)
    itemtype = models.CharField(db_column='ItemType', max_length=35)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'itemmaster_listed_branch'
        unique_together = (('itemcode', 'branch'),)


class ItemmasterMiscellaneous(models.Model):
    mis_guid = models.CharField(primary_key=True, max_length=32)
    itemcode = models.ForeignKey(Itemmaster, models.DO_NOTHING, db_column='itemcode')
    seq = models.IntegerField()
    text1 = models.CharField(max_length=60)
    value1 = models.DecimalField(max_digits=10, decimal_places=2)
    text2 = models.CharField(max_length=60)
    value2 = models.DecimalField(max_digits=10, decimal_places=2)
    remark = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=15)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=15)
    set_active = models.IntegerField()
    misc_group = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'itemmaster_miscellaneous'
        unique_together = (('itemcode', 'misc_group'),)


class ItemmasterOthersinfo(models.Model):
    oinfo_guid = models.CharField(primary_key=True, max_length=32)
    itemcode = models.OneToOneField(Itemmaster, models.DO_NOTHING, db_column='itemcode')
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


class ItemmasterPricetype(models.Model):
    itemcode = models.ForeignKey(Itemmaster, models.DO_NOTHING, db_column='itemcode')
    pricetype_guid = models.CharField(primary_key=True, max_length=32)
    concept = models.CharField(max_length=32)
    pricetype = models.CharField(max_length=30)
    date_from = models.DateField()
    date_to = models.DateField()
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=15)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=15)
    cancel = models.IntegerField()
    cancel_at = models.DateTimeField()
    last_refno = models.CharField(max_length=20)
    future_eff_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'itemmaster_pricetype'


class ItemmasterReplenishment(models.Model):
    im_rep_guid = models.CharField(max_length=32)
    itemcode = models.OneToOneField(Itemmaster, models.DO_NOTHING, db_column='itemcode', primary_key=True)
    concept = models.CharField(max_length=32)
    min_qty = models.DecimalField(max_digits=10, decimal_places=4)
    max_qty = models.DecimalField(max_digits=10, decimal_places=4)
    display_qty = models.DecimalField(max_digits=10, decimal_places=4)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=15)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'itemmaster_replenishment'
        unique_together = (('itemcode', 'concept'),)


class Itemmastersupcode(models.Model):
    itemcode = models.ForeignKey(Itemmaster, models.DO_NOTHING, db_column='Itemcode')  # Field name made lowercase.
    code = models.OneToOneField('Supcus', models.DO_NOTHING, db_column='Code', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=60)  # Field name made lowercase.
    supitemcode = models.CharField(db_column='SupItemCode', max_length=30)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='Created_at')  # Field name made lowercase.
    created_by = models.CharField(db_column='Created_by', max_length=15)  # Field name made lowercase.
    updated_at = models.DateTimeField(db_column='Updated_at')  # Field name made lowercase.
    updated_by = models.CharField(db_column='Updated_by', max_length=15)  # Field name made lowercase.
    item_desc = models.CharField(db_column='ITEM_DESC', max_length=40)  # Field name made lowercase.
    suplastprice = models.DecimalField(db_column='SupLastPrice', max_digits=12, decimal_places=4)  # Field name made lowercase.
    supstdprice = models.DecimalField(db_column='SupStdPrice', max_digits=12, decimal_places=4)  # Field name made lowercase.
    disc1type = models.CharField(db_column='Disc1Type', max_length=1)  # Field name made lowercase.
    disc1value = models.DecimalField(db_column='Disc1Value', max_digits=10, decimal_places=2)  # Field name made lowercase.
    disc2type = models.CharField(db_column='Disc2Type', max_length=1)  # Field name made lowercase.
    disc2value = models.DecimalField(db_column='Disc2Value', max_digits=10, decimal_places=2)  # Field name made lowercase.
    netunitprice = models.DecimalField(db_column='NetUnitPrice', max_digits=10, decimal_places=4)  # Field name made lowercase.
    cartonprice = models.DecimalField(db_column='CartonPrice', max_digits=10, decimal_places=4)  # Field name made lowercase.
    block_order = models.IntegerField()
    priority_vendor = models.IntegerField()
    none_return = models.IntegerField()
    supbulkqty = models.DecimalField(db_column='SupBulkQty', max_digits=10, decimal_places=4)  # Field name made lowercase.
    suprspaftertax = models.DecimalField(db_column='SupRSPAfterTax', max_digits=10, decimal_places=2)  # Field name made lowercase.
    suprspbeforetax = models.DecimalField(db_column='SupRSPBeforeTax', max_digits=10, decimal_places=2)  # Field name made lowercase.
    future_effdate = models.DateField(db_column='future_EffDate')  # Field name made lowercase.
    future_itemtype = models.CharField(db_column='future_ItemType', max_length=35)  # Field name made lowercase.
    future_supstdprice = models.DecimalField(db_column='future_SupStdPrice', max_digits=10, decimal_places=4)  # Field name made lowercase.
    future_supdisc1type = models.CharField(db_column='future_SupDisc1Type', max_length=1)  # Field name made lowercase.
    future_supdisc1value = models.DecimalField(db_column='future_SupDisc1Value', max_digits=10, decimal_places=2)  # Field name made lowercase.
    future_supdisc2type = models.CharField(db_column='future_SupDisc2Type', max_length=1)  # Field name made lowercase.
    future_supdisc2value = models.DecimalField(db_column='future_SupDisc2Value', max_digits=10, decimal_places=2)  # Field name made lowercase.
    future_netunitprice = models.DecimalField(db_column='future_NetUnitPrice', max_digits=10, decimal_places=4)  # Field name made lowercase.
    future_cartonprice = models.DecimalField(db_column='future_CartonPrice', max_digits=10, decimal_places=4)  # Field name made lowercase.
    orderlotsize = models.DecimalField(db_column='OrderLotSize', max_digits=10, decimal_places=4)  # Field name made lowercase.
    taxintno = models.IntegerField(db_column='TaxIntNo')  # Field name made lowercase.
    taxcode = models.CharField(db_column='TaxCode', max_length=15)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'itemmastersupcode'
        unique_together = (('itemcode', 'priority_vendor'), ('code', 'itemcode'),)


class Location(models.Model):
    code = models.CharField(db_column='Code', primary_key=True, max_length=10)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50)  # Field name made lowercase.
    locgroup = models.ForeignKey('Locationgroup', models.DO_NOTHING, db_column='LocGroup')  # Field name made lowercase.
    salesloc = models.IntegerField(db_column='SalesLoc')  # Field name made lowercase.
    replenishlevel = models.IntegerField()
    replenishqty = models.IntegerField()
    badstock = models.IntegerField(db_column='BadStock')  # Field name made lowercase.
    remark = models.TextField(db_column='Remark', blank=True, null=True)  # Field name made lowercase.
    loc_address = models.TextField(blank=True, null=True)
    loc_tel = models.CharField(max_length=20, blank=True, null=True)
    loc_fax = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location'


class Locationgroup(models.Model):
    code = models.CharField(db_column='Code', primary_key=True, max_length=10)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=50, blank=True, null=True)  # Field name made lowercase.
    set_active = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'locationgroup'


class Poamendchild(models.Model):
    refno = models.OneToOneField('Poamendmain', models.DO_NOTHING, db_column='RefNo', primary_key=True)  # Field name made lowercase.
    line = models.IntegerField(db_column='Line')  # Field name made lowercase.
    entrytype = models.CharField(db_column='EntryType', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pricetype = models.CharField(db_column='PriceType', max_length=5, blank=True, null=True)  # Field name made lowercase.
    barcode = models.CharField(db_column='Barcode', max_length=30, blank=True, null=True)  # Field name made lowercase.
    itemcode = models.ForeignKey(Itemmaster, models.DO_NOTHING, db_column='Itemcode', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=40, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='Qty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    um = models.CharField(db_column='UM', max_length=5, blank=True, null=True)  # Field name made lowercase.
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    totalprice = models.DecimalField(db_column='TotalPrice', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    packsize = models.DecimalField(db_column='PackSize', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    colour = models.CharField(db_column='Colour', max_length=20, blank=True, null=True)  # Field name made lowercase.
    size = models.CharField(db_column='Size', max_length=20, blank=True, null=True)  # Field name made lowercase.
    brand = models.CharField(db_column='Brand', max_length=10, blank=True, null=True)  # Field name made lowercase.
    articleno = models.CharField(db_column='ArticleNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    poline = models.SmallIntegerField(db_column='POLine', blank=True, null=True)  # Field name made lowercase.
    porefno = models.CharField(db_column='PORefNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    amendqty = models.DecimalField(db_column='AmendQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    dept = models.CharField(db_column='Dept', max_length=6, blank=True, null=True)  # Field name made lowercase.
    subdept = models.CharField(db_column='SubDept', max_length=6, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=6, blank=True, null=True)  # Field name made lowercase.
    postdatetime_c = models.DateTimeField(blank=True, null=True)
    hq_update = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'poamendchild'
        unique_together = (('refno', 'line'),)


class Poamendmain(models.Model):
    refno = models.CharField(db_column='RefNo', primary_key=True, max_length=20, db_collation='latin1_swedish_ci')  # Field name made lowercase.
    amenddate = models.DateField(db_column='AmendDate', blank=True, null=True)  # Field name made lowercase.
    amendreason = models.TextField(db_column='AmendReason', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    issuestamp = models.DateTimeField(db_column='IssueStamp', blank=True, null=True)  # Field name made lowercase.
    laststamp = models.DateTimeField(db_column='LastStamp', blank=True, null=True)  # Field name made lowercase.
    porefno = models.CharField(db_column='PORefNo', max_length=20, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    podate = models.DateField(db_column='PODate', blank=True, null=True)  # Field name made lowercase.
    issuedby = models.CharField(db_column='IssuedBy', max_length=80, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    dept = models.CharField(db_column='Dept', max_length=30, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=10, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    scode = models.CharField(db_column='SCode', max_length=15, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    sname = models.CharField(db_column='SName', max_length=60, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    billstatus = models.IntegerField(db_column='BillStatus', blank=True, null=True)  # Field name made lowercase.
    accstatus = models.IntegerField(db_column='AccStatus', blank=True, null=True)  # Field name made lowercase.
    closed = models.IntegerField(db_column='Closed', blank=True, null=True)  # Field name made lowercase.
    rejected = models.IntegerField(db_column='Rejected', blank=True, null=True)  # Field name made lowercase.
    postby = models.CharField(max_length=20, db_collation='latin1_swedish_ci', blank=True, null=True)
    postdatetime = models.DateTimeField(blank=True, null=True)
    loc_group = models.CharField(max_length=10, db_collation='latin1_swedish_ci')
    hq_update = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'poamendmain'


class Pochild(models.Model):
    refno = models.OneToOneField('Pomain', models.DO_NOTHING, db_column='RefNo', primary_key=True)  # Field name made lowercase.
    line = models.PositiveSmallIntegerField(db_column='Line')  # Field name made lowercase.
    entrytype = models.CharField(db_column='EntryType', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pricetype = models.CharField(db_column='PriceType', max_length=5, blank=True, null=True)  # Field name made lowercase.
    barcode = models.CharField(db_column='Barcode', max_length=30, blank=True, null=True)  # Field name made lowercase.
    itemcode = models.CharField(db_column='Itemcode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=40, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='Qty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    um = models.CharField(db_column='UM', max_length=5, blank=True, null=True)  # Field name made lowercase.
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    disc1type = models.CharField(db_column='Disc1Type', max_length=1, blank=True, null=True)  # Field name made lowercase.
    disc1value = models.DecimalField(db_column='Disc1Value', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    disc2type = models.CharField(db_column='Disc2Type', max_length=1, blank=True, null=True)  # Field name made lowercase.
    disc2value = models.DecimalField(db_column='Disc2Value', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    netunitprice = models.DecimalField(db_column='NetUnitPrice', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    discamt = models.DecimalField(db_column='DiscAmt', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    totalprice = models.DecimalField(db_column='TotalPrice', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    packsize = models.DecimalField(db_column='PackSize', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    colour = models.CharField(db_column='Colour', max_length=20, blank=True, null=True)  # Field name made lowercase.
    size = models.CharField(db_column='Size', max_length=20, blank=True, null=True)  # Field name made lowercase.
    brand = models.CharField(db_column='Brand', max_length=10, blank=True, null=True)  # Field name made lowercase.
    articleno = models.CharField(db_column='ArticleNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    temprecvqty = models.DecimalField(db_column='TempRecvQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    receivedqty = models.DecimalField(db_column='ReceivedQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    balanceqty = models.DecimalField(db_column='BalanceQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    tempitem = models.IntegerField(db_column='TempItem', blank=True, null=True)  # Field name made lowercase.
    tempitemchanged = models.IntegerField(db_column='TempItemChanged', blank=True, null=True)  # Field name made lowercase.
    discvalue = models.DecimalField(db_column='DiscValue', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    costaftdisc = models.DecimalField(db_column='CostAftDisc', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    costfactor = models.DecimalField(db_column='CostFactor', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    invactcost = models.DecimalField(db_column='InvActCost', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    invacttotcost = models.DecimalField(db_column='InvActTotCost', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    sysqoh = models.DecimalField(db_column='SysQOH', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    sysavgcost = models.DecimalField(db_column='SysAvgCost', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    weightavgcost = models.DecimalField(db_column='WeightAvgCost', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    groupno = models.IntegerField(db_column='GroupNo', blank=True, null=True)  # Field name made lowercase.
    groupno2 = models.IntegerField(db_column='GroupNo2', blank=True, null=True)  # Field name made lowercase.
    itemlink = models.CharField(db_column='ItemLink', max_length=20, blank=True, null=True)  # Field name made lowercase.
    amendment = models.IntegerField(db_column='Amendment', blank=True, null=True)  # Field name made lowercase.
    amendqty = models.DecimalField(db_column='AmendQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    bulkqty = models.DecimalField(db_column='BulkQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    umbulk = models.CharField(db_column='UMBulk', max_length=5, blank=True, null=True)  # Field name made lowercase.
    bqty = models.DecimalField(db_column='BQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pqty = models.DecimalField(db_column='PQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    itemremark = models.TextField(db_column='ItemRemark', blank=True, null=True)  # Field name made lowercase.
    dept = models.CharField(db_column='Dept', max_length=6, blank=True, null=True)  # Field name made lowercase.
    subdept = models.CharField(db_column='SubDept', max_length=6, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=6, blank=True, null=True)  # Field name made lowercase.
    onhandqty = models.DecimalField(db_column='OnHandQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    avgpesalesqty = models.DecimalField(db_column='AvgPESalesQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    lastpesalesqty = models.DecimalField(db_column='LastPESalesQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    sellingprice = models.DecimalField(db_column='SellingPrice', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    mrank = models.CharField(max_length=1, blank=True, null=True)
    cartonprice = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    lastcost = models.DecimalField(db_column='LastCost', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    poitemavgcost = models.DecimalField(db_column='POItemAvgCost', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    groupcost = models.IntegerField(db_column='GroupCost', blank=True, null=True)  # Field name made lowercase.
    invturnover = models.DecimalField(db_column='InvTurnOver', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    soldbyweight = models.IntegerField(db_column='SoldByWeight', blank=True, null=True)  # Field name made lowercase.
    sales_current = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    group_status = models.IntegerField(blank=True, null=True)
    group_sequence = models.IntegerField(blank=True, null=True)
    hq_update = models.IntegerField(blank=True, null=True)
    cp_child_guid = models.CharField(max_length=32, blank=True, null=True)
    purtolerance_std_plus = models.DecimalField(db_column='PurTolerance_Std_plus', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    purtolerance_std_minus = models.DecimalField(db_column='PurTolerance_Std_Minus', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    weighttraceqty = models.IntegerField(db_column='WeightTraceQty', blank=True, null=True)  # Field name made lowercase.
    weighttraceqtyuom = models.CharField(db_column='WeightTraceQtyUOM', max_length=5, blank=True, null=True)  # Field name made lowercase.
    weighttraceqtycount = models.DecimalField(db_column='WeightTraceQtyCount', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pe_qty_rec = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    pe_qty_pos = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    pe_qty_si = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    pe_qty_dn = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    pe_qty_cn = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    pe_qty_adj = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    pe_qty_hamper = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    price_posnet = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    price_future = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    link_guid = models.CharField(max_length=32, blank=True, null=True)
    stockday_min_qty = models.IntegerField(blank=True, null=True)
    stockday_max_qty = models.SmallIntegerField(blank=True, null=True)
    stockday_first_grn_date = models.DateField(blank=True, null=True)
    stockday_interval_days = models.IntegerField(blank=True, null=True)
    stockday_pos_qty_sum = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    stockday_pos_qty_avg = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    stockday_openingqty = models.DecimalField(db_column='stockday_OpeningQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    stockday_onhandqty = models.DecimalField(db_column='stockday_OnHandQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    stockday_possalesqty = models.DecimalField(db_column='stockday_PosSalesQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    stockday_invsalesqty = models.DecimalField(db_column='stockday_InvSalesQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    stockday_adjustqty = models.DecimalField(db_column='stockday_AdjustQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    stockday_soqty = models.DecimalField(db_column='stockday_SOQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    stockday_poqty = models.DecimalField(db_column='stockday_POQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    stockday_recqty = models.DecimalField(db_column='stockday_RecQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    stockday_hamperqty = models.DecimalField(db_column='stockday_HamperQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    stockday_creditqty = models.DecimalField(db_column='stockday_CreditQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    stockday_debitqty = models.DecimalField(db_column='stockday_DebitQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    stockday_exchangeqty = models.DecimalField(db_column='stockday_ExchangeQty', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    stockday_poamount = models.DecimalField(db_column='stockday_POAmount', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    hcost_po = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    hcost_po_unit = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    cost_manual = models.IntegerField(blank=True, null=True)
    cost_manual_value = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    cat_max = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cat_min = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    last_grndate = models.DateField(blank=True, null=True)
    last_qty = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    last_supcode = models.CharField(max_length=20, blank=True, null=True)
    pe_qty_firstdate = models.DateField(blank=True, null=True)
    pe_qty_open = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    pgrqty = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    pother = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    psoldqty = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    rebate_value = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    postdatetime = models.DateTimeField(blank=True, null=True)
    gst_tax_type = models.CharField(max_length=5, blank=True, null=True)
    gst_tax_code = models.CharField(max_length=10, blank=True, null=True)
    gst_tax_rate = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    gst_tax_amount = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    price_include_tax = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    totalprice_include_tax = models.DecimalField(db_column='TotalPrice_include_tax', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    surchgvalue = models.DecimalField(db_column='SurchgValue', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    e_foc = models.DecimalField(db_column='E_FOC', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    e_foc_line = models.SmallIntegerField(db_column='E_FOC_Line', blank=True, null=True)  # Field name made lowercase.
    e_price = models.DecimalField(db_column='E_Price', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    e_discount_rule = models.CharField(db_column='E_Discount_Rule', max_length=15, blank=True, null=True)  # Field name made lowercase.
    e_discount_value = models.DecimalField(db_column='E_Discount_Value', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    e_gross = models.DecimalField(db_column='E_Gross', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    e_price_net = models.DecimalField(db_column='E_Price_Net', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    e_total_bf_tax = models.DecimalField(db_column='E_Total_bf_Tax', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    e_taxamt = models.DecimalField(db_column='E_TaxAmt', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    e_total_af_tax = models.DecimalField(db_column='E_Total_af_Tax', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    taxintno = models.IntegerField(db_column='TaxIntNo', blank=True, null=True)  # Field name made lowercase.
    taxcodemap = models.CharField(db_column='TaxCodeMap', max_length=15, blank=True, null=True)  # Field name made lowercase.
    taxvalue = models.DecimalField(db_column='TaxValue', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    taxamount = models.DecimalField(db_column='TaxAmount', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    taxamountvariance = models.DecimalField(db_column='TaxAmountVariance', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pochild'
        unique_together = (('refno', 'line'),)


class Pomain(models.Model):
    refno = models.CharField(db_column='RefNo', primary_key=True, max_length=20)  # Field name made lowercase.
    podate = models.DateField(db_column='PODate', blank=True, null=True)  # Field name made lowercase.
    deliverdate = models.DateField(db_column='DeliverDate', blank=True, null=True)  # Field name made lowercase.
    duedate = models.DateField(db_column='DueDate', blank=True, null=True)  # Field name made lowercase.
    issuestamp = models.DateTimeField(db_column='IssueStamp', blank=True, null=True)  # Field name made lowercase.
    issuedby = models.CharField(db_column='IssuedBy', max_length=80, blank=True, null=True)  # Field name made lowercase.
    laststamp = models.DateTimeField()
    dept = models.CharField(db_column='Dept', max_length=30, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=10, blank=True, null=True)  # Field name made lowercase.
    approvedby = models.CharField(db_column='ApprovedBy', max_length=60, blank=True, null=True)  # Field name made lowercase.
    scode = models.CharField(db_column='SCode', max_length=15, blank=True, null=True)  # Field name made lowercase.
    sname = models.CharField(db_column='SName', max_length=60, blank=True, null=True)  # Field name made lowercase.
    sterm = models.CharField(db_column='STerm', max_length=30, blank=True, null=True)  # Field name made lowercase.
    stel = models.CharField(db_column='STel', max_length=20, blank=True, null=True)  # Field name made lowercase.
    sfax = models.CharField(db_column='SFax', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remark = models.TextField(db_column='Remark', blank=True, null=True)  # Field name made lowercase.
    subtotal1 = models.DecimalField(db_column='SubTotal1', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    discount1 = models.DecimalField(db_column='Discount1', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    discount1type = models.CharField(db_column='Discount1Type', max_length=1, blank=True, null=True)  # Field name made lowercase.
    subtotal2 = models.DecimalField(db_column='SubTotal2', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    discount2 = models.DecimalField(db_column='Discount2', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    discount2type = models.CharField(db_column='Discount2Type', max_length=1, blank=True, null=True)  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    billstatus = models.IntegerField(db_column='BillStatus', blank=True, null=True)  # Field name made lowercase.
    accstatus = models.IntegerField(db_column='AccStatus', blank=True, null=True)  # Field name made lowercase.
    closed = models.IntegerField(db_column='Closed', blank=True, null=True)  # Field name made lowercase.
    amendment = models.IntegerField(db_column='Amendment', blank=True, null=True)  # Field name made lowercase.
    completed = models.IntegerField(db_column='Completed', blank=True, null=True)  # Field name made lowercase.
    disc1percent = models.DecimalField(db_column='Disc1Percent', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    disc2percent = models.DecimalField(db_column='Disc2Percent', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    subdeptcode = models.CharField(db_column='SubDeptCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    postby = models.CharField(max_length=80, blank=True, null=True)
    postdatetime = models.DateTimeField(blank=True, null=True)
    calduedateby = models.CharField(db_column='CalDueDateby', max_length=30, blank=True, null=True)  # Field name made lowercase.
    expiry_date = models.DateField(blank=True, null=True)
    pur_expiry_days = models.IntegerField(blank=True, null=True)
    hq_update = models.IntegerField(blank=True, null=True)
    cp_main_guid = models.CharField(max_length=32, blank=True, null=True)
    autoclosepo = models.IntegerField(db_column='AutoClosePO', blank=True, null=True)  # Field name made lowercase.
    stockday_min = models.IntegerField(blank=True, null=True)
    stockday_max = models.IntegerField(blank=True, null=True)
    send = models.PositiveIntegerField(blank=True, null=True)
    send_remark = models.TextField(blank=True, null=True)
    send_at = models.DateTimeField(blank=True, null=True)
    send_by = models.CharField(max_length=20, blank=True, null=True)
    rejected = models.IntegerField(blank=True, null=True)
    rejected_remark = models.TextField(blank=True, null=True)
    rejected_at = models.DateTimeField(blank=True, null=True)
    rejected_by = models.CharField(max_length=20, blank=True, null=True)
    approved = models.IntegerField(blank=True, null=True)
    approved_remark = models.TextField(blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    approved_by = models.CharField(max_length=20, blank=True, null=True)
    loc_group = models.CharField(max_length=10, blank=True, null=True)
    run_cost = models.IntegerField(blank=True, null=True)
    rebate_amt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dn_amt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    in_kind = models.IntegerField(blank=True, null=True)
    cross_ref = models.CharField(max_length=32, blank=True, null=True)
    cross_ref_module = models.CharField(max_length=32, blank=True, null=True)
    hq_issue = models.IntegerField(blank=True, null=True)
    gst_tax_sum = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax_code_purchase = models.CharField(max_length=10, blank=True, null=True)
    total_include_tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gst_tax_rate = models.IntegerField(blank=True, null=True)
    price_include_tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    surchg_tax_sum = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax_inclusive = models.SmallIntegerField(blank=True, null=True)
    doc_name_reg = models.CharField(max_length=80, blank=True, null=True)
    ibt = models.IntegerField(blank=True, null=True)
    multi_tax_code = models.IntegerField(blank=True, null=True)
    refno2 = models.CharField(max_length=20, blank=True, null=True)
    discount_as_inv = models.IntegerField(blank=True, null=True)
    ibt_gst = models.IntegerField(blank=True, null=True)
    rebate_as_inv = models.IntegerField(blank=True, null=True)
    uploaded = models.IntegerField(blank=True, null=True)
    uploaded_at = models.DateTimeField(blank=True, null=True)
    unpost = models.IntegerField(blank=True, null=True)
    unpost_at = models.DateTimeField(blank=True, null=True)
    unpost_by = models.CharField(max_length=20, blank=True, null=True)
    cancel = models.IntegerField(blank=True, null=True)
    cancel_at = models.DateTimeField(blank=True, null=True)
    cancel_by = models.CharField(max_length=20, blank=True, null=True)
    cancel_reason = models.CharField(max_length=32, blank=True, null=True)
    b2b_status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pomain'


class SetConcept(models.Model):
    concept_guid = models.CharField(primary_key=True, max_length=32)
    concept = models.CharField(unique=True, max_length=30)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=15)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=15)
    inactive = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'set_concept'


class SetConceptBranch(models.Model):
    branch_guid = models.CharField(primary_key=True, max_length=32)
    concept_guid = models.ForeignKey(SetConcept, models.DO_NOTHING, db_column='concept_guid')
    branch = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=15)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=15)
    inactive = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'set_concept_branch'
        unique_together = (('branch', 'concept_guid'),)


class SetGen(models.Model):
    set_gen_guid = models.CharField(primary_key=True, max_length=32, db_collation='latin1_swedish_ci')
    gen_link_guid = models.CharField(max_length=32, db_collation='latin1_swedish_ci')
    gen_type = models.CharField(max_length=32, db_collation='latin1_swedish_ci')
    is_global = models.IntegerField()
    concept_guid = models.CharField(max_length=32)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=15, db_collation='latin1_swedish_ci')
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=15, db_collation='latin1_swedish_ci')

    class Meta:
        managed = False
        db_table = 'set_gen'


class SetGenC(models.Model):
    set_gen_c_guid = models.CharField(primary_key=True, max_length=32, db_collation='latin1_swedish_ci')
    gen_link_guid = models.ForeignKey(SetGen, models.DO_NOTHING, db_column='gen_link_guid')
    param_guid = models.CharField(max_length=32, db_collation='latin1_swedish_ci')
    param_module = models.CharField(max_length=32, db_collation='latin1_swedish_ci')
    param_type = models.CharField(max_length=32)
    param_group = models.CharField(max_length=32, db_collation='latin1_swedish_ci')
    param_desc = models.CharField(max_length=60, db_collation='latin1_swedish_ci')
    field_checkbox = models.IntegerField()
    field_integer = models.PositiveSmallIntegerField()
    field_double = models.DecimalField(max_digits=10, decimal_places=4)
    field_varchar = models.CharField(max_length=20, db_collation='latin1_swedish_ci')
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=15, db_collation='latin1_swedish_ci')
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=15, db_collation='latin1_swedish_ci')

    class Meta:
        managed = False
        db_table = 'set_gen_c'


class SetGroup(models.Model):
    group_guid = models.CharField(db_column='GROUP_GUID', unique=True, max_length=32)  # Field name made lowercase.
    group_code = models.CharField(db_column='GROUP_CODE', primary_key=True, max_length=10)  # Field name made lowercase.
    group_desc = models.CharField(db_column='GROUP_DESC', max_length=40)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='CREATED_AT')  # Field name made lowercase.
    created_by = models.CharField(db_column='CREATED_BY', max_length=30)  # Field name made lowercase.
    updated_at = models.DateTimeField(db_column='UPDATED_AT')  # Field name made lowercase.
    updated_by = models.CharField(db_column='UPDATED_BY', max_length=30)  # Field name made lowercase.
    group_code_acc = models.CharField(max_length=20)
    code_acc = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'set_group'


class SetGroupDept(models.Model):
    dept_guid = models.CharField(db_column='DEPT_GUID', unique=True, max_length=32)  # Field name made lowercase.
    group_code = models.ForeignKey(SetGroup, models.DO_NOTHING, db_column='GROUP_CODE')  # Field name made lowercase.
    dept_code = models.CharField(db_column='DEPT_CODE', primary_key=True, max_length=6)  # Field name made lowercase.
    dept_desc = models.CharField(db_column='DEPT_DESC', max_length=40)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='CREATED_AT')  # Field name made lowercase.
    created_by = models.CharField(db_column='CREATED_BY', max_length=30)  # Field name made lowercase.
    updated_at = models.DateTimeField(db_column='UPDATED_AT')  # Field name made lowercase.
    updated_by = models.CharField(db_column='UPDATED_BY', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'set_group_dept'


class SiPayment(models.Model):
    refno = models.CharField(db_column='RefNo', primary_key=True, max_length=20)  # Field name made lowercase.
    line = models.FloatField(db_column='Line')  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=10, blank=True, null=True)  # Field name made lowercase.
    bizdate = models.DateField(db_column='BizDate', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=20, blank=True, null=True)
    paytype = models.CharField(db_column='PayType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    paydescription = models.CharField(db_column='PayDescription', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cardtype = models.CharField(db_column='CardType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cardno = models.CharField(db_column='Cardno', max_length=30, blank=True, null=True)  # Field name made lowercase.
    carddate = models.DateField(db_column='CardDate', blank=True, null=True)  # Field name made lowercase.
    cardapproval = models.CharField(db_column='CardApproval', max_length=50, blank=True, null=True)  # Field name made lowercase.
    voucherno = models.CharField(db_column='VoucherNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    payamt = models.FloatField(db_column='PayAmt', blank=True, null=True)  # Field name made lowercase.
    appliedamt = models.FloatField(db_column='AppliedAmt', blank=True, null=True)  # Field name made lowercase.
    value_factor = models.FloatField(db_column='Value_Factor', blank=True, null=True)  # Field name made lowercase.
    retention_amt = models.FloatField(db_column='Retention_amt', blank=True, null=True)  # Field name made lowercase.
    hq_update = models.SmallIntegerField(blank=True, null=True)
    loc_group = models.CharField(max_length=20, blank=True, null=True)
    currencycode = models.CharField(db_column='CurrencyCode', max_length=6, blank=True, null=True)  # Field name made lowercase.
    exchangevalue = models.FloatField(db_column='ExchangeValue', blank=True, null=True)  # Field name made lowercase.
    exchangerate = models.FloatField(db_column='ExchangeRate', blank=True, null=True)  # Field name made lowercase.
    merchant_no = models.CharField(max_length=20, blank=True, null=True)
    updatememberspoint = models.SmallIntegerField(db_column='UpdateMembersPoint', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'si_payment'
        unique_together = (('refno', 'line'),)


class SiPrice(models.Model):
    trans_guid = models.CharField(primary_key=True, max_length=32)
    refno = models.CharField(unique=True, max_length=20, blank=True, null=True)
    price_code = models.CharField(max_length=20, blank=True, null=True)
    date_effective = models.DateField(blank=True, null=True)
    date_with_expiry = models.SmallIntegerField(blank=True, null=True)
    date_expiry = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    trans_type = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=20, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=20, blank=True, null=True)
    posted = models.SmallIntegerField(blank=True, null=True)
    posted_at = models.DateTimeField(blank=True, null=True)
    posted_by = models.CharField(max_length=20, blank=True, null=True)
    loc_group = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'si_price'


class SiPriceChild(models.Model):
    child_guid = models.CharField(primary_key=True, max_length=32)
    trans_guid = models.CharField(max_length=32, blank=True, null=True)
    itemcode = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=60, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    disc1_type = models.CharField(max_length=1, blank=True, null=True)
    disc1_value = models.FloatField(blank=True, null=True)
    disc2_type = models.CharField(max_length=1, blank=True, null=True)
    disc2_value = models.FloatField(blank=True, null=True)
    price_net = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=20, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=20, blank=True, null=True)
    price_min = models.FloatField(blank=True, null=True)
    price_max = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'si_price_child'


class SiPriceRules(models.Model):
    rules_guid = models.CharField(primary_key=True, max_length=32)
    rules_code = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=20, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=20, blank=True, null=True)
    set_disable = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'si_price_rules'


class SiPriceRulesC(models.Model):
    child_guid = models.CharField(primary_key=True, max_length=32)
    rules_guid = models.CharField(max_length=32, blank=True, null=True)
    seq = models.IntegerField(db_column='Seq', blank=True, null=True)  # Field name made lowercase.
    rules_desc = models.CharField(max_length=50, blank=True, null=True)
    rules_type = models.CharField(max_length=10, blank=True, null=True)
    rules_query = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=20, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'si_price_rules_c'


class Sichild(models.Model):
    refno = models.CharField(db_column='RefNo', primary_key=True, max_length=15)  # Field name made lowercase.
    line = models.IntegerField(db_column='Line')  # Field name made lowercase.
    entrytype = models.CharField(db_column='EntryType', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pricetype = models.CharField(db_column='PriceType', max_length=5, blank=True, null=True)  # Field name made lowercase.
    barcode = models.CharField(db_column='Barcode', max_length=30, blank=True, null=True)  # Field name made lowercase.
    itemcode = models.CharField(db_column='Itemcode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='Qty', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    um = models.CharField(db_column='UM', max_length=5, blank=True, null=True)  # Field name made lowercase.
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    disc1type = models.CharField(db_column='Disc1Type', max_length=1, blank=True, null=True)  # Field name made lowercase.
    disc1value = models.DecimalField(db_column='Disc1Value', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    disc2type = models.CharField(db_column='Disc2Type', max_length=1, blank=True, null=True)  # Field name made lowercase.
    disc2value = models.DecimalField(db_column='Disc2Value', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    netunitprice = models.DecimalField(db_column='NetUnitPrice', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    discamt = models.DecimalField(db_column='DiscAmt', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    totalprice = models.DecimalField(db_column='TotalPrice', max_digits=14, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    packsize = models.FloatField(db_column='PackSize', blank=True, null=True)  # Field name made lowercase.
    colour = models.CharField(db_column='Colour', max_length=20, blank=True, null=True)  # Field name made lowercase.
    size = models.CharField(db_column='Size', max_length=20, blank=True, null=True)  # Field name made lowercase.
    brand = models.CharField(db_column='Brand', max_length=5, blank=True, null=True)  # Field name made lowercase.
    articleno = models.CharField(db_column='ArticleNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    sysqoh = models.FloatField(db_column='SysQOH', blank=True, null=True)  # Field name made lowercase.
    sysavgcost = models.FloatField(db_column='SysAvgCost', blank=True, null=True)  # Field name made lowercase.
    itemlink = models.CharField(db_column='ItemLink', max_length=20, blank=True, null=True)  # Field name made lowercase.
    amendment = models.IntegerField(db_column='Amendment', blank=True, null=True)  # Field name made lowercase.
    bulkqty = models.FloatField(db_column='BulkQty', blank=True, null=True)  # Field name made lowercase.
    umbulk = models.CharField(db_column='UMBulk', max_length=5, blank=True, null=True)  # Field name made lowercase.
    bqty = models.FloatField(db_column='BQty', blank=True, null=True)  # Field name made lowercase.
    pqty = models.FloatField(db_column='PQty', blank=True, null=True)  # Field name made lowercase.
    itemremark = models.TextField(db_column='ItemRemark', blank=True, null=True)  # Field name made lowercase.
    dept = models.CharField(db_column='Dept', max_length=5, blank=True, null=True)  # Field name made lowercase.
    subdept = models.CharField(db_column='SubDept', max_length=5, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=5, blank=True, null=True)  # Field name made lowercase.
    onhandqty = models.FloatField(db_column='OnHandQty', blank=True, null=True)  # Field name made lowercase.
    avgpesalesqty = models.FloatField(db_column='AvgPESalesQty', blank=True, null=True)  # Field name made lowercase.
    lastpesalesqty = models.FloatField(db_column='LastPESalesQty', blank=True, null=True)  # Field name made lowercase.
    sellingprice = models.FloatField(db_column='SellingPrice', blank=True, null=True)  # Field name made lowercase.
    mrank = models.CharField(max_length=1, blank=True, null=True)
    cartonprice = models.FloatField(blank=True, null=True)
    sorefno = models.CharField(max_length=15, blank=True, null=True)
    soline = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=10, blank=True, null=True)
    hq_update = models.SmallIntegerField(blank=True, null=True)
    purtolerance_std_plus = models.FloatField(db_column='PurTolerance_Std_plus', blank=True, null=True)  # Field name made lowercase.
    purtolerance_std_minus = models.FloatField(db_column='PurTolerance_Std_Minus', blank=True, null=True)  # Field name made lowercase.
    weighttraceqty = models.SmallIntegerField(db_column='WeightTraceQty', blank=True, null=True)  # Field name made lowercase.
    weighttraceqtyuom = models.CharField(db_column='WeightTraceQtyUOM', max_length=6, blank=True, null=True)  # Field name made lowercase.
    weighttraceqtycount = models.FloatField(db_column='WeightTraceQtyCount', blank=True, null=True)  # Field name made lowercase.
    gst_tax_type = models.CharField(max_length=5, blank=True, null=True)
    gst_tax_code = models.CharField(max_length=10, blank=True, null=True)
    gst_tax_rate = models.FloatField(blank=True, null=True)
    gst_tax_amount = models.FloatField(blank=True, null=True)
    price_include_tax = models.FloatField(blank=True, null=True)
    totalprice_include_tax = models.FloatField(db_column='TotalPrice_include_tax', blank=True, null=True)  # Field name made lowercase.
    discvalue = models.FloatField(blank=True, null=True)
    postdatetime_c = models.DateTimeField(blank=True, null=True)
    surchg_value = models.FloatField(blank=True, null=True)
    unitactprice = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    consign = models.SmallIntegerField(blank=True, null=True)
    surchg_disc_gst = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    itemtype = models.CharField(max_length=40, blank=True, null=True)
    costmarginvalue = models.FloatField(blank=True, null=True)
    costmargin = models.SmallIntegerField(blank=True, null=True)
    soldbyweight = models.SmallIntegerField(blank=True, null=True)
    points = models.FloatField(db_column='Points', blank=True, null=True)  # Field name made lowercase.
    lastcost = models.FloatField(blank=True, null=True)
    fifocost = models.FloatField(blank=True, null=True)
    cost_deduct = models.FloatField(blank=True, null=True)
    gst_manual = models.SmallIntegerField(blank=True, null=True)
    taxintno = models.IntegerField(db_column='TaxIntNo', blank=True, null=True)  # Field name made lowercase.
    taxcodemap = models.CharField(db_column='TaxCodeMap', max_length=15, blank=True, null=True)  # Field name made lowercase.
    taxvalue = models.FloatField(db_column='TaxValue', blank=True, null=True)  # Field name made lowercase.
    taxamount = models.FloatField(db_column='TaxAmount', blank=True, null=True)  # Field name made lowercase.
    taxamountvariance = models.FloatField(db_column='TaxAmountVariance', blank=True, null=True)  # Field name made lowercase.
    promo_refno = models.CharField(max_length=20, blank=True, null=True)
    claim_amt_unit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    item_volume = models.FloatField(blank=True, null=True)
    item_weight = models.FloatField(blank=True, null=True)
    ignore_price_rules = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sichild'
        unique_together = (('refno', 'line'),)


class Simain(models.Model):
    refno = models.CharField(db_column='RefNo', primary_key=True, max_length=15)  # Field name made lowercase.
    docno = models.CharField(db_column='DocNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    invoicedate = models.DateField(db_column='InvoiceDate', blank=True, null=True)  # Field name made lowercase.
    deliverdate = models.DateField(db_column='DeliverDate', blank=True, null=True)  # Field name made lowercase.
    issuestamp = models.DateTimeField(db_column='IssueStamp', blank=True, null=True)  # Field name made lowercase.
    issuedby = models.CharField(db_column='IssuedBy', max_length=80, blank=True, null=True)  # Field name made lowercase.
    laststamp = models.DateTimeField(db_column='LastStamp', blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=15, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=60, blank=True, null=True)  # Field name made lowercase.
    add1 = models.CharField(db_column='Add1', max_length=60, blank=True, null=True)  # Field name made lowercase.
    add2 = models.CharField(db_column='Add2', max_length=60, blank=True, null=True)  # Field name made lowercase.
    add3 = models.CharField(db_column='Add3', max_length=60, blank=True, null=True)  # Field name made lowercase.
    attn = models.CharField(db_column='Attn', max_length=60, blank=True, null=True)  # Field name made lowercase.
    term = models.CharField(max_length=20, blank=True, null=True)
    tel = models.CharField(db_column='Tel', max_length=20, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='Fax', max_length=20, blank=True, null=True)  # Field name made lowercase.
    dadd1 = models.CharField(db_column='DAdd1', max_length=60, blank=True, null=True)  # Field name made lowercase.
    dadd2 = models.CharField(db_column='DAdd2', max_length=60, blank=True, null=True)  # Field name made lowercase.
    dadd3 = models.CharField(db_column='DAdd3', max_length=60, blank=True, null=True)  # Field name made lowercase.
    dattn = models.CharField(db_column='DAttn', max_length=60, blank=True, null=True)  # Field name made lowercase.
    dtel = models.CharField(db_column='DTel', max_length=20, blank=True, null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remark = models.TextField(db_column='Remark', blank=True, null=True)  # Field name made lowercase.
    subtotal1 = models.FloatField(db_column='SubTotal1', blank=True, null=True)  # Field name made lowercase.
    discount1 = models.FloatField(db_column='Discount1', blank=True, null=True)  # Field name made lowercase.
    discount1type = models.CharField(db_column='Discount1Type', max_length=1, blank=True, null=True)  # Field name made lowercase.
    subtotal2 = models.FloatField(db_column='SubTotal2', blank=True, null=True)  # Field name made lowercase.
    discount2 = models.FloatField(db_column='Discount2', blank=True, null=True)  # Field name made lowercase.
    discount2type = models.CharField(db_column='Discount2Type', max_length=1, blank=True, null=True)  # Field name made lowercase.
    total = models.FloatField(db_column='Total', blank=True, null=True)  # Field name made lowercase.
    billstatus = models.SmallIntegerField(db_column='BillStatus', blank=True, null=True)  # Field name made lowercase.
    disc1percent = models.FloatField(db_column='Disc1Percent', blank=True, null=True)  # Field name made lowercase.
    disc2percent = models.FloatField(db_column='Disc2Percent', blank=True, null=True)  # Field name made lowercase.
    subdeptcode = models.CharField(db_column='SubDeptCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    postby = models.CharField(max_length=80, blank=True, null=True)
    postdatetime = models.DateTimeField(blank=True, null=True)
    deflocation = models.CharField(max_length=10, blank=True, null=True)
    amtasdescription = models.CharField(db_column='AmtAsDescription', max_length=200, blank=True, null=True)  # Field name made lowercase.
    salesman = models.CharField(db_column='SALESMAN', max_length=30, blank=True, null=True)  # Field name made lowercase.
    export_account = models.CharField(db_column='EXPORT_ACCOUNT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    hq_update = models.SmallIntegerField(blank=True, null=True)
    converted_from_module = models.CharField(db_column='CONVERTED_FROM_MODULE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    converted_from_at = models.DateTimeField(db_column='CONVERTED_FROM_AT', blank=True, null=True)  # Field name made lowercase.
    converted_from_by = models.CharField(db_column='CONVERTED_FROM_BY', max_length=20, blank=True, null=True)  # Field name made lowercase.
    converted_from_guid = models.CharField(db_column='CONVERTED_FROM_GUID', max_length=32, blank=True, null=True)  # Field name made lowercase.
    export_at = models.DateTimeField(db_column='EXPORT_AT', blank=True, null=True)  # Field name made lowercase.
    export_by = models.CharField(db_column='EXPORT_BY', max_length=30, blank=True, null=True)  # Field name made lowercase.
    duedate = models.DateField(db_column='DueDate', blank=True, null=True)  # Field name made lowercase.
    deliverd_by = models.CharField(db_column='Deliverd_by', max_length=40, blank=True, null=True)  # Field name made lowercase.
    vehicle_no = models.CharField(db_column='Vehicle_no', max_length=30, blank=True, null=True)  # Field name made lowercase.
    doc_no = models.CharField(db_column='Doc_No', max_length=30, blank=True, null=True)  # Field name made lowercase.
    loc_group = models.CharField(max_length=20, blank=True, null=True)
    ibt = models.SmallIntegerField(blank=True, null=True)
    gst_tax_sum = models.FloatField(blank=True, null=True)
    tax_code_purchase = models.CharField(max_length=10, blank=True, null=True)
    tax_code_sales = models.CharField(max_length=10, blank=True, null=True)
    total_include_tax = models.FloatField(blank=True, null=True)
    tax_inclusive = models.SmallIntegerField(blank=True, null=True)
    doc_name_reg = models.CharField(max_length=80, blank=True, null=True)
    gst_tax_rate = models.FloatField(blank=True, null=True)
    multi_tax_code = models.SmallIntegerField(blank=True, null=True)
    refno2 = models.CharField(max_length=20, blank=True, null=True)
    surchg_tax_sum = models.FloatField(blank=True, null=True)
    gst_adj = models.FloatField(blank=True, null=True)
    ibt_gst = models.SmallIntegerField(blank=True, null=True)
    unpostby = models.CharField(max_length=80, blank=True, null=True)
    unpostdatetime = models.DateTimeField(blank=True, null=True)
    revision = models.IntegerField(blank=True, null=True)
    member_accno = models.CharField(max_length=20, blank=True, null=True)
    updatememberspoint = models.SmallIntegerField(db_column='UpdateMembersPoint', blank=True, null=True)  # Field name made lowercase.
    pointssum = models.FloatField(db_column='PointsSum', blank=True, null=True)  # Field name made lowercase.
    rounding_adj = models.FloatField(blank=True, null=True)
    roundadjneed = models.SmallIntegerField(db_column='RoundAdjNeed', blank=True, null=True)  # Field name made lowercase.
    ibt_complete = models.SmallIntegerField(blank=True, null=True)
    ibt_rec_amt = models.FloatField(blank=True, null=True)
    cardtype = models.CharField(max_length=10, blank=True, null=True)
    totaltax = models.FloatField(db_column='TotalTax', blank=True, null=True)  # Field name made lowercase.
    doc_status = models.CharField(max_length=20, blank=True, null=True)
    doc_type = models.CharField(max_length=20, blank=True, null=True)
    billto_name = models.CharField(max_length=60, blank=True, null=True)
    billto_reg_no = models.CharField(max_length=30, blank=True, null=True)
    billto_gst = models.CharField(max_length=30, blank=True, null=True)
    credit_available = models.FloatField(blank=True, null=True)
    tran_volume = models.FloatField(blank=True, null=True)
    tran_weight = models.FloatField(blank=True, null=True)
    doutlet_code = models.CharField(db_column='DOutlet_code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    add4 = models.CharField(db_column='Add4', max_length=60, blank=True, null=True)  # Field name made lowercase.
    dadd4 = models.CharField(db_column='DAdd4', max_length=60, blank=True, null=True)  # Field name made lowercase.
    si_paid = models.SmallIntegerField(blank=True, null=True)
    si_point_multiply = models.FloatField(blank=True, null=True)
    uploaded = models.IntegerField(blank=True, null=True)
    uploaded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'simain'


class SoPayment(models.Model):
    refno = models.CharField(db_column='RefNo', primary_key=True, max_length=20)  # Field name made lowercase.
    line = models.FloatField(db_column='Line')  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=10, blank=True, null=True)  # Field name made lowercase.
    bizdate = models.DateField(db_column='BizDate', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=20, blank=True, null=True)
    paytype = models.CharField(db_column='PayType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    paydescription = models.CharField(db_column='PayDescription', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cardtype = models.CharField(db_column='CardType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cardno = models.CharField(db_column='Cardno', max_length=30, blank=True, null=True)  # Field name made lowercase.
    carddate = models.DateField(db_column='CardDate', blank=True, null=True)  # Field name made lowercase.
    cardapproval = models.CharField(db_column='CardApproval', max_length=50, blank=True, null=True)  # Field name made lowercase.
    voucherno = models.CharField(db_column='VoucherNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    payamt = models.FloatField(db_column='PayAmt', blank=True, null=True)  # Field name made lowercase.
    appliedamt = models.FloatField(db_column='AppliedAmt', blank=True, null=True)  # Field name made lowercase.
    value_factor = models.FloatField(db_column='Value_Factor', blank=True, null=True)  # Field name made lowercase.
    retention_amt = models.FloatField(db_column='Retention_amt', blank=True, null=True)  # Field name made lowercase.
    hq_update = models.SmallIntegerField(blank=True, null=True)
    loc_group = models.CharField(max_length=20, blank=True, null=True)
    currencycode = models.CharField(db_column='CurrencyCode', max_length=6, blank=True, null=True)  # Field name made lowercase.
    exchangevalue = models.FloatField(db_column='ExchangeValue', blank=True, null=True)  # Field name made lowercase.
    exchangerate = models.FloatField(db_column='ExchangeRate', blank=True, null=True)  # Field name made lowercase.
    merchant_no = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'so_payment'
        unique_together = (('refno', 'line'),)


class Soamendchild(models.Model):
    refno = models.CharField(db_column='RefNo', primary_key=True, max_length=15)  # Field name made lowercase.
    line = models.IntegerField(db_column='Line')  # Field name made lowercase.
    entrytype = models.CharField(db_column='EntryType', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pricetype = models.CharField(db_column='PriceType', max_length=5, blank=True, null=True)  # Field name made lowercase.
    barcode = models.CharField(db_column='Barcode', max_length=30, blank=True, null=True)  # Field name made lowercase.
    itemcode = models.CharField(db_column='Itemcode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50, blank=True, null=True)  # Field name made lowercase.
    qty = models.FloatField(db_column='Qty', blank=True, null=True)  # Field name made lowercase.
    um = models.CharField(db_column='UM', max_length=5, blank=True, null=True)  # Field name made lowercase.
    unitprice = models.FloatField(db_column='UnitPrice', blank=True, null=True)  # Field name made lowercase.
    totalprice = models.FloatField(db_column='TotalPrice', blank=True, null=True)  # Field name made lowercase.
    packsize = models.FloatField(db_column='PackSize', blank=True, null=True)  # Field name made lowercase.
    colour = models.CharField(db_column='Colour', max_length=20, blank=True, null=True)  # Field name made lowercase.
    size = models.CharField(db_column='Size', max_length=20, blank=True, null=True)  # Field name made lowercase.
    brand = models.CharField(db_column='Brand', max_length=5, blank=True, null=True)  # Field name made lowercase.
    articleno = models.CharField(db_column='ArticleNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    soline = models.IntegerField(db_column='SOLine', blank=True, null=True)  # Field name made lowercase.
    sorefno = models.CharField(db_column='SORefno', max_length=15, blank=True, null=True)  # Field name made lowercase.
    amendqty = models.FloatField(db_column='AmendQty', blank=True, null=True)  # Field name made lowercase.
    dept = models.CharField(db_column='Dept', max_length=5, blank=True, null=True)  # Field name made lowercase.
    subdept = models.CharField(db_column='SubDept', max_length=5, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'soamendchild'
        unique_together = (('refno', 'line'),)


class Soamendmain(models.Model):
    refno = models.CharField(db_column='RefNo', primary_key=True, max_length=15)  # Field name made lowercase.
    amenddate = models.DateField(db_column='AmendDate', blank=True, null=True)  # Field name made lowercase.
    amendreason = models.TextField(db_column='AmendReason', blank=True, null=True)  # Field name made lowercase.
    issuestamp = models.DateTimeField(db_column='IssueStamp', blank=True, null=True)  # Field name made lowercase.
    laststamp = models.DateTimeField(db_column='LastStamp', blank=True, null=True)  # Field name made lowercase.
    sorefno = models.CharField(db_column='SORefno', max_length=15, blank=True, null=True)  # Field name made lowercase.
    sodate = models.DateField(db_column='SODate', blank=True, null=True)  # Field name made lowercase.
    issuedby = models.CharField(db_column='IssuedBy', max_length=80, blank=True, null=True)  # Field name made lowercase.
    subdeptcode = models.CharField(db_column='SubdeptCode', max_length=30, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=10, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=15, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=60, blank=True, null=True)  # Field name made lowercase.
    rejected = models.SmallIntegerField(db_column='Rejected', blank=True, null=True)  # Field name made lowercase.
    postby = models.CharField(max_length=80, blank=True, null=True)
    postdatetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'soamendmain'


class Sochild(models.Model):
    refno = models.CharField(db_column='RefNo', primary_key=True, max_length=15)  # Field name made lowercase.
    line = models.IntegerField(db_column='Line')  # Field name made lowercase.
    entrytype = models.CharField(db_column='EntryType', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pricetype = models.CharField(db_column='PriceType', max_length=5, blank=True, null=True)  # Field name made lowercase.
    barcode = models.CharField(db_column='Barcode', max_length=30, blank=True, null=True)  # Field name made lowercase.
    itemcode = models.CharField(db_column='Itemcode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50, blank=True, null=True)  # Field name made lowercase.
    qty = models.FloatField(db_column='Qty', blank=True, null=True)  # Field name made lowercase.
    um = models.CharField(db_column='UM', max_length=5, blank=True, null=True)  # Field name made lowercase.
    unitprice = models.FloatField(db_column='UnitPrice', blank=True, null=True)  # Field name made lowercase.
    disc1type = models.CharField(db_column='Disc1Type', max_length=1, blank=True, null=True)  # Field name made lowercase.
    disc1value = models.FloatField(db_column='Disc1Value', blank=True, null=True)  # Field name made lowercase.
    disc2type = models.CharField(db_column='Disc2Type', max_length=1, blank=True, null=True)  # Field name made lowercase.
    disc2value = models.FloatField(db_column='Disc2Value', blank=True, null=True)  # Field name made lowercase.
    netunitprice = models.FloatField(db_column='NetUnitPrice', blank=True, null=True)  # Field name made lowercase.
    discamt = models.FloatField(db_column='DiscAmt', blank=True, null=True)  # Field name made lowercase.
    totalprice = models.FloatField(db_column='TotalPrice', blank=True, null=True)  # Field name made lowercase.
    packsize = models.FloatField(db_column='PackSize', blank=True, null=True)  # Field name made lowercase.
    colour = models.CharField(db_column='Colour', max_length=20, blank=True, null=True)  # Field name made lowercase.
    size = models.CharField(db_column='Size', max_length=20, blank=True, null=True)  # Field name made lowercase.
    brand = models.CharField(db_column='Brand', max_length=5, blank=True, null=True)  # Field name made lowercase.
    articleno = models.CharField(db_column='ArticleNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tempdeliverqty = models.FloatField(db_column='TempDeliverQty', blank=True, null=True)  # Field name made lowercase.
    deliverqty = models.FloatField(db_column='DeliverQty', blank=True, null=True)  # Field name made lowercase.
    balanceqty = models.FloatField(db_column='BalanceQty', blank=True, null=True)  # Field name made lowercase.
    tempitem = models.SmallIntegerField(db_column='TempItem', blank=True, null=True)  # Field name made lowercase.
    tempitemchanged = models.SmallIntegerField(db_column='TempItemChanged', blank=True, null=True)  # Field name made lowercase.
    discvalue = models.FloatField(db_column='DiscValue', blank=True, null=True)  # Field name made lowercase.
    sysqoh = models.FloatField(db_column='SysQOH', blank=True, null=True)  # Field name made lowercase.
    sysavgcost = models.FloatField(db_column='SysAvgCost', blank=True, null=True)  # Field name made lowercase.
    groupno = models.IntegerField(db_column='GroupNo', blank=True, null=True)  # Field name made lowercase.
    groupno2 = models.IntegerField(db_column='GroupNo2', blank=True, null=True)  # Field name made lowercase.
    itemlink = models.CharField(db_column='ItemLink', max_length=20, blank=True, null=True)  # Field name made lowercase.
    amendment = models.IntegerField(db_column='Amendment', blank=True, null=True)  # Field name made lowercase.
    amendqty = models.FloatField(db_column='AmendQty', blank=True, null=True)  # Field name made lowercase.
    bulkqty = models.FloatField(db_column='BulkQty', blank=True, null=True)  # Field name made lowercase.
    umbulk = models.CharField(db_column='UMBulk', max_length=5, blank=True, null=True)  # Field name made lowercase.
    bqty = models.FloatField(db_column='BQty', blank=True, null=True)  # Field name made lowercase.
    pqty = models.FloatField(db_column='PQty', blank=True, null=True)  # Field name made lowercase.
    itemremark = models.TextField(db_column='ItemRemark', blank=True, null=True)  # Field name made lowercase.
    dept = models.CharField(db_column='Dept', max_length=5, blank=True, null=True)  # Field name made lowercase.
    subdept = models.CharField(db_column='SubDept', max_length=5, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=5, blank=True, null=True)  # Field name made lowercase.
    onhandqty = models.FloatField(db_column='OnHandQty', blank=True, null=True)  # Field name made lowercase.
    avgpesalesqty = models.FloatField(db_column='AvgPESalesQty', blank=True, null=True)  # Field name made lowercase.
    lastpesalesqty = models.FloatField(db_column='LastPESalesQty', blank=True, null=True)  # Field name made lowercase.
    sellingprice = models.FloatField(db_column='SellingPrice', blank=True, null=True)  # Field name made lowercase.
    mrank = models.CharField(max_length=1, blank=True, null=True)
    cartonprice = models.FloatField(blank=True, null=True)
    reqdate = models.DateField(blank=True, null=True)
    hq_update = models.SmallIntegerField(blank=True, null=True)
    purtolerance_std_plus = models.FloatField(db_column='PurTolerance_Std_plus', blank=True, null=True)  # Field name made lowercase.
    purtolerance_std_minus = models.FloatField(db_column='PurTolerance_Std_Minus', blank=True, null=True)  # Field name made lowercase.
    weighttraceqty = models.SmallIntegerField(db_column='WeightTraceQty', blank=True, null=True)  # Field name made lowercase.
    weighttraceqtyuom = models.CharField(db_column='WeightTraceQtyUOM', max_length=6, blank=True, null=True)  # Field name made lowercase.
    weighttraceqtycount = models.FloatField(db_column='WeightTraceQtyCount', blank=True, null=True)  # Field name made lowercase.
    qty_mobile = models.FloatField(blank=True, null=True)
    gst_tax_type = models.CharField(max_length=5, blank=True, null=True)
    gst_tax_code = models.CharField(max_length=10, blank=True, null=True)
    gst_tax_rate = models.FloatField(blank=True, null=True)
    gst_tax_amount = models.FloatField(blank=True, null=True)
    price_include_tax = models.FloatField(blank=True, null=True)
    totalprice_include_tax = models.FloatField(db_column='TotalPrice_include_tax', blank=True, null=True)  # Field name made lowercase.
    postdatetime_c = models.DateTimeField(blank=True, null=True)
    surchg_value = models.FloatField(blank=True, null=True)
    unitactprice = models.FloatField(blank=True, null=True)
    consign = models.SmallIntegerField(blank=True, null=True)
    surchg_disc_gst = models.FloatField(blank=True, null=True)
    itemtype = models.CharField(max_length=40, blank=True, null=True)
    costmarginvalue = models.FloatField(blank=True, null=True)
    costmargin = models.SmallIntegerField(blank=True, null=True)
    soldbyweight = models.SmallIntegerField(blank=True, null=True)
    cross_link_refno = models.CharField(max_length=32, blank=True, null=True)
    points = models.FloatField(db_column='Points', blank=True, null=True)  # Field name made lowercase.
    gst_manual = models.SmallIntegerField(blank=True, null=True)
    taxintno = models.IntegerField(db_column='TaxIntNo', blank=True, null=True)  # Field name made lowercase.
    taxcodemap = models.CharField(db_column='TaxCodeMap', max_length=15, blank=True, null=True)  # Field name made lowercase.
    taxvalue = models.FloatField(db_column='TaxValue', blank=True, null=True)  # Field name made lowercase.
    taxamount = models.FloatField(db_column='TaxAmount', blank=True, null=True)  # Field name made lowercase.
    taxamountvariance = models.FloatField(db_column='TaxAmountVariance', blank=True, null=True)  # Field name made lowercase.
    item_volume = models.FloatField(blank=True, null=True)
    item_weight = models.FloatField(blank=True, null=True)
    ignore_price_rules = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sochild'
        unique_together = (('refno', 'line'),)


class Somain(models.Model):
    refno = models.CharField(db_column='RefNo', primary_key=True, max_length=15)  # Field name made lowercase.
    docno = models.CharField(db_column='DocNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ordereddate = models.DateField(db_column='OrderedDate', blank=True, null=True)  # Field name made lowercase.
    reqdate = models.DateField(db_column='ReqDate', blank=True, null=True)  # Field name made lowercase.
    issuestamp = models.DateTimeField(db_column='IssueStamp', blank=True, null=True)  # Field name made lowercase.
    issuedby = models.CharField(db_column='IssuedBy', max_length=80, blank=True, null=True)  # Field name made lowercase.
    laststamp = models.DateTimeField(db_column='LastStamp', blank=True, null=True)  # Field name made lowercase.
    approvedby = models.CharField(db_column='ApprovedBy', max_length=60, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=15, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=60, blank=True, null=True)  # Field name made lowercase.
    add1 = models.CharField(db_column='Add1', max_length=60, blank=True, null=True)  # Field name made lowercase.
    add2 = models.CharField(db_column='Add2', max_length=60, blank=True, null=True)  # Field name made lowercase.
    add3 = models.CharField(db_column='Add3', max_length=60, blank=True, null=True)  # Field name made lowercase.
    attn = models.CharField(db_column='Attn', max_length=60, blank=True, null=True)  # Field name made lowercase.
    term = models.CharField(max_length=20, blank=True, null=True)
    tel = models.CharField(db_column='Tel', max_length=20, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='Fax', max_length=20, blank=True, null=True)  # Field name made lowercase.
    dadd1 = models.CharField(db_column='DAdd1', max_length=60, blank=True, null=True)  # Field name made lowercase.
    dadd2 = models.CharField(db_column='DAdd2', max_length=60, blank=True, null=True)  # Field name made lowercase.
    dadd3 = models.CharField(db_column='DAdd3', max_length=60, blank=True, null=True)  # Field name made lowercase.
    dattn = models.CharField(db_column='DAttn', max_length=60, blank=True, null=True)  # Field name made lowercase.
    dtel = models.CharField(db_column='DTel', max_length=20, blank=True, null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remark = models.TextField(db_column='Remark', blank=True, null=True)  # Field name made lowercase.
    subtotal1 = models.FloatField(db_column='SubTotal1', blank=True, null=True)  # Field name made lowercase.
    discount1 = models.FloatField(db_column='Discount1', blank=True, null=True)  # Field name made lowercase.
    discount1type = models.CharField(db_column='Discount1Type', max_length=1, blank=True, null=True)  # Field name made lowercase.
    subtotal2 = models.FloatField(db_column='SubTotal2', blank=True, null=True)  # Field name made lowercase.
    discount2 = models.FloatField(db_column='Discount2', blank=True, null=True)  # Field name made lowercase.
    discount2type = models.CharField(db_column='Discount2Type', max_length=1, blank=True, null=True)  # Field name made lowercase.
    total = models.FloatField(db_column='Total', blank=True, null=True)  # Field name made lowercase.
    billstatus = models.SmallIntegerField(db_column='BillStatus', blank=True, null=True)  # Field name made lowercase.
    amendment = models.SmallIntegerField(db_column='Amendment', blank=True, null=True)  # Field name made lowercase.
    completed = models.IntegerField(blank=True, null=True)
    disc1percent = models.FloatField(db_column='Disc1Percent', blank=True, null=True)  # Field name made lowercase.
    disc2percent = models.FloatField(db_column='Disc2Percent', blank=True, null=True)  # Field name made lowercase.
    subdeptcode = models.CharField(db_column='SubDeptCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    postby = models.CharField(max_length=80, blank=True, null=True)
    postdatetime = models.DateTimeField(blank=True, null=True)
    salesman = models.CharField(db_column='SALESMAN', max_length=30, blank=True, null=True)  # Field name made lowercase.
    hq_update = models.SmallIntegerField(blank=True, null=True)
    cross_ref = models.CharField(max_length=32, blank=True, null=True)
    cross_ref_module = models.CharField(max_length=32, blank=True, null=True)
    gst_tax_sum = models.FloatField(blank=True, null=True)
    tax_code_purchase = models.CharField(max_length=10, blank=True, null=True)
    total_include_tax = models.FloatField(blank=True, null=True)
    tax_inclusive = models.SmallIntegerField(blank=True, null=True)
    doc_name_reg = models.CharField(max_length=80, blank=True, null=True)
    gst_tax_rate = models.FloatField(blank=True, null=True)
    ibt = models.SmallIntegerField(blank=True, null=True)
    loc_group = models.CharField(max_length=20, blank=True, null=True)
    multi_tax_code = models.SmallIntegerField(blank=True, null=True)
    surchg_tax_sum = models.FloatField(blank=True, null=True)
    gst_adj = models.FloatField(blank=True, null=True)
    unpostby = models.CharField(max_length=80, blank=True, null=True)
    unpostdatetime = models.DateTimeField(blank=True, null=True)
    ibt_gst = models.SmallIntegerField(blank=True, null=True)
    revision = models.IntegerField(blank=True, null=True)
    member_accno = models.CharField(max_length=20, blank=True, null=True)
    updatememberspoint = models.SmallIntegerField(db_column='UpdateMembersPoint', blank=True, null=True)  # Field name made lowercase.
    pointssum = models.FloatField(db_column='PointsSum', blank=True, null=True)  # Field name made lowercase.
    rounding_adj = models.FloatField(blank=True, null=True)
    roundadjneed = models.SmallIntegerField(db_column='RoundAdjNeed', blank=True, null=True)  # Field name made lowercase.
    totaltax = models.FloatField(db_column='TotalTax', blank=True, null=True)  # Field name made lowercase.
    so_cancel = models.SmallIntegerField(blank=True, null=True)
    so_cancel_at = models.DateTimeField(blank=True, null=True)
    so_cancel_by = models.CharField(max_length=20, blank=True, null=True)
    so_cancel_reason = models.CharField(max_length=32, blank=True, null=True)
    so_expiry_date = models.DateField(blank=True, null=True)
    doc_status = models.CharField(max_length=20, blank=True, null=True)
    doc_type = models.CharField(max_length=20, blank=True, null=True)
    billto_name = models.CharField(max_length=60, blank=True, null=True)
    pos_sales = models.SmallIntegerField(blank=True, null=True)
    billto_reg_no = models.CharField(max_length=30, blank=True, null=True)
    billto_gst = models.CharField(max_length=30, blank=True, null=True)
    tran_volume = models.FloatField(blank=True, null=True)
    tran_weight = models.FloatField(blank=True, null=True)
    doutlet_code = models.CharField(db_column='DOutlet_code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    add4 = models.CharField(db_column='Add4', max_length=60, blank=True, null=True)  # Field name made lowercase.
    dadd4 = models.CharField(db_column='DAdd4', max_length=60, blank=True, null=True)  # Field name made lowercase.
    so_paid = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'somain'


class Subdept(models.Model):
    mcode = models.ForeignKey(Department, models.DO_NOTHING, db_column='MCode')  # Field name made lowercase.
    code = models.CharField(db_column='Code', primary_key=True, max_length=6)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=40)  # Field name made lowercase.
    running = models.IntegerField(db_column='Running')  # Field name made lowercase.
    memberpoints = models.DecimalField(db_column='MemberPoints', max_digits=5, decimal_places=2)  # Field name made lowercase.
    margin_min = models.DecimalField(max_digits=5, decimal_places=2)
    margin_max = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(db_column='CREATED_AT')  # Field name made lowercase.
    created_by = models.CharField(db_column='CREATED_BY', max_length=30)  # Field name made lowercase.
    updated_at = models.DateTimeField(db_column='UPDATED_AT')  # Field name made lowercase.
    updated_by = models.CharField(db_column='UPDATED_BY', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'subdept'


class Supcus(models.Model):
    type = models.CharField(db_column='Type', max_length=1)  # Field name made lowercase.
    code = models.CharField(db_column='Code', primary_key=True, max_length=15)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=60)  # Field name made lowercase.
    add1 = models.CharField(db_column='Add1', max_length=60)  # Field name made lowercase.
    add2 = models.CharField(db_column='Add2', max_length=60)  # Field name made lowercase.
    add3 = models.CharField(db_column='Add3', max_length=60)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=20)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=20)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=25)  # Field name made lowercase.
    postcode = models.CharField(db_column='Postcode', max_length=6)  # Field name made lowercase.
    tel = models.CharField(db_column='Tel', max_length=20)  # Field name made lowercase.
    fax = models.CharField(db_column='Fax', max_length=20)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=60)  # Field name made lowercase.
    mobile = models.CharField(db_column='Mobile', max_length=12)  # Field name made lowercase.
    term = models.CharField(db_column='Term', max_length=30)  # Field name made lowercase.
    paymentday = models.IntegerField(db_column='PaymentDay')  # Field name made lowercase.
    bankacc = models.CharField(db_column='BankAcc', max_length=35)  # Field name made lowercase.
    creditlimit = models.DecimalField(db_column='CreditLimit', max_digits=10, decimal_places=2)  # Field name made lowercase.
    monitorcredit = models.SmallIntegerField(db_column='MonitorCredit')  # Field name made lowercase.
    remark = models.TextField(db_column='Remark', blank=True, null=True)  # Field name made lowercase.
    pointbf = models.DecimalField(db_column='PointBF', max_digits=10, decimal_places=2)  # Field name made lowercase.
    pointcumm = models.DecimalField(db_column='PointCumm', max_digits=10, decimal_places=2)  # Field name made lowercase.
    pointsum = models.DecimalField(db_column='PointSum', max_digits=10, decimal_places=2)  # Field name made lowercase.
    member = models.SmallIntegerField(db_column='Member')  # Field name made lowercase.
    memberno = models.CharField(max_length=20)
    expirydate = models.DateField(db_column='ExpiryDate')  # Field name made lowercase.
    cyclevisit = models.IntegerField(db_column='CycleVisit')  # Field name made lowercase.
    deliveryterm = models.IntegerField()
    issuedstamp = models.DateTimeField(db_column='IssuedStamp')  # Field name made lowercase.
    laststamp = models.DateTimeField(db_column='LastStamp')  # Field name made lowercase.
    dadd1 = models.CharField(max_length=60)
    dadd2 = models.CharField(max_length=60)
    dadd3 = models.CharField(max_length=60)
    dattn = models.CharField(max_length=60)
    dtel = models.CharField(max_length=20)
    dfax = models.CharField(max_length=20)
    email = models.CharField(max_length=60)
    accountcode = models.CharField(db_column='AccountCode', max_length=15)  # Field name made lowercase.
    accpdebit = models.CharField(db_column='AccPDebit', max_length=10)  # Field name made lowercase.
    accpcredit = models.CharField(db_column='AccPCredit', max_length=10)  # Field name made lowercase.
    calduedateby = models.CharField(db_column='CalDueDateby', max_length=30)  # Field name made lowercase.
    supcusgroup = models.CharField(db_column='supcusGroup', max_length=20)  # Field name made lowercase.
    region = models.CharField(max_length=10)
    pcode = models.CharField(max_length=10)
    add4 = models.CharField(db_column='Add4', max_length=60)  # Field name made lowercase.
    contact2 = models.CharField(db_column='Contact2', max_length=60)  # Field name made lowercase.
    dadd4 = models.CharField(db_column='DAdd4', max_length=60)  # Field name made lowercase.
    poprice_method = models.CharField(max_length=7)
    stockday_min = models.IntegerField()
    stockday_max = models.IntegerField()
    stock_returnable = models.IntegerField()
    stock_return_cost_type = models.CharField(max_length=10)
    autoclosepo = models.IntegerField(db_column='AutoClosePO')  # Field name made lowercase.
    consign = models.IntegerField(db_column='Consign')  # Field name made lowercase.
    block = models.IntegerField(db_column='Block')  # Field name made lowercase.
    exclude_orderqty_control = models.IntegerField()
    supcus_guid = models.CharField(unique=True, max_length=32)
    acc_no = models.CharField(max_length=20)
    ord_w1 = models.IntegerField(db_column='Ord_W1')  # Field name made lowercase.
    ord_w2 = models.IntegerField(db_column='Ord_W2')  # Field name made lowercase.
    ord_w3 = models.IntegerField(db_column='Ord_W3')  # Field name made lowercase.
    ord_w4 = models.IntegerField(db_column='Ord_W4')  # Field name made lowercase.
    ord_d1 = models.IntegerField(db_column='Ord_D1')  # Field name made lowercase.
    ord_d2 = models.IntegerField(db_column='Ord_D2')  # Field name made lowercase.
    ord_d3 = models.IntegerField(db_column='Ord_D3')  # Field name made lowercase.
    ord_d4 = models.IntegerField(db_column='Ord_D4')  # Field name made lowercase.
    ord_d5 = models.IntegerField(db_column='Ord_D5')  # Field name made lowercase.
    ord_d6 = models.IntegerField(db_column='Ord_D6')  # Field name made lowercase.
    ord_d7 = models.IntegerField(db_column='Ord_D7')  # Field name made lowercase.
    rec_method_1 = models.IntegerField(db_column='Rec_Method_1')  # Field name made lowercase.
    rec_method_2 = models.IntegerField(db_column='Rec_Method_2')  # Field name made lowercase.
    rec_method_3 = models.IntegerField(db_column='Rec_Method_3')  # Field name made lowercase.
    rec_method_4 = models.IntegerField(db_column='Rec_Method_4')  # Field name made lowercase.
    rec_method_5 = models.IntegerField(db_column='Rec_Method_5')  # Field name made lowercase.
    pur_expiry_days = models.IntegerField()
    grn_baseon_pocost = models.IntegerField()
    ord_set_global = models.IntegerField(db_column='Ord_set_global')  # Field name made lowercase.
    rules_code = models.CharField(max_length=20)
    po_negative_qty = models.IntegerField()
    grpo_variance_qty = models.DecimalField(max_digits=10, decimal_places=2)
    grpo_variance_price = models.DecimalField(max_digits=10, decimal_places=2)
    price_include_tax = models.IntegerField()
    delivery_early_in_day = models.PositiveIntegerField()
    delivery_late_in_day = models.PositiveIntegerField()
    tax_code = models.CharField(max_length=10)
    gst_start_date = models.DateField()
    gst_no = models.CharField(max_length=15)
    reg_no = models.CharField(max_length=25)
    name_reg = models.CharField(max_length=80)
    multi_tax_rate = models.IntegerField()
    grn_allow_negative_margin = models.IntegerField()
    rebate_as_inv = models.IntegerField()
    discount_as_inv = models.IntegerField()
    poso_line_max = models.PositiveIntegerField()
    apply_actual_cn = models.IntegerField()
    purchasednamtastaxinv = models.IntegerField(db_column='PurchaseDNAmtAsTaxInv')  # Field name made lowercase.
    member_accno = models.CharField(max_length=20)
    promorebateastaxinv = models.IntegerField(db_column='PromoRebateAsTaxInv')  # Field name made lowercase.
    roundingadjust = models.IntegerField(db_column='RoundingAdjust')  # Field name made lowercase.
    mobile_po = models.IntegerField()
    auto_grn_mobile_po = models.IntegerField()
    min_expiry_day = models.IntegerField()
    currency_code = models.CharField(max_length=5)
    sstdefaultcode = models.CharField(db_column='SSTDefaultCode', max_length=15)  # Field name made lowercase.
    sstdefaulttaxintno = models.IntegerField(db_column='SSTDefaultTaxIntNo')  # Field name made lowercase.
    ssteffectivedate = models.DateField(db_column='SSTEffectiveDate')  # Field name made lowercase.
    sstregno = models.CharField(db_column='SSTRegNo', max_length=20)  # Field name made lowercase.
    replenish_date = models.CharField(max_length=12)
    replenish_stockbalance = models.IntegerField()
    b2b_registration = models.IntegerField()
    cdi = models.IntegerField()
    cpm = models.IntegerField()
    auto_price_change = models.IntegerField()
    promo_date = models.IntegerField()
    pos_sales = models.IntegerField()
    sales_agent = models.CharField(max_length=30)
    stk_rtn_collect_day = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'supcus'
        unique_together = (('code', 'supcus_guid'),)


class SupcusBranch(models.Model):
    branch_guid = models.CharField(unique=True, max_length=32)
    supcus_guid = models.OneToOneField(Supcus, models.DO_NOTHING, db_column='supcus_guid', primary_key=True)
    loc_group = models.CharField(max_length=10)
    set_active = models.IntegerField()
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=15)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=15)
    is_ibt = models.IntegerField()
    limit_control_amt = models.DecimalField(max_digits=10, decimal_places=4)
    debit_acc_code = models.CharField(max_length=15)
    credit_acc_code = models.CharField(max_length=15)
    isict = models.IntegerField(db_column='isICT')  # Field name made lowercase.
    acc_code = models.CharField(max_length=15)
    is_gst = models.IntegerField()
    supbulkqty = models.DecimalField(db_column='SupBulkQty', max_digits=5, decimal_places=2)  # Field name made lowercase.
    outlet_ord_d1 = models.IntegerField(db_column='Outlet_Ord_D1')  # Field name made lowercase.
    outlet_ord_d2 = models.IntegerField(db_column='Outlet_Ord_D2')  # Field name made lowercase.
    outlet_ord_d3 = models.PositiveIntegerField(db_column='Outlet_Ord_D3')  # Field name made lowercase.
    outlet_ord_d4 = models.IntegerField(db_column='Outlet_Ord_D4')  # Field name made lowercase.
    outlet_ord_d5 = models.IntegerField(db_column='Outlet_Ord_D5')  # Field name made lowercase.
    outlet_ord_d6 = models.IntegerField(db_column='Outlet_Ord_D6')  # Field name made lowercase.
    outlet_ord_d7 = models.IntegerField(db_column='Outlet_Ord_D7')  # Field name made lowercase.
    po_min_amt = models.DecimalField(db_column='PO_min_amt', max_digits=14, decimal_places=2)  # Field name made lowercase.
    block_po = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'supcus_branch'
        unique_together = (('supcus_guid', 'loc_group'),)


class SupcusLink(models.Model):
    link_guid = models.CharField(primary_key=True, max_length=32)
    supcus_guid = models.ForeignKey(Supcus, models.DO_NOTHING, db_column='supcus_guid')
    selected_guid = models.ForeignKey(Supcus, models.DO_NOTHING, db_column='selected_guid')
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=15)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'supcus_link'
        unique_together = (('supcus_guid', 'selected_guid'),)


class Sysuser(models.Model):
    name = models.CharField(primary_key=True, max_length=15)
    pwd = models.CharField(max_length=15)
    issuedstamp = models.DateTimeField(db_column='issuedStamp')  # Field name made lowercase.
    laststamp = models.DateTimeField(db_column='lastStamp')  # Field name made lowercase.
    querydept = models.TextField(db_column='QueryDept')  # Field name made lowercase.
    fullname = models.CharField(db_column='FullName', max_length=60)  # Field name made lowercase.
    subdeptcode = models.CharField(db_column='SubDeptCode', max_length=6)  # Field name made lowercase.
    membermodule = models.IntegerField(db_column='MemberModule')  # Field name made lowercase.
    itemmaster = models.IntegerField(db_column='ItemMaster')  # Field name made lowercase.
    reportmodule = models.IntegerField(db_column='ReportModule')  # Field name made lowercase.
    freegiftmodule = models.IntegerField(db_column='FreeGiftModule')  # Field name made lowercase.
    pocketpcmodule = models.IntegerField(db_column='PocketPCModule')  # Field name made lowercase.
    groupcode = models.CharField(max_length=40)
    pwd_expirydate = models.DateField()
    sysuser_guid = models.CharField(max_length=32)
    loginlocked = models.SmallIntegerField(db_column='LoginLocked')  # Field name made lowercase.
    lastchangepassword = models.DateField(db_column='LastChangePassword')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sysuser'


class SysuserDept(models.Model):
    name = models.OneToOneField(Sysuser, models.DO_NOTHING, db_column='name', primary_key=True)
    deptcode = models.CharField(db_column='DeptCode', max_length=6)  # Field name made lowercase.
    deptdescription = models.CharField(db_column='DeptDescription', max_length=40)  # Field name made lowercase.
    active = models.IntegerField(db_column='Active')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sysuser_dept'
        unique_together = (('name', 'deptcode'),)


class SysuserLog(models.Model):
    log_guid = models.CharField(primary_key=True, max_length=32)
    name = models.ForeignKey(Sysuser, models.DO_NOTHING, db_column='name')
    log_type = models.CharField(max_length=50)
    log_count = models.IntegerField()
    from_value = models.CharField(max_length=50)
    to_value = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=15)
    log_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'sysuser_log'


class SysuserSubdept(models.Model):
    name = models.OneToOneField(Sysuser, models.DO_NOTHING, db_column='name', primary_key=True)
    deptcode = models.CharField(db_column='DeptCode', max_length=6)  # Field name made lowercase.
    deptdescription = models.CharField(db_column='DeptDescription', max_length=40)  # Field name made lowercase.
    subdeptcode = models.ForeignKey(Subdept, models.DO_NOTHING, db_column='SubdeptCode')  # Field name made lowercase.
    subdeptdescription = models.CharField(db_column='SubDeptDescription', max_length=40)  # Field name made lowercase.
    active = models.IntegerField(db_column='Active')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sysuser_subdept'
        unique_together = (('name', 'subdeptcode'),)
