import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from account.models import User
from account.services.google import GoogleLoginService
from account.services.linkedin import LinkedinLoginService

logger = logging.getLogger()


def social_login_callback(request, backend):
    if 'error' in request.GET:
        messages.error(request, f'Error : {request.GET.get("error")}')
        return redirect('/')
    if backend in [LinkedinLoginService.KEY, GoogleLoginService.KEY]:
        service = None
        if backend == LinkedinLoginService.KEY:
            service = LinkedinLoginService(request=request,
                                           client_id=settings.LINKEDIN_CLIENT_ID,
                                           client_secret=settings.LINKEDIN_CLIENT_SECRET)

        if backend == GoogleLoginService.KEY:
            service = GoogleLoginService(request=request,
                                         client_id=settings.GOOGLE_OAUTH2_CLIENT_ID,
                                         client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
                                         client_project_id=settings.GOOGLE_OAUTH2_PROJECT_ID)

        service.process_response(request.get_full_path())

        user_info = service.get_user_info()
        try:
            user = User.objects.get(email=user_info.get('email'))
        except User.DoesNotExist:
            user = User.objects.create_user(email=user_info.get('email'),
                                            password=User.objects.make_random_password(8))
        login(request, user=user)

    return redirect('/')


def social_login(request, backend):
    if backend == GoogleLoginService.KEY:
        service = GoogleLoginService(request=request,
                                     client_id=settings.GOOGLE_OAUTH2_CLIENT_ID,
                                     client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
                                     client_project_id=settings.GOOGLE_OAUTH2_PROJECT_ID)
        authorization_url, state = service.get_authorization_url()
        return redirect(authorization_url)

    if backend == LinkedinLoginService.KEY:
        service = LinkedinLoginService(request=request,
                                       client_id=settings.LINKEDIN_CLIENT_ID,
                                       client_secret=settings.LINKEDIN_CLIENT_SECRET)
        authorization_url, state = service.get_authorization_url()
        return redirect(authorization_url)

    return redirect('/')
