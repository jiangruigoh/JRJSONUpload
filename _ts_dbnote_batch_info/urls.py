from django.urls import include, path, include
from rest_framework import routers
from . import views
 
router = routers.DefaultRouter()
router.register(r'ts_DbnoteBatchInfo', views.DbnoteBatchInfoViewSet)
#router_parent = routers.SimpleRouter()
#router_parent.register(r'<Type>_DbnoteBatchInfo_parent', views.DbnoteBatchInfoViewSet_parent)
 
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
#    path('', include(router_parent.urls)),
 
#20220901 Beh - disable due to will create another admin login url based on table API
#    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')) 
]  
