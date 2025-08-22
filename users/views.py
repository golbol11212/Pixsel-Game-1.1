# users/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import UserRegisterForm, VerificationCodeForm
from django.contrib.auth import get_user_model
from django.contrib import messages

# Class-Based View для регистрации пользователя
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import PendingUser
import uuid
from django.utils import timezone
from .utils import generate_random_password, send_email_tls_with_password

class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:verification_code')

    def form_valid(self, form):
        # Не сохраняем пользователя сразу, а создаем PendingUser
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        raw_password = form.cleaned_data['password1']
        password_hash = make_password(raw_password)
        token = str(uuid.uuid4())
        temp_password = generate_random_password(6)

        # Генерируем 6-значный числовой код подтверждения
        token = ''.join([str(i) for i in generate_random_password(6)])

        # Создаем или обновляем PendingUser
        pending_user, created = PendingUser.objects.update_or_create(
            email=email,
            defaults={
                'username': username,
                'password_hash': password_hash,
                'email_confirmation_token': token,
                'generated_password': temp_password,
                'created_at': timezone.now(),
            }
        )

        # Отправляем письмо с кодом и временным паролем
        current_site = '127.0.0.1:8000'  # Замените на ваш домен в продакшене
        mail_subject = 'Подтвердите вашу регистрацию и получите временный пароль'
        context = {
            'user': pending_user,
            'domain': current_site,
            'token': token,
            'generated_password': temp_password,
        }
        to_email = email
        send_email_tls_with_password(
            sender_email='golbol112@gmail.com',
            sender_password='owyj vdld ipky epei',
            receiver_email=to_email,
            subject=mail_subject,
            body_template='users/account_activation_email.html',
            context=context
        )

        return redirect(self.success_url)

# View для ввода и проверки 6-значного кода подтверждения
class VerificationCodeView(View):
    form_class = VerificationCodeForm
    template_name = 'users/verification_code.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['verification_code'].strip()
            print(f"Verification code from form: '{code}'")  # debug
            try:
                pending_user = PendingUser.objects.get(email_confirmation_token=code)
                print(f"Found PendingUser with token: '{pending_user.email_confirmation_token}'")  # debug
                # Создаем пользователя из PendingUser
                User = get_user_model()
                user = User.objects.create(
                    username=pending_user.username,
                    email=pending_user.email,
                    password=pending_user.password_hash,
                    is_active=True,
                )
                # Удаляем PendingUser
                pending_user.delete()
                messages.success(request, 'Регистрация успешно завершена. Теперь вы можете войти.')
                return redirect('users:login')
            except PendingUser.DoesNotExist:
                messages.error(request, 'Неверный код подтверждения.')
        return render(request, self.template_name, {'form': form})

# Удаляем старое представление подтверждения email
# class ActivateAccount(View):
#     ...

# Новое представление для страницы успешной регистрации (сообщение о подтверждении)
class RegistrationSuccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/registration_success.html')
