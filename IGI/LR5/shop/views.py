from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.db.models import Avg, Count, Sum, F, Q, Min, Max
from django.http import JsonResponse, Http404
from django.utils import timezone
from .models import (
    Product, ProductCategory, Order, OrderItem,
    Customer, Employee, Review, Promo, CompanyInfo, User, PickupPoint, Manufacturer, News
)
from .forms import UserRegistrationForm, UserLoginForm, OrderForm, OrderManagementForm, ProductForm, EmployeeForm
from decimal import Decimal
import logging
from django.views.decorators.http import require_POST
from .cart import Cart
import matplotlib
matplotlib.use('Agg')  # Use Agg backend
import matplotlib.pyplot as plt
import io
import base64
from django.db.models.functions import TruncMonth, TruncDay
import seaborn as sns
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.urls import reverse
from django.views.generic import ListView, DetailView
import requests
from django.core.cache import cache
import json
import pytz

logger = logging.getLogger(__name__)

# Decorators for role-based access
def admin_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Пожалуйста, войдите в систему.')
            return redirect('shop:login')
        if request.user.role != User.ADMIN:  # Используем константу из модели
            messages.error(request, 'У вас нет прав для доступа к этой странице.')
            return redirect('shop:home')
        return function(request, *args, **kwargs)
    return wrap

def employee_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Пожалуйста, войдите в систему.')
            return redirect('shop:login')
        if request.user.role != User.EMPLOYEE:  # Используем константу из модели
            messages.error(request, 'У вас нет прав для доступа к этой странице.')
            return redirect('shop:home')
        return function(request, *args, **kwargs)
    return wrap

def customer_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Пожалуйста, войдите в систему.')
            return redirect('shop:login')
        if request.user.role != User.CUSTOMER:  # Используем константу из модели
            messages.error(request, 'У вас нет прав для доступа к этой странице.')
            return redirect('shop:home')
        return function(request, *args, **kwargs)
    return wrap

# Public views (no authentication required)
def get_cat_fact():
    cache_key = 'cat_fact'
    fact_data = cache.get(cache_key)
    
    if fact_data is None:
        try:
            # Используем Cat Facts API для получения случайного факта о кошках
            url = 'https://catfact.ninja/fact'
            
            response = requests.get(url, timeout=5)
            print(f"Cat Fact API response status: {response.status_code}")  # Отладочная информация
            
            if response.status_code == 200:
                data = response.json()
                print(f"Cat Fact API response data: {data}")  # Отладочная информация
                
                fact_data = {
                    'text': data['fact'],
                    'icon': 'fas fa-cat'  # Font Awesome иконка кошки
                }
                # Кэшируем данные на 30 минут
                cache.set(cache_key, fact_data, 30 * 60)
                print(f"Cached cat fact data: {fact_data}")  # Отладочная информация
            else:
                print(f"Cat Fact API error: {response.text}")  # Отладочная информация
                fact_data = None
        except Exception as e:
            print(f"Error fetching cat fact data: {str(e)}")  # Отладочная информация
            fact_data = None
            
    return fact_data

def get_currency_rates():
    cache_key = 'currency_rates'
    currency_data = cache.get(cache_key)
    
    if currency_data is None:
        try:
            # Используем API Национального банка РБ
            url = 'https://www.nbrb.by/api/exrates/rates?periodicity=0'
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                currency_data = {
                    'USD': next((item for item in data if item['Cur_Abbreviation'] == 'USD'), None)['Cur_OfficialRate'],
                    'EUR': next((item for item in data if item['Cur_Abbreviation'] == 'EUR'), None)['Cur_OfficialRate'],
                    'RUB': next((item for item in data if item['Cur_Abbreviation'] == 'RUB'), None)['Cur_OfficialRate'],
                }
                # Кэшируем данные на 3 часа
                cache.set(cache_key, currency_data, 3 * 60 * 60)
            else:
                currency_data = None
        except Exception as e:
            print(f"Error fetching currency data: {e}")
            currency_data = None
            
    return currency_data

def get_minsk_time():
    minsk_tz = pytz.timezone('Europe/Minsk')
    return timezone.now().astimezone(minsk_tz)

def home(request):
    latest_news = News.objects.order_by('-created_at').first()
    categories = ProductCategory.objects.all()
    products = Product.objects.filter(available=True)[:8]
    
    # Получаем текущее время в Минске, случайный факт о кошках и курсы валют
    current_time = get_minsk_time()
    fact_data = get_cat_fact()
    currency_rates = get_currency_rates()
    
    context = {
        'categories': categories,
        'products': products,
        'latest_news': latest_news,
        'cat_fact': fact_data,
        'currency_rates': currency_rates,
        'current_time': current_time,
    }
    return render(request, 'shop/home.html', context)

def about(request):
    company_info = CompanyInfo.objects.first()
    return render(request, 'shop/about.html', {'company_info': company_info})

def news_list(request):
    # This will be implemented in the next semester
    return render(request, 'shop/news.html')

def glossary(request):
    """Страница со словарем кондитерских терминов"""
    return render(request, 'shop/glossary.html')

def contacts(request):
    """Страница контактов"""
    company_info = CompanyInfo.objects.first()
    employees = Employee.objects.select_related('user').all()
    return render(request, 'shop/contacts.html', {
        'company_info': company_info,
        'employees': employees
    })

def privacy(request):
    """Страница политики конфиденциальности"""
    return render(request, 'shop/privacy.html')

def vacancies(request):
    # This will be implemented in the next semester
    return render(request, 'shop/vacancies.html')

def reviews(request):
    reviews = Review.objects.select_related('customer', 'product').order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    context = {
        'reviews': reviews,
        'avg_rating': avg_rating
    }
    return render(request, 'shop/reviews.html', context)

def promotions(request):
    active_promotions = Promo.objects.filter(
        is_active=True,
        valid_from__lte=timezone.now(),
        valid_to__gte=timezone.now()
    )
    return render(request, 'shop/promotions.html', {'promotions': active_promotions})

def product_list(request):
    products = Product.objects.filter(available=True)
    categories = ProductCategory.objects.all()
    manufacturers = Manufacturer.objects.all()
    
    # Filtering
    category_id = request.GET.get('category')
    manufacturer_id = request.GET.get('manufacturer')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if category_id:
        products = products.filter(category_id=category_id)
    if manufacturer_id:
        products = products.filter(manufacturer_id=manufacturer_id)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
        
    # Sorting
    sort_by = request.GET.get('sort')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
        
    context = {
        'products': products,
        'categories': categories,
        'manufacturers': manufacturers,
        'current_category': category_id,
        'current_manufacturer': manufacturer_id,
        'current_sort': sort_by,
        'min_price': min_price,
        'max_price': max_price
    }
    return render(request, 'shop/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = Review.objects.filter(product=product).select_related('customer')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating
    }
    return render(request, 'shop/product_detail.html', context)

def category_products(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    products = Product.objects.filter(category=category, available=True)
    return render(request, 'shop/category_products.html', {
        'category': category,
        'products': products
    })

# Authentication views
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.save()
            
            # Создаем объект Customer для нового пользователя
            Customer.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone'],
                birth_date=form.cleaned_data['birth_date'],
                address=form.cleaned_data['address'] or ''
            )
            
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('shop:profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'shop/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вход выполнен успешно!')
            
            # Перенаправление в зависимости от роли
            if user.role == User.ADMIN:
                return redirect('shop:admin_dashboard')
            elif user.role == User.EMPLOYEE:
                return redirect('shop:employee_dashboard')
            else:
                return redirect('shop:profile')
    else:
        form = UserLoginForm()
    return render(request, 'shop/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы.')
    return redirect('shop:home')

# Customer views
@login_required
@customer_required
def customer_dashboard(request):
    orders = Order.objects.filter(customer=request.user)
    active_promos = Promo.objects.filter(
        is_active=True,
        valid_from__lte=timezone.now(),
        valid_to__gte=timezone.now()
    )
    pickup_points = PickupPoint.objects.filter(is_active=True)
    
    context = {
        'orders': orders,
        'active_promos': active_promos,
        'pickup_points': pickup_points,
        'total_spent': orders.aggregate(total=Sum('total_amount'))['total'] or 0,
        'orders_count': orders.count()
    }
    return render(request, 'shop/customer/dashboard.html', context)

@login_required
@customer_required
def place_order(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, 'Ваша корзина пуста')
        return redirect('shop:cart')

    if request.method == 'POST':
        try:
            # Создаем заказ
            order = Order.objects.create(
                customer=request.user,
                total_amount=cart.get_total_price()
            )

            # Добавляем товары из корзины в заказ
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price_at_time=item['price']
                )

            # Если был использован промокод, применяем его к заказу
            if cart.promo_code:
                try:
                    promo = Promo.objects.get(code=cart.promo_code)
                    order.promo = promo
                    # Пересчитываем сумму заказа с учетом скидки
                    discount = cart.get_promo_discount()
                    if discount:
                        order.total_amount = discount['final_price']
                    order.save()
                except Promo.DoesNotExist:
                    pass

            # Назначаем случайного сотрудника для обработки заказа
            try:
                employee = User.objects.filter(role=User.EMPLOYEE, is_active=True).order_by('?').first()
                if employee:
                    order.employee = employee
                    order.save()
            except Exception as e:
                logger.error(f"Ошибка при назначении сотрудника: {str(e)}")

            # Очищаем корзину
            cart.clear()
            
            messages.success(request, 'Заказ успешно оформлен!')
            return redirect('shop:order_detail', pk=order.id)
        except Exception as e:
            messages.error(request, f'Ошибка при оформлении заказа: {str(e)}')
            return redirect('shop:cart')
    
    return render(request, 'shop/place_order.html', {'cart': cart})

# Employee views
@login_required
@employee_required
def employee_dashboard(request):
    orders = Order.objects.filter(employee=request.user)
    customers = User.objects.filter(
        role=User.CUSTOMER,
        orders__employee=request.user
    ).distinct()
    
    context = {
        'orders': orders,
        'customers': customers,
        'total_orders': orders.count(),
        'total_sales': orders.aggregate(total=Sum('total_amount'))['total'] or 0
    }
    return render(request, 'shop/employee/dashboard.html', context)

@login_required
@employee_required
def order_management(request, order_id):
    order = get_object_or_404(Order, id=order_id, employee=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.id} status updated to {order.get_status_display()}')
    return render(request, 'shop/employee/order_detail.html', {'order': order})

@login_required
@employee_required
def employee_order_list(request):
    # Получаем все заказы, назначенные данному сотруднику
    orders = Order.objects.filter(employee=request.user).select_related('customer').order_by('-order_date')
    
    # Фильтрация по статусу
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    
    context = {
        'orders': orders,
        'current_status': status,
        'status_choices': Order.STATUS_CHOICES,
        'total_orders': orders.count(),
        'new_orders': orders.filter(status='new').count(),
        'processing_orders': orders.filter(status='processing').count(),
        'completed_orders': orders.filter(status='delivered').count()
    }
    return render(request, 'shop/employee/order_list.html', context)

@login_required
@employee_required
def employee_customer_list(request):
    customers = User.objects.filter(role=User.CUSTOMER).order_by('username')
    return render(request, 'shop/employee/customer_list.html', {'customers': customers})

# Admin views
@login_required
@admin_required
def admin_dashboard(request):
    today = timezone.now().date()
    
    # Статистика за сегодня
    today_orders = Order.objects.filter(order_date__date=today)
    today_sales = today_orders.aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Общая статистика
    context = {
        'total_products': Product.objects.filter(available=True).count(),
        'total_orders': Order.objects.count(),
        'total_customers': User.objects.filter(role=User.CUSTOMER).count(),
        'total_sales': Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0,
        
        # Статистика за сегодня
        'today_sales': today_sales,
        'new_orders': Order.objects.filter(status='new').count(),
        'active_customers': User.objects.filter(role=User.CUSTOMER, is_active=True).count(),
        'active_promos': Promo.objects.filter(
            is_active=True,
            valid_from__lte=timezone.now(),
            valid_to__gte=timezone.now()
        ).count(),
        
        # Последние заказы
        'recent_orders': Order.objects.select_related('customer').order_by('-order_date')[:10],
        
        # Последние товары
        'recent_products': Product.objects.select_related('category').order_by('-created_at')[:10]
    }
    return render(request, 'shop/admin/dashboard.html', context)

@login_required
@admin_required
def admin_product_list(request):
    products = Product.objects.select_related('category', 'manufacturer').all()
    
    # Фильтрация
    category_id = request.GET.get('category')
    manufacturer_id = request.GET.get('manufacturer')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if category_id:
        products = products.filter(category_id=category_id)
    if manufacturer_id:
        products = products.filter(manufacturer_id=manufacturer_id)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
        
    # Добавляем количество проданных товаров
    products = products.annotate(
        total_sold=Count('orderitem')
    )
    
    # Получаем списки категорий и производителей для фильтров
    categories = ProductCategory.objects.all()
    manufacturers = Manufacturer.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'manufacturers': manufacturers
    }
    return render(request, 'shop/admin/product_list.html', context)

@login_required
@admin_required
def admin_product_add(request):
    if request.method == 'POST':
        try:
            product = Product.objects.create(
                name=request.POST.get('name'),
                description=request.POST.get('description'),
                category_id=request.POST.get('category'),
                manufacturer_id=request.POST.get('manufacturer'),
                price=request.POST.get('price'),
                weight=request.POST.get('weight'),
                calories=request.POST.get('calories'),
                ingredients=request.POST.get('ingredients'),
                proteins=request.POST.get('proteins'),
                fats=request.POST.get('fats'),
                carbohydrates=request.POST.get('carbohydrates'),
                shelf_life=request.POST.get('shelf_life'),
                available=request.POST.get('available') == 'on',
                featured=request.POST.get('featured') == 'on'
            )
            if 'image' in request.FILES:
                product.image = request.FILES['image']
                product.save()
            return render(request, 'shop/admin/success.html', {
                'message': f'Товар "{product.name}" успешно добавлен',
                'return_url': reverse('shop:admin_product_list')
            })
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении товара: {str(e)}')
    
    categories = ProductCategory.objects.all()
    manufacturers = Manufacturer.objects.all()
    return render(request, 'shop/admin/product_form.html', {
        'categories': categories,
        'manufacturers': manufacturers
    })

@login_required
@admin_required
def admin_product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        try:
            product.name = request.POST.get('name')
            product.description = request.POST.get('description')
            product.category_id = request.POST.get('category')
            product.manufacturer_id = request.POST.get('manufacturer')
            product.price = request.POST.get('price')
            product.weight = request.POST.get('weight')
            product.calories = request.POST.get('calories')
            product.ingredients = request.POST.get('ingredients')
            product.proteins = request.POST.get('proteins')
            product.fats = request.POST.get('fats')
            product.carbohydrates = request.POST.get('carbohydrates')
            product.shelf_life = request.POST.get('shelf_life')
            product.available = request.POST.get('available') == 'on'
            product.featured = request.POST.get('featured') == 'on'
            
            if 'image' in request.FILES:
                if product.image:
                    default_storage.delete(product.image.path)
                product.image = request.FILES['image']
            product.save()
            messages.success(request, f'Товар "{product.name}" успешно обновлен')
            return redirect('shop:admin_product_list')
        except Exception as e:
            messages.error(request, f'Ошибка при обновлении товара: {str(e)}')
    
    categories = ProductCategory.objects.all()
    manufacturers = Manufacturer.objects.all()
    return render(request, 'shop/admin/product_form.html', {
        'product': product,
        'categories': categories,
        'manufacturers': manufacturers
    })

@login_required
@admin_required
def admin_category_list(request):
    categories = ProductCategory.objects.annotate(
        products_count=Count('products'),
        total_sales=Sum('products__orderitem__price_at_time')
    ).order_by('name')
    return render(request, 'shop/admin/category_list.html', {'categories': categories})

@login_required
@admin_required
def admin_category_add(request):
    if request.method == 'POST':
        try:
            category = ProductCategory.objects.create(
                name=request.POST.get('name'),
                description=request.POST.get('description')
            )
            if 'image' in request.FILES:
                category.image = request.FILES['image']
                category.save()
            return render(request, 'shop/admin/success.html', {
                'message': f'Категория "{category.name}" успешно добавлена',
                'return_url': reverse('shop:admin_category_list')
            })
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении категории: {str(e)}')
    return render(request, 'shop/admin/category_form.html')

@login_required
@admin_required
def admin_category_edit(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        try:
            category.name = request.POST.get('name')
            category.description = request.POST.get('description')
            if 'image' in request.FILES:
                if category.image:
                    default_storage.delete(category.image.path)
                category.image = request.FILES['image']
            category.save()
            messages.success(request, f'Категория "{category.name}" успешно обновлена')
            return redirect('shop:admin_category_list')
        except Exception as e:
            messages.error(request, f'Ошибка при обновлении категории: {str(e)}')
    return render(request, 'shop/admin/category_form.html', {'category': category})

@login_required
@admin_required
def admin_category_delete(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        try:
            # Удаляем изображение категории, если оно есть
            if category.image:
                default_storage.delete(category.image.path)
            category.delete()
            messages.success(request, f'Категория "{category.name}" успешно удалена')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении категории: {str(e)}')
    return redirect('shop:admin_category_list')

@login_required
@admin_required
def admin_manufacturer_list(request):
    manufacturers = Manufacturer.objects.annotate(
        products_count=Count('products'),
        total_sales=Sum('products__orderitem__price_at_time')
    ).order_by('name')
    return render(request, 'shop/admin/manufacturer_list.html', {'manufacturers': manufacturers})

@login_required
@admin_required
def admin_manufacturer_add(request):
    if request.method == 'POST':
        try:
            manufacturer = Manufacturer.objects.create(
                name=request.POST.get('name'),
                description=request.POST.get('description'),
                country=request.POST.get('country'),
                website=request.POST.get('website'),
                contact_info=request.POST.get('contact_info', '')
            )
            if 'logo' in request.FILES:
                manufacturer.logo = request.FILES['logo']
                manufacturer.save()
            return render(request, 'shop/admin/success.html', {
                'message': f'Производитель "{manufacturer.name}" успешно добавлен',
                'show_return_button': False
            })
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении производителя: {str(e)}')
    return render(request, 'shop/admin/manufacturer_form.html')

@login_required
@admin_required
def admin_manufacturer_edit(request, pk):
    manufacturer = get_object_or_404(Manufacturer, pk=pk)
    if request.method == 'POST':
        try:
            manufacturer.name = request.POST.get('name')
            manufacturer.description = request.POST.get('description')
            manufacturer.country = request.POST.get('country')
            manufacturer.website = request.POST.get('website')
            if 'logo' in request.FILES:
                if manufacturer.logo:
                    default_storage.delete(manufacturer.logo.path)
                manufacturer.logo = request.FILES['logo']
            manufacturer.save()
            messages.success(request, f'Производитель "{manufacturer.name}" успешно обновлен')
            return redirect('shop:admin_manufacturer_list')
        except Exception as e:
            messages.error(request, f'Ошибка при обновлении производителя: {str(e)}')
    return render(request, 'shop/admin/manufacturer_form.html', {'manufacturer': manufacturer})

@login_required
@admin_required
def admin_manufacturer_delete(request, pk):
    manufacturer = get_object_or_404(Manufacturer, pk=pk)
    if request.method == 'POST':
        try:
            # Удаляем логотип производителя, если он есть
            if manufacturer.logo:
                default_storage.delete(manufacturer.logo.path)
            manufacturer.delete()
            messages.success(request, f'Производитель "{manufacturer.name}" успешно удален')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении производителя: {str(e)}')
    return redirect('shop:admin_manufacturer_list')

@login_required
@admin_required
def admin_order_list(request):
    orders = Order.objects.select_related('customer').prefetch_related('items__product').all()
    
    # Фильтрация по статусу
    status = request.GET.get('status')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if status:
        orders = orders.filter(status=status)
    if date_from:
        orders = orders.filter(order_date__date__gte=date_from)
    if date_to:
        orders = orders.filter(order_date__date__lte=date_to)
        
    orders = orders.order_by('-order_date')
    
    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'current_status': status,
        'date_from': date_from,
        'date_to': date_to
    }
    return render(request, 'shop/admin/order_list.html', context)

@login_required
@admin_required
def admin_order_cancel(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.status = 'cancelled'
        order.save()
        return render(request, 'shop/admin/success.html', {
            'message': f'Заказ #{order.id} успешно отменен',
            'return_url': reverse('shop:admin_order_list')
        })
    return redirect('shop:admin_order_list')

@login_required
@admin_required
def admin_order_detail(request, pk):
    order = get_object_or_404(Order.objects.select_related('customer', 'promo')
                             .prefetch_related('items__product'), pk=pk)
    if request.method == 'POST':
        form = OrderManagementForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус заказа обновлен')
            return redirect('shop:admin_order_list')
    else:
        form = OrderManagementForm(instance=order)
    return render(request, 'shop/admin/order_detail.html', {'order': order, 'form': form})

@login_required
@admin_required
def admin_customer_list(request):
    # Базовый queryset
    customers = User.objects.filter(role=User.CUSTOMER)

    # Поиск
    search = request.GET.get('search')
    if search:
        customers = customers.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )

    # Сортировка
    sort = request.GET.get('sort', 'orders_count')
    if sort == 'orders_count':
        customers = customers.annotate(
            orders_count=Count('orders')
        ).order_by('-orders_count')
    elif sort == 'total_spent':
        customers = customers.annotate(
            total_spent=Sum('orders__total_amount')
        ).order_by('-total_spent')
    elif sort == 'date_joined':
        customers = customers.order_by('-date_joined')

    # Добавляем аннотации для отображения в шаблоне
    customers = customers.annotate(
        orders_count=Count('orders'),
        total_spent=Sum('orders__total_amount')
    )

    return render(request, 'shop/admin/customer_list.html', {'customers': customers})

@login_required
@admin_required
def admin_employee_list(request):
    employees = User.objects.filter(role=User.EMPLOYEE).annotate(
        orders_processed=Count('processed_orders')
    ).order_by('-date_joined')
    return render(request, 'shop/admin/employee_list.html', {'employees': employees})

@login_required
@admin_required
def admin_employee_add(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f'Сотрудник {employee.get_full_name() or employee.username} успешно добавлен')
            return redirect('shop:admin_employee_list')
    else:
        form = EmployeeForm()
    
    return render(request, 'shop/admin/employee_form.html', {
        'form': form,
        'title': 'Добавление сотрудника'
    })

@login_required
@admin_required
def admin_employee_edit(request, pk):
    employee = get_object_or_404(User, pk=pk, role=User.EMPLOYEE)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f'Данные сотрудника {employee.get_full_name() or employee.username} обновлены')
            return redirect('shop:admin_employee_list')
    else:
        form = EmployeeForm(instance=employee)
    
    return render(request, 'shop/admin/employee_form.html', {
        'form': form,
        'employee': employee,
        'title': f'Редактирование сотрудника: {employee.get_full_name() or employee.username}'
    })

@login_required
@admin_required
def admin_employee_toggle_status(request, pk):
    employee = get_object_or_404(User, pk=pk, role=User.EMPLOYEE)
    if request.method == 'POST':
        employee.is_active = not employee.is_active
        employee.save()
        status = "активирован" if employee.is_active else "заблокирован"
        messages.success(request, f'Сотрудник {employee.get_full_name() or employee.username} {status}')
    return redirect('shop:admin_employee_list')

@login_required
@admin_required
def admin_review_list(request):
    reviews = Review.objects.select_related('customer', 'product').all()
    return render(request, 'shop/admin/review_list.html', {'reviews': reviews})

@login_required
@admin_required
def admin_promo_list(request):
    promos = Promo.objects.annotate(
        usage_count=Count('orders'),
        total_discount=Sum(F('orders__total_amount') * F('discount_percent') / 100.0)
    )
    return render(request, 'shop/admin/promo_list.html', {'promos': promos})

@login_required
@admin_required
def admin_promo_add(request):
    if request.method == 'POST':
        try:
            promo = Promo.objects.create(
                code=request.POST.get('code'),
                description=request.POST.get('description'),
                discount_percent=float(request.POST.get('discount_percent')),
                valid_from=request.POST.get('valid_from'),
                valid_to=request.POST.get('valid_to'),
                is_active=request.POST.get('is_active') == 'on'
            )
            return render(request, 'shop/admin/success.html', {
                'message': f'Промокод "{promo.code}" успешно добавлен',
                'show_return_button': False
            })
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении промокода: {str(e)}')
    return render(request, 'shop/admin/promo_form.html', {
        'title': 'Добавление промокода'
    })

@login_required
@admin_required
def admin_promo_edit(request, pk):
    promo = get_object_or_404(Promo, pk=pk)
    if request.method == 'POST':
        code = request.POST.get('code')
        discount_percent = request.POST.get('discount_percent')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        description = request.POST.get('description')
        is_active = request.POST.get('is_active') == 'on'
        
        if code and discount_percent:
            try:
                promo.code = code
                promo.discount_percent = float(discount_percent)
                promo.valid_from = valid_from
                promo.valid_to = valid_to
                promo.description = description
                promo.is_active = is_active
                promo.save()
                messages.success(request, 'Промокод успешно обновлен')
                return redirect('shop:admin_promo_list')
            except ValueError:
                messages.error(request, 'Проверьте правильность введенных данных')
        else:
            messages.error(request, 'Код и процент скидки обязательны')
    return render(request, 'shop/admin/promo_form.html', {
        'promo': promo,
        'title': f'Редактирование промокода: {promo.code}'
    })

@login_required
@admin_required
def admin_product_stats(request):
    # Получаем базовую статистику
    stats = {
        'top_products': Product.objects.annotate(
            total_ordered=Count('orderitem')
        ).select_related('category').order_by('-total_ordered')[:10],
        'category_distribution': ProductCategory.objects.annotate(
            products_count=Count('products')
        ),
        'price_ranges': Product.objects.aggregate(
            min_price=Min('price'),
            max_price=Max('price'),
            avg_price=Avg('price')
        )
    }

    # Создаем графики с помощью matplotlib
    charts = {}

    
    categories = list(ProductCategory.objects.annotate(count=Count('products')))
    if categories:
        plt.figure(figsize=(10, 6))
        plt.pie([c.count for c in categories], 
                labels=[c.name for c in categories],
                autopct='%1.1f%%')
        plt.title('Распределение товаров по категориям')
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        charts['category_distribution'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()

    
    top_products = stats['top_products']
    if top_products:
        plt.figure(figsize=(12, 6))
        plt.bar([p.name for p in top_products], [p.price for p in top_products])
        plt.xticks(rotation=45, ha='right')
        plt.title('Цены топ-10 самых продаваемых товаров')
        plt.ylabel('Цена (₽)')
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        charts['top_products_prices'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()

    stats['charts'] = charts
    return render(request, 'shop/admin/product_stats.html', {'stats': stats})

@login_required
@admin_required
def admin_customer_stats(request):
    stats = {
        'top_customers': User.objects.filter(role=User.CUSTOMER).annotate(
            total_spent=Sum('orders__total_amount')
        ).order_by('-total_spent')[:10],
        'new_customers': User.objects.filter(
            role=User.CUSTOMER,
            date_joined__gte=timezone.now() - timezone.timedelta(days=30)
        ).count(),
        'customer_activity': Order.objects.values('customer').annotate(
            order_count=Count('id'),
            total_spent=Sum('total_amount')
        ).order_by('-order_count')
    }
    return render(request, 'shop/admin/customer_stats.html', {'stats': stats})

@login_required
@admin_required
def admin_delivery_stats(request):
    stats = {
        'delivery_times': Order.objects.annotate(
            delivery_time=F('delivery_date') - F('order_date')
        ).aggregate(
            avg_time=Avg('delivery_time'),
            min_time=Min('delivery_time'),
            max_time=Max('delivery_time')
        ),
        'orders_by_status': Order.objects.values('status').annotate(
            count=Count('id')
        ),
        'delivery_costs': Order.objects.aggregate(
            total_delivery_cost=Sum('delivery_cost'),
            avg_delivery_cost=Avg('delivery_cost')
        )
    }
    return render(request, 'shop/admin/delivery_stats.html', {'stats': stats})

# Public views
def apply_promo(request):
    if request.method == 'POST':
        if 'remove_promo' in request.POST:
            if 'promo_code' in request.session:
                del request.session['promo_code']
                messages.success(request, 'Промокод удален')
        else:
            code = request.POST.get('promo_code')
            try:
                promo = Promo.objects.get(
                    code=code,
                    is_active=True,
                    valid_from__lte=timezone.now(),
                    valid_to__gte=timezone.now()
                )
                # Сохраняем промокод в сессии
                request.session['promo_code'] = promo.code
                messages.success(request, f'Промокод {promo.code} успешно применен! Скидка {promo.discount_percent}%')
            except Promo.DoesNotExist:
                messages.error(request, 'Недействительный промокод')
    
    # Перенаправляем на предыдущую страницу
    return redirect(request.META.get('HTTP_REFERER', 'shop:promotions'))

@login_required
def cart(request):
    # This will be implemented using sessions
    return render(request, 'shop/cart.html')

@require_POST
@login_required
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity)
    return redirect('shop:cart')

@require_POST
@login_required
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart')

@require_POST
@login_required
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity, override_quantity=True)
    return redirect('shop:cart')

@login_required
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart.html', {'cart': cart})

@login_required
def order_list(request):
    if request.user.role != User.CUSTOMER:
        messages.error(request, 'Доступ запрещен. Эта страница только для покупателей.')
        return redirect('shop:home')
        
    orders = Order.objects.filter(customer=request.user)
    return render(request, 'shop/order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if not hasattr(request.user, 'customer') or order.customer != request.user.customer:
        messages.error(request, "You don't have permission to view this order.")
        return redirect('shop:order_list')
    return render(request, 'shop/order_detail.html', {'order': order})

@login_required
def add_review(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        try:
            # Получаем или создаем объект Customer для пользователя
            customer, created = Customer.objects.get_or_create(
                user=request.user,
                defaults={
                    'phone_number': '+375 (29) 000-00-00',
                    'birth_date': timezone.now().date(),
                    'address': request.user.address or ''
                }
            )
            
            rating = int(request.POST.get('rating'))
            comment = request.POST.get('comment')
            
            Review.objects.create(
                customer=customer,
                product=product,
                rating=rating,
                comment=comment
            )
            messages.success(request, "Спасибо за ваш отзыв!")
        except Exception as e:
            logger.error(f"Error adding review: {str(e)}")
            messages.error(request, "Произошла ошибка при добавлении отзыва.")
    return redirect('shop:product_detail', pk=product_id)

# API Views
def api_product_list(request):
    products = Product.objects.filter(available=True).values('id', 'name', 'price', 'unit')
    return JsonResponse({'products': list(products)})

@login_required
def api_order_list(request):
    if not hasattr(request.user, 'customer'):
        return JsonResponse({'error': 'Not authorized'}, status=403)
    
    orders = Order.objects.filter(customer=request.user.customer).values(
        'id', 'order_date', 'status', 'total_amount'
    )
    return JsonResponse({'orders': list(orders)})

@login_required
def profile_update(request):
    if request.method == 'POST':
        user = request.user
        user.phone = request.POST.get('phone', '')
        user.address = request.POST.get('address', '')
        user.save()
        messages.success(request, 'Профиль успешно обновлен!')
        return redirect('shop:profile')
    return redirect('shop:profile')

def manufacturer_products(request, pk):
    manufacturer = get_object_or_404(Manufacturer, pk=pk)
    products = Product.objects.filter(manufacturer=manufacturer, available=True)
    return render(request, 'shop/manufacturer_products.html', {
        'manufacturer': manufacturer,
        'products': products
    })

def pickup_points_list(request):
    return render(request, '404.html', status=404)

@login_required
def profile(request):
    context = {
        'user': request.user,
        'orders': Order.objects.filter(customer=request.user).order_by('-order_date') if hasattr(request.user, 'customer') else [],
    }
    return render(request, 'shop/profile.html', context)

@login_required
def fill_profile(request):
    # Проверяем, есть ли уже профиль у пользователя
    if hasattr(request.user, 'customer'):
        messages.warning(request, 'Ваш профиль уже заполнен')
        return redirect('shop:profile')

    if request.method == 'POST':
        try:
            # Создаем объект Customer
            customer = Customer.objects.create(
                user=request.user,
                phone_number=request.POST.get('phone_number'),
                birth_date=request.POST.get('birth_date'),
                address=request.POST.get('address')
            )
            messages.success(request, 'Профиль успешно заполнен!')
            return redirect('shop:profile')
        except Exception as e:
            messages.error(request, f'Ошибка при сохранении профиля: {str(e)}')
            return render(request, 'shop/profile_form.html')

    return render(request, 'shop/profile_form.html')

@login_required
@admin_required
def admin_product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        try:
            # Удаляем изображение товара, если оно есть
            if product.image:
                default_storage.delete(product.image.path)
            product.delete()
            messages.success(request, f'Товар "{product.name}" успешно удален')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении товара: {str(e)}')
    return redirect('shop:admin_product_list')

@login_required
@admin_required
def admin_sales_stats(request):
    # Получаем параметры фильтрации
    period = request.GET.get('period', 'month')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    # Базовый queryset заказов
    orders = Order.objects.all()

    # Применяем фильтры по датам
    if date_from:
        orders = orders.filter(order_date__date__gte=date_from)
    if date_to:
        orders = orders.filter(order_date__date__lte=date_to)
    elif period:
        if period == 'week':
            date_from = timezone.now() - timezone.timedelta(days=7)
        elif period == 'month':
            date_from = timezone.now() - timezone.timedelta(days=30)
        elif period == 'year':
            date_from = timezone.now() - timezone.timedelta(days=365)
        orders = orders.filter(order_date__gte=date_from)

    # Статистика
    total_sales = orders.aggregate(total=Sum('total_amount'))['total'] or 0
    total_orders = orders.count()
    average_order = total_sales / total_orders if total_orders > 0 else 0
    active_customers = User.objects.filter(role=User.CUSTOMER, orders__isnull=False).distinct().count()

    # Графики
    charts = {}

    # 1. График продаж по времени
    sales_by_date = orders.annotate(
        date=TruncDay('order_date')
    ).values('date').annotate(
        total=Sum('total_amount')
    ).order_by('date')

    if sales_by_date:
        plt.figure(figsize=(12, 6))
        dates = [x['date'] for x in sales_by_date]
        totals = [x['total'] for x in sales_by_date]
        plt.plot(dates, totals, marker='o')
        plt.title('Динамика продаж')
        plt.xlabel('Дата')
        plt.ylabel('Сумма продаж (₽)')
        plt.xticks(rotation=45)
        plt.grid(True)
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        charts['sales_over_time'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()

    # 2. График продаж по категориям
    sales_by_category = ProductCategory.objects.annotate(
        total_sales=Sum('products__orderitem__price_at_time')
    ).filter(total_sales__gt=0).order_by('-total_sales')

    if sales_by_category:
        plt.figure(figsize=(8, 8))
        plt.pie(
            [x.total_sales for x in sales_by_category],
            labels=[x.name for x in sales_by_category],
            autopct='%1.1f%%'
        )
        plt.title('Продажи по категориям')
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        charts['sales_by_category'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()

    # 3. Топ-10 продуктов
    top_products = Product.objects.annotate(
        total_sales=Sum('orderitem__price_at_time')
    ).filter(total_sales__gt=0).order_by('-total_sales')[:10]

    if top_products:
        plt.figure(figsize=(12, 6))
        plt.bar(
            [p.name for p in top_products],
            [p.total_sales for p in top_products]
        )
        plt.title('Топ-10 продуктов по продажам')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('Сумма продаж (₽)')
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        charts['top_products'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()

    context = {
        'period': period,
        'date_from': date_from,
        'date_to': date_to,
        'total_sales': total_sales,
        'total_orders': total_orders,
        'average_order': average_order,
        'active_customers': active_customers,
        'charts': charts,
        'sales_by_category': sales_by_category,
        'top_products': top_products
    }
    return render(request, 'shop/admin/sales_stats.html', context)

class NewsListView(ListView):
    model = News
    template_name = 'shop/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

class NewsDetailView(DetailView):
    model = News
    template_name = 'shop/news_detail.html'
    context_object_name = 'news'

def index(request):
    latest_news = News.objects.first()
    categories = ProductCategory.objects.all()
    products = Product.objects.all()[:8]
    context = {
        'categories': categories,
        'products': products,
        'latest_news': latest_news,
    }
    return render(request, 'shop/index.html', context) 