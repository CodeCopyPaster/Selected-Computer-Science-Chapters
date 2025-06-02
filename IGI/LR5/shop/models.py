from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone
from decimal import Decimal

class User(AbstractUser):
    ADMIN = 'admin'
    EMPLOYEE = 'employee'
    CUSTOMER = 'customer'
    
    ROLE_CHOICES = [
        (ADMIN, 'Administrator'),
        (EMPLOYEE, 'Employee'),
        (CUSTOMER, 'Customer'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CUSTOMER)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='shop_user_set',
        related_query_name='shop_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='shop_user_set',
        related_query_name='shop_user',
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def save(self, *args, **kwargs):
        if self.is_superuser and self.role != self.ADMIN:
            self.role = self.ADMIN
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Manufacturer(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='manufacturers/', null=True, blank=True)
    contact_info = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    unit = models.CharField(max_length=50, choices=[
        ('piece', 'Штука'),
        ('kg', 'Килограмм'),
        ('g', 'Грамм'),
        ('box', 'Коробка'),
    ], default='piece')
    
    # Физические характеристики
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text='Вес в граммах')
    calories = models.PositiveIntegerField(null=True, blank=True, help_text='Калорийность на 100г')
    
    # Состав и пищевая ценность
    ingredients = models.TextField(blank=True, help_text='Состав продукта')
    proteins = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Белки на 100г')
    fats = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Жиры на 100г')
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Углеводы на 100г')
    shelf_life = models.PositiveIntegerField(null=True, blank=True, help_text='Срок годности в днях')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class PickupPoint(models.Model):
    address = models.CharField(max_length=255)
    working_hours = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.address

class Promo(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    discount_percent = models.IntegerField(validators=[MinValueValidator(0)])
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.code

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В обработке'),
        ('confirmed', 'Подтвержден'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='handled_orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.SET_NULL, null=True)
    promo = models.ForeignKey(Promo, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Заказ #{self.id} от {self.customer.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)  # Price at the time of purchase
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name} в заказе #{self.order.id}"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(
        max_length=19,
        validators=[
            RegexValidator(
                regex=r'^\+375 \((?:29|33|44|25)\) [0-9]{3}-[0-9]{2}-[0-9]{2}$',
                message="Phone number must be in format: '+375 (29) XXX-XX-XX'"
            )
        ]
    )
    birth_date = models.DateField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.phone_number}"

    def age(self):
        today = timezone.now().date()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(
        max_length=19,
        validators=[
            RegexValidator(
                regex=r'^\+375 \((?:29|33|44|25)\) [0-9]{3}-[0-9]{2}-[0-9]{2}$',
                message="Phone number must be in format: '+375 (29) XXX-XX-XX'"
            )
        ]
    )
    position = models.CharField(max_length=100)
    birth_date = models.DateField()
    hire_date = models.DateField()
    photo = models.ImageField(upload_to='employees/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent')
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.customer.user.get_full_name()} for {self.product.name}"

class CompanyInfo(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to='company/', null=True, blank=True)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(
        max_length=19,
        validators=[
            RegexValidator(
                regex=r'^\+375 \((?:29|33|44|25)\) [0-9]{3}-[0-9]{2}-[0-9]{2}$',
                message="Phone number must be in format: '+375 (29) XXX-XX-XX'"
            )
        ]
    )
    founded_year = models.PositiveIntegerField()
    history = models.TextField()

    class Meta:
        verbose_name_plural = "Company Info"

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title 