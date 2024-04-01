from django.urls import path

from account.views.api import LoginApiView, RegisterApiView, logout_api

urlpatterns = [
    path('login/', LoginApiView.as_view(), name='login-api'),
    path('register/', RegisterApiView.as_view(), name='register-api'),
    path('logout/', logout_api, name='logout-api')
]
