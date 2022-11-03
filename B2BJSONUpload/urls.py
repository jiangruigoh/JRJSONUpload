"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from main import views
# from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    # path('api/token/',
    #      jwt_views.TokenObtainPairView.as_view(),
    #      name ='token_obtain_pair'),
    # path('api/token/refresh/',
    #      jwt_views.TokenRefreshView.as_view(),
    #      name ='token_refresh'),
    # path('admin/', admin.site.urls),

    # path('mc_allcode/', include('_mc_allcode.urls')),
    # path('mc_category/', include('_mc_category.urls')),
    # path('mc_companyprofile/', include('_mc_companyprofile.urls')),
    # path('mc_department/', include('_mc_department.urls')),
    # path('mc_set_group/', include('_mc_set_group.urls')),
    # path('mc_set_group_dept/', include('_mc_set_group_dept.urls')),
    # path('mc_subdept/', include('_mc_subdept.urls')),
    # path('ml_itembarcode/', include('_ml_itembarcode.urls')),
    # path('ml_itemmaster/', include('_ml_itemmaster.urls')),
    # path('ml_itemmaster_block_by_branch/',
    #      include('_ml_itemmaster_block_by_branch.urls')),
    # path('ml_itemmaster_branch_stock/',
    #      include('_ml_itemmaster_branch_stock.urls')),
    # path('ml_itemmaster_itemtype/', include('_ml_itemmaster_itemtype.urls')),
    # path('ml_itemmaster_listed_branch/',
    #      include('_ml_itemmaster_listed_branch.urls')),
    # path('ml_itemmaster_miscellaneous/',
    #      include('_ml_itemmaster_miscellaneous.urls')),
    # path('ml_itemmaster_othersinfo/', include('_ml_itemmaster_othersinfo.urls')),
    # path('ml_itemmaster_pricetype/', include('_ml_itemmaster_pricetype.urls')),
    # path('ml_itemmaster_replenishment/',
    #      include('_ml_itemmaster_replenishment.urls')),
    # path('ml_itemmastersupcode/', include('_ml_itemmastersupcode.urls')),
    # path('ml_location/', include('_ml_location.urls')),
    # path('ml_locationgroup/', include('_ml_locationgroup.urls')),
    # path('ml_supcus/', include('_ml_supcus.urls')),
    # path('ml_supcus_branch/', include('_ml_supcus_branch.urls')),
    # path('ml_sysuser/', include('_ml_sysuser.urls')),
    #    path('mc_department_v2/',include('_mc_department_v2.urls')),
    #    path('mc_subdept_v2/',include('_mc_subdept_v2.urls')),
    #    path('mc_category_v2/',include('_mc_category_v2.urls')),
    # path('ts_simain/', include('_ts_simain.urls')),
    # path('ts_sichild/', include('_ts_sichild.urls')),
    # path('ts_sipayment/', include('_ts_sipayment.urls')),


    # report PO Management
    path('report_PoManagementCopy/<search_refno>',
         views.report_PoManagementCopy, name='report_PoManagementCopy'),
    # report PO Supplier
    path('report_PoSupplierCopy/<search_refno>',
         views.report_PoSupplierCopy, name='report_PoSupplierCopy'),
    # report GRN Management
    path('report_GrManagementCopy/<search_refno>',
         views.report_GrManagementCopy, name='GrManagementCopy'),
    # report GRN supplier
    path('report_GrSupplierCopy/<search_refno>',
         views.report_GrSupplierCopy, name='report_GrSupplierCopy'),
    # report GRDA
    path('report_Grda/<search_refno>',
         views.report_Grda, name='report_Grda'),
    # report GRN supplier GQV
    path('report_GrSupplierGQV/<search_refno>',
         views.report_GrSupplierGQV, name='report_GrSupplierGQV'),
    # report PRDN
    path('report_PurchaseReturnDN/<search_refno>',
         views.report_PurchaseReturnDN, name='report_PurchaseReturnDN'),
    # report PRCN
    path('report_PurchaseReturnCN/<search_refno>',
         views.report_PurchaseReturnCN, name='report_PurchaseReturnCN'),
    # report PCI
    path('report_PromotionClaimInvoie/<search_refno>',
         views.report_PromotionClaimInvoie, name='report_PromotionClaimInvoie'),
    # report DI
    path('report_DisplayIncentive_TaxInvoice/<search_refno>',
         views.report_DisplayIncentive_TaxInvoice, name='report_DisplayIncentive_TaxInvoice'),
    # report SI Management
    path('report_SiManagementCopy/<search_refno>',
         views.report_SiManagementCopy, name='report_SiManagementCopy'),
    # report SI supplier
    path('report_SiSupplierCopy/<search_refno>',
         views.report_SiSupplierCopy, name='report_SiSupplierCopy'),
    #path('PurchaseReturnCN/<search_refno>', views.PurchaseReturnCN, name='PurchaseReturnCN'),
    #    path('PnLCategory/<DateFrom>/<DateTo>', views.PnLCategory, name='PnLCategory'),
    #path('PnLCategory/<date_from>/<date_to>', views.PnLCategory, name='PnLCategory'),
    # report PDN
    path('report_PurchaseDN/<search_refno>', views.report_PurchaseDN,
         name='report_PurchaseDN'),
    # report PCN
    path('report_PurchaseCN/<search_refno>', views.report_PurchaseCN,
         name='report_PurchaseCN'),

    # PO Json Info
    path('info_PoMain/<search_refno>', views.info_PoMain, name='info_PoMain'),
    # GRN Json Info
    path('info_GrMain/<search_refno>', views.info_GrMain, name='info_GrMain'),
    # GRDA Json Info
    path('info_GrMain_dncn/<search_refno>',
         views.info_GrMain_dncn, name='info_GrMain_dncn'),
    # PCI Json Info
    path('info__PromotionClaim/<search_refno>',
         views.info__PromotionClaim, name='info__PromotionClaim'),
    # PRDN Json Info
    path('info_PurchaseReturnDN/<search_refno>',
         views.info_PurchaseReturnDN, name='info_PurchaseReturnDN'),
    # PRCN Json Info
    path('info_PurchaseReturnCN/<search_refno>',
         views.info_PurchaseReturnCN, name='info_PurchaseReturnCN'),
    # DI Json Info
    path('info__DisplayIncentive/<search_refno>',
         views.info__DisplayIncentive, name='info__DisplayIncentive'),
    # SI Json Info
    path('info_SiMain/<search_refno>', views.info_SiMain, name='info_SiMain'),
    # PDNCN Json Info
    path('info_PurchaseDNCN/<search_refno>',
         views.info_PurchaseDNCN, name='info_PurchaseDNCN'),
]
