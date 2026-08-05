from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


admin.site.site_header = "TruthGuard Situation Room"
admin.site.site_title = "TruthGuard Admin Portal"
admin.site.index_title = "System Administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('incidents.urls')), 
    path('api/core/', include('core.urls')),
]