# users/utils.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
from django.conf import settings # Для доступа к настройкам Django

def generate_random_password(length=6):
    """
    Генерирует случайный пароль из заданного количества цифр.
    """
    digits = string.digits
    return ''.join(random.choice(digits) for i in range(length))

def send_email_tls_with_password(sender_email, sender_password, receiver_email, subject, body_template, context):
    """
    Отправляет электронное письмо с использованием TLS, с возможностью включения сгенерированного пароля.
    Использует шаблоны Django для формирования тела письма.

    Args:
        sender_email (str): Адрес электронной почты отправителя.
        sender_password (str): Пароль или пароль приложения для электронной почты отправителя.
        receiver_email (str): Адрес электронной почты получателя.
        subject (str): Тема письма.
        body_template (str): Имя шаблона Django для тела письма.
        context (dict): Словарь контекста для рендеринга шаблона письма.
    """
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags

    smtp_server = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_PORT

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    html_message = render_to_string(body_template, context)
    plain_message = strip_tags(html_message)

    message.attach(MIMEText(plain_message, "plain"))
    message.attach(MIMEText(html_message, "html")) # Отправляем также HTML-версию

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        print("Письмо успешно отправлено!")
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")