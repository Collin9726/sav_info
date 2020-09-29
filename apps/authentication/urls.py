from django.urls import path, include
from .views import RegistrationAPIView,LoginAPIView

urlpatterns = [

  path('signup/', RegistrationAPIView.as_view(), name='signup'),
  path('login/', LoginAPIView.as_view(), name='login'),
]