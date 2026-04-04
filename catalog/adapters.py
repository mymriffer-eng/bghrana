"""
Custom adapters for django-allauth
"""
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter за автоматично свързване на социални акаунти
    """
    
    def pre_social_login(self, request, sociallogin):
        """
        Ако user е вече логнат, директно свързва social акаунта
        без да показва signup форма
        """
        # Ако user е authenticated и социален акаунт не е свързан
        if request.user.is_authenticated and not sociallogin.is_existing:
            # Свързваме социалния акаунт към текущия user
            sociallogin.connect(request, request.user)
            # Редирект обратно към connections страницата
            raise ImmediateHttpResponse(redirect('/accounts/social/connections/'))
