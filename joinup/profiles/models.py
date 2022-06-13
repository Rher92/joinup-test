from ntpath import join
from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
from joinup.utils.models import TrackModel
from joinup.utils.verifications import send_email_to_verify, send_sms_to_verify



class Profile(TrackModel):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    hobbies = models.CharField(max_length=255, null=True, blank=True)
    
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Formato requerido: +999999999."
    )
    phone = models.PositiveBigIntegerField(validators=[phone_regex])
    
    phone_validated = models.BooleanField(default=False)
    email_validated = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'{self.user.username}'
    

@receiver(pre_save, sender=get_user_model())
def save_profile(sender, instance, **kwargs):
    instance.username = f'{instance.email}-{instance.pk}'
    

@receiver(pre_save, sender=Profile)
def verify_email_profile(sender, instance, **kwargs):
    if not instance.pk:
        send_email_to_verify(instance.user.email, instance.user.username, settings.HOST)
        send_sms_to_verify(instance.user.email, instance.user.username, settings.HOST)
    send_email_to_verify(instance.user.email, instance.user.username, settings.HOST)
    send_sms_to_verify(instance.user.email, instance.user.username, settings.HOST)
