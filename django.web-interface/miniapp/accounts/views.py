from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render  # ВАЖНО: render должен быть импортирован!
from django.views.decorators.csrf import csrf_exempt
from .models import Registration  # добавим импорт

@csrf_exempt  # Убрать в продакшене!
def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Сохраняем данные в базу
        Registration.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            message=message,
        )

        # Письмо остаётся как есть
        full_message = (
            f"Здравствуйте, {first_name} {last_name}!\n\n"
            f"Мы получили ваши данные:\n"
            f"Email: {email}\n"
            f"Телефон: {phone}\n"
            f"Сообщение: {message}\n\n"
            "Спасибо за регистрацию!"
        )

        send_mail(
            subject="Подтверждение регистрации",
            message=full_message,
            from_email="rexavuum@gmail.com",  # заменим позже
            recipient_list=[email],
            fail_silently=False,
        )

        return HttpResponse("Письмо отправлено и данные сохранены!")
    
    return render(request, 'accounts/register.html')