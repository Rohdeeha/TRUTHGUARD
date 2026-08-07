from django.urls import path
from .views import EducationalHubView

urlpatterns = [
    path('education/', EducationalHubView.as_view(), name='education-hub'),
]