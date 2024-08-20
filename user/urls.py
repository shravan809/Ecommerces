from django.contrib import admin
from django.urls import path
from user.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',UserRegitration.as_view()),
    #path('verifyotp/',VerifiedAPI.as_view()),
    path('login/', VerifyAndLoginAPIView.as_view(), name='login'),
    path('update/', UserUpdateView.as_view(), name='user-update'),
]