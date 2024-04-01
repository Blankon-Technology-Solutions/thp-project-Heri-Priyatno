from django.urls import path

from account.views.auth import login, register, logout_user
from account.views.social import social_login_callback, social_login

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout', logout_user, name='logout'),
    path('oauth-login/<slug:backend>/', social_login, name='oauth-login'),
    path('oauth-login/<slug:backend>/callback/', social_login_callback, name='oauth-login-callback')
]
