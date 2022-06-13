from django.core.mail import send_mail
from django.urls import reverse



def send_email_to_verify(email, username, host):
    url = host + reverse('api:profiles-verify-email')  + f'?username={username}'
    send_mail(
        'verificar movil',
        f'mock verificar email - {url}', 
        'sender@example.com',
        [email]
    )

def send_sms_to_verify(email, username, host):
    url = host + reverse('api:profiles-verify-phone')  + f'?username={username}'
    send_mail(
        'verificar movil',
        f'mock de sms para verificar movil - {url}', 
        'sender@example.com',
        [email]
    )