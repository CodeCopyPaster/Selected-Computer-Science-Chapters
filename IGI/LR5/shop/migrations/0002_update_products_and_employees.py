from django.db import migrations
from django.core.files import File
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.utils import timezone
import os

def update_data(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    User = apps.get_model('shop', 'User')
    Employee = apps.get_model('shop', 'Employee')
    ProductCategory = apps.get_model('shop', 'ProductCategory')
    
    # Создаем категории
    categories = {
        'cakes': ProductCategory.objects.create(
            name='Торты',
            description='Праздничные и повседневные торты на любой вкус'
        ),
        'pastry': ProductCategory.objects.create(
            name='Пирожные',
            description='Изысканные пирожные и мелкая выпечка'
        ),
        'bread': ProductCategory.objects.create(
            name='Хлебобулочные изделия',
            description='Свежая выпечка и хлеб'
        )
    }
    
    # Обновляем продукты с изображениями
    products_data = [
        {
            'name': 'Торт "Наполеон"',
            'image': 'products/napoleon.jpg',
            'price': '1200.00',
            'category': categories['cakes']
        },
        {
            'name': 'Торт "Медовик"',
            'image': 'products/medovik.jpg',
            'price': '1100.00',
            'category': categories['cakes']
        },
        {
            'name': 'Эклер классический',
            'image': 'products/eclair.jpg',
            'price': '150.00',
            'category': categories['pastry']
        },
        {
            'name': 'Круассан с миндалем',
            'image': 'products/croissant.jpg',
            'price': '180.00',
            'category': categories['bread']
        },
        {
            'name': 'Макарон ассорти',
            'image': 'products/macaron.jpg',
            'price': '90.00',
            'category': categories['pastry']
        },
        {
            'name': 'Чизкейк Нью-Йорк',
            'image': 'products/cheesecake.jpg',
            'price': '950.00',
            'category': categories['cakes']
        },
        {
            'name': 'Тирамису',
            'image': 'products/tiramisu.jpg',
            'price': '850.00',
            'category': categories['pastry']
        },
        {
            'name': 'Пирожное картошка',
            'image': 'products/kartoshka.jpg',
            'price': '120.00',
            'category': categories['pastry']
        }
    ]

    for product_data in products_data:
        product = Product.objects.filter(name=product_data['name']).first()
        if not product:
            product = Product.objects.create(
                name=product_data['name'],
                price=product_data['price'],
                image=product_data['image'],
                description=f"Описание для {product_data['name']}",
                category=product_data['category'],
                available=True
            )
        else:
            product.price = product_data['price']
            product.image = product_data['image']
            product.category = product_data['category']
            product.save()

    # Создаем сотрудников
    employees_data = [
        {
            'username': 'maria_chef',
            'first_name': 'Мария',
            'last_name': 'Иванова',
            'email': 'maria@sweetdreams.com',
            'position': 'Шеф-кондитер',
            'phone_number': '+375 (29) 123-45-67',
            'description': 'Опытный шеф-кондитер с 15-летним стажем. Специализируется на авторских тортах и французских десертах.'
        },
        {
            'username': 'anna_baker',
            'first_name': 'Анна',
            'last_name': 'Петрова',
            'email': 'anna@sweetdreams.com',
            'position': 'Кондитер',
            'phone_number': '+375 (29) 234-56-78',
            'description': 'Мастер по работе с шоколадом и карамелью. Создает уникальные конфеты и пралине.'
        },
        {
            'username': 'pavel_pastry',
            'first_name': 'Павел',
            'last_name': 'Сидоров',
            'email': 'pavel@sweetdreams.com',
            'position': 'Пекарь',
            'phone_number': '+375 (29) 345-67-89',
            'description': 'Специалист по хлебобулочным изделиям. Создает восхитительные круассаны и слоеную выпечку.'
        }
    ]

    for emp_data in employees_data:
        user = User.objects.filter(username=emp_data['username']).first()
        if not user:
            user = User.objects.create(
                username=emp_data['username'],
                first_name=emp_data['first_name'],
                last_name=emp_data['last_name'],
                email=emp_data['email'],
                role='employee',
                password=make_password('employee123')
            )

            Employee.objects.create(
                user=user,
                position=emp_data['position'],
                phone_number=emp_data['phone_number'],
                description=emp_data['description'],
                birth_date=timezone.now().date(),
                hire_date=timezone.now().date()
            )

def reverse_func(apps, schema_editor):
    # Удаляем созданные данные
    User = apps.get_model('shop', 'User')
    Product = apps.get_model('shop', 'Product')
    ProductCategory = apps.get_model('shop', 'ProductCategory')
    
    User.objects.filter(username__in=['maria_chef', 'anna_baker', 'pavel_pastry']).delete()
    Product.objects.all().delete()
    ProductCategory.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(update_data, reverse_func),
    ] 