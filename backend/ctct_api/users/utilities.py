# Utilities

# Importing necessary modules from Django core
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings


# Project imports
def send_activation_email_util(user, request):
    token = default_token_generator.make_token(user)
    #print(f"Generated activation token for user ID {user.pk}: {token}")
    current_site = get_current_site(request)
    mail_subject = 'Ative a sua conta da unidade curricular de CTCT.'
    message = render_to_string('account_activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [user.email])

    messages.success(request, 'Verifique o seu email para completar a ativação da sua conta.')

