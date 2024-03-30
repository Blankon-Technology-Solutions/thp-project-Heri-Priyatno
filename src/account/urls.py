from django.urls import path

from account.views import social_login, social_login_callback

urlpatterns = [
    path('oauth-login/<slug:backend>/', social_login, name='oauth-login'),
    path('oauth-login/<slug:backend>/callback/', social_login_callback, name='oauth-login-callback')
]
