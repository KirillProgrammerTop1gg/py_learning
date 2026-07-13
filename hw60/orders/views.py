from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order
from .forms import RegistrationForm, LoginForm, OrderBriefForm, ReviewForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('orders:profile')
        
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Автоматично авторизуємо користувача після реєстрації
            login(request, user)
            messages.success(request, "Реєстрація пройшла успішно! Ласкаво просимо.")
            return redirect('orders:profile')
    else:
        form = RegistrationForm()
        
    return render(request, 'orders/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('orders:profile')
        
    next_url = request.GET.get('next', 'orders:profile')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Вітаємо, {username}! Ви успішно увійшли.")
                from django.utils.http import url_has_allowed_host_and_scheme
                if next_url and next_url != 'orders:profile' and not next_url.startswith('orders:'):
                    if url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
                        return redirect(next_url)
                return redirect('orders:profile')
            else:
                form.add_error(None, "Неправильне ім'я користувача або пароль.")
    else:
        form = LoginForm()
        
    return render(request, 'orders/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    logout(request)
    messages.info(request, "Ви вийшли з системи.")
    return redirect('portfolio:home')


@login_required
def profile_view(request):
    if request.user.is_staff or request.user.is_superuser:
        # Адміністратор бачить глобальну аналітику по всій системі
        orders_queryset = Order.objects.all()
        completed_no_review_orders = Order.objects.none()
    else:
        # Звичайний користувач бачить тільки свої заявки
        orders_queryset = Order.objects.filter(user=request.user)
        # Знаходимо виконані замовлення користувача, на які ще немає відгуку
        completed_no_review_orders = Order.objects.filter(
            user=request.user, 
            status='completed', 
            review__isnull=True
        )

    from django.db.models import Count, Q
    stats = orders_queryset.aggregate(
        total=Count('id'),
        pending=Count('id', filter=Q(status='pending')),
        active=Count('id', filter=Q(status='in_progress')),
        completed=Count('id', filter=Q(status='completed'))
    )
    total_orders = stats['total']
    pending_orders = stats['pending']
    active_orders = stats['active']
    completed_orders = stats['completed']
    
    # Створюємо інстанс форми для кожного замовлення без відгуку або обробляємо POST
    review_form = None
    if not request.user.is_staff and not request.user.is_superuser and completed_no_review_orders.exists():
        if request.method == 'POST' and 'submit_review' in request.POST:
            order_id = request.POST.get('order_id')
            try:
                # Перевіряємо безпеку: замовлення має належати користувачу, бути виконаним і не мати відгуку
                target_order = completed_no_review_orders.get(id=order_id)
                form = ReviewForm(request.POST)
                if form.is_valid():
                    review = form.save(commit=False)
                    review.user = request.user
                    review.order = target_order
                    review.save()
                    messages.success(request, f"Дякуємо! Ваш відгук про проект '{target_order.project_name}' успішно збережено.")
                    return redirect('orders:profile')
            except Order.DoesNotExist:
                messages.error(request, "Невірне замовлення для відгуку.")
        else:
            review_form = ReviewForm()

    # Розширена аналітика для Адміністратора
    page_views = None
    popular_projects = None
    monthly_activity_graph = None
    
    if request.user.is_staff or request.user.is_superuser:
        from portfolio.models import PageView, Project
        # 1. Підрахунок переглядів сторінок (топ 10)
        page_views = PageView.objects.all().order_by('-views_count')[:10]
        
        # 2. Статистика найпопулярніших проектів (топ 5)
        popular_projects = Project.objects.all().order_by('-views_count')[:5]
        
        # 3. Графіки активності замовлень по місяцях (групування в Python для 100% сумісності з СУБД)
        from collections import OrderedDict
        order_dates = list(Order.objects.all().values_list('created_at', flat=True))
        
        monthly_counts = {}
        for dt in order_dates:
            if dt:
                month_str = dt.strftime('%Y-%m')
                monthly_counts[month_str] = monthly_counts.get(month_str, 0) + 1
                
        sorted_months = OrderedDict(sorted(monthly_counts.items()))
        
        max_orders_in_any_month = max(monthly_counts.values()) if monthly_counts else 1
        monthly_activity_graph = []
        for month_str, count in sorted_months.items():
            bar_length = int((count / max_orders_in_any_month) * 20)
            bar = "#" * bar_length + "-" * (20 - bar_length)
            monthly_activity_graph.append({
                'month': month_str,
                'count': count,
                'bar': bar,
            })

    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'active_orders': active_orders,
        'completed_orders': completed_orders,
        'completed_no_review_orders': completed_no_review_orders,
        'review_form': review_form,
        'page_views': page_views,
        'popular_projects': popular_projects,
        'monthly_activity_graph': monthly_activity_graph,
    }
    return render(request, 'orders/profile.html', context)


@login_required
def create_order_view(request):
    if request.method == 'POST':
        form = OrderBriefForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            
            # Автоматичне надсилання email сповіщення адміністраторам (HTML + Текст)
            from django.core.mail import EmailMultiAlternatives
            from django.template.loader import render_to_string
            from django.conf import settings
            from django.contrib.auth import get_user_model
            
            try:
                subject = f"[Новий Бриф] {order.project_name}"
                
                # Контекст для рендерингу шаблонів
                context = {
                    'project_name': order.project_name,
                    'project_type_display': order.get_project_type_display(),
                    'budget': order.budget,
                    'timeline': order.timeline,
                    'username': request.user.username,
                    'user_email': request.user.email,
                    'contacts': order.contacts,
                    'description': order.description,
                    'admin_url': request.build_absolute_uri('/admin/orders/order/'),
                }
                
                # Рендеримо HTML
                html_content = render_to_string('emails/admin_new_order.html', context)
                
                # Простий текстовий варіант (якщо поштовий клієнт не підтримує HTML)
                text_content = f"Привіт, Кірілле!\n\n" \
                               f"На твоєму сайті 'Вечірній термінал' залишено новий технічний бриф!\n\n" \
                               f"--- ДЕТАЛІ ЗАМОВЛЕННЯ ---\n" \
                               f"Назва проекту: {order.project_name}\n" \
                               f"Тип проекту: {order.get_project_type_display()}\n" \
                               f"Орієнтовний бюджет: {order.budget} USD\n" \
                               f"Терміни: {order.timeline}\n" \
                               f"Клієнт: @{request.user.username} ({request.user.email})\n" \
                               f"Контакти: {order.contacts}\n\n" \
                               f"--- ТЕХНІЧНЕ ЗАВДАННЯ ---\n" \
                               f"{order.description}\n\n" \
                               f"-------------------------\n" \
                               f"Переглянути замовлення у Django Admin: {context['admin_url']}\n"
                
                # Знаходимо всі адреси суперкористувачів
                admin_emails = list(get_user_model().objects.filter(is_superuser=True).exclude(email='').values_list('email', flat=True))
                if not admin_emails:
                    admin_emails = ['kirillwork31@gmail.com']
                
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=admin_emails
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send(fail_silently=True)
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Помилка відправки HTML email: {e}")

            messages.success(request, "Ваш технічний бриф успішно надіслано! Кірілл незабаром перегляне його.")
            return redirect('orders:list')
    else:
        form = OrderBriefForm()
        
    return render(request, 'orders/create_order.html', {'form': form})


@login_required
def user_orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/user_orders.html', {'orders': orders})
