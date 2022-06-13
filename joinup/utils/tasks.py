from config.celery import app
from .verifications import send_email_to_verify, send_sms_to_verify
from pathlib import Path

PATH_DIR = Path(__file__).resolve(strict=True).parent


@app.task(name='send_mail_task', autoretry_for=(Exception,), bind=True, retry_kwargs={'max_retries': 10, 'countdown': 5},)
def send_mail(self, email, username, host):
    send_sms_to_verify(email, username, host)
    send_email_to_verify(email, username, host)