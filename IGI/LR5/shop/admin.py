from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import (
    User, ProductCategory, Product, Customer, Employee,
    Order, OrderItem, Promo, Review, CompanyInfo,
    Manufacturer, PickupPoint, News
)

# Register custom User model with admin site
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'role', 'phone', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

class ProductInline(admin.TabularInline):
    model = Product
    extra = 1

# Product categories management
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'products_count')
    search_fields = ('name',)
    inlines = [ProductInline]

    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Products Count'

# Order management with inline items
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('price_at_time',)

# Product management in admin interface
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available', 'manufacturer', 'show_image')
    list_filter = ('category', 'available', 'manufacturer')
    search_fields = ('name', 'description')
    readonly_fields = ('show_image',)

    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No image"
    show_image.short_description = 'Image'

# Customer profile management
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'birth_date', 'orders_count', 'total_spent')
    search_fields = ('user__username', 'phone_number')

    def orders_count(self, obj):
        return Order.objects.filter(customer=obj.user).count()
    orders_count.short_description = 'Orders Count'

    def total_spent(self, obj):
        total = Order.objects.filter(customer=obj.user).aggregate(
            total=models.Sum('total_amount')
        )['total']
        return total or 0
    total_spent.short_description = 'Total Spent'

# Employee management
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'phone_number', 'hire_date', 'orders_handled')
    search_fields = ('user__username', 'position', 'phone_number')

    def orders_handled(self, obj):
        return Order.objects.filter(employee=obj.user).count()
    orders_handled.short_description = 'Orders Handled'

# Order management
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'order_date', 'total_amount', 'employee')
    list_filter = ('status', 'order_date')
    search_fields = ('customer__username', 'employee__username')
    inlines = [OrderItemInline]
    readonly_fields = ('total_amount',)
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.price_at_time:  # Если цена не установлена
                instance.price_at_time = instance.product.price
            instance.save()
        formset.save_m2m()

# Promotional codes management
@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'valid_from', 'valid_to', 'is_active', 'usage_count')
    list_filter = ('is_active',)
    search_fields = ('code',)

    def usage_count(self, obj):
        return Order.objects.filter(promo=obj).count()
    usage_count.short_description = 'Times Used'

# Product reviews management
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('customer__user__username', 'product__name', 'comment')

# Manufacturer management
@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'products_count', 'created_at')
    search_fields = ('name', 'description')

    def products_count(self, obj):
        return Product.objects.filter(manufacturer=obj).count()
    products_count.short_description = 'Products Count'

# Pickup points management
@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    list_display = ('address', 'working_hours', 'phone', 'is_active', 'orders_count')
    list_filter = ('is_active',)
    search_fields = ('address', 'phone')

    def orders_count(self, obj):
        return Order.objects.filter(pickup_point=obj).count()
    orders_count.short_description = 'Orders Count'

# Company information management
@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'founded_year')
    search_fields = ('name', 'description', 'history')

# News management
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'content') 