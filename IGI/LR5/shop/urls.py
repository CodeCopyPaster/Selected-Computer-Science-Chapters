from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Customer URLs
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('profile/fill/', views.fill_profile, name='fill_profile'),
    path('orders/', views.order_list, name='order_list'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('order/new/', views.place_order, name='place_order'),
    
    # Employee URLs
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('employee/orders/', views.employee_order_list, name='employee_order_list'),
    path('employee/order/<int:order_id>/', views.order_management, name='order_management'),
    path('employee/customers/', views.employee_customer_list, name='employee_customer_list'),
    
    # Management URLs (previously Admin URLs)
    path('management/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('management/products/', views.admin_product_list, name='admin_product_list'),
    path('management/products/add/', views.admin_product_add, name='admin_product_add'),
    path('management/products/<int:pk>/edit/', views.admin_product_edit, name='admin_product_edit'),
    path('management/products/<int:pk>/delete/', views.admin_product_delete, name='admin_product_delete'),
    path('management/categories/', views.admin_category_list, name='admin_category_list'),
    path('management/categories/add/', views.admin_category_add, name='admin_category_add'),
    path('management/categories/<int:pk>/edit/', views.admin_category_edit, name='admin_category_edit'),
    path('management/categories/<int:pk>/delete/', views.admin_category_delete, name='admin_category_delete'),
    path('management/manufacturers/', views.admin_manufacturer_list, name='admin_manufacturer_list'),
    path('management/manufacturers/add/', views.admin_manufacturer_add, name='admin_manufacturer_add'),
    path('management/manufacturers/<int:pk>/edit/', views.admin_manufacturer_edit, name='admin_manufacturer_edit'),
    path('management/manufacturers/<int:pk>/delete/', views.admin_manufacturer_delete, name='admin_manufacturer_delete'),
    path('management/orders/', views.admin_order_list, name='admin_order_list'),
    path('management/orders/<int:pk>/', views.admin_order_detail, name='admin_order_detail'),
    path('management/orders/<int:pk>/cancel/', views.admin_order_cancel, name='admin_order_cancel'),
    path('management/customers/', views.admin_customer_list, name='admin_customer_list'),
    path('management/employees/', views.admin_employee_list, name='admin_employee_list'),
    path('management/employees/add/', views.admin_employee_add, name='admin_employee_add'),
    path('management/employees/<int:pk>/edit/', views.admin_employee_edit, name='admin_employee_edit'),
    path('management/employees/<int:pk>/toggle-status/', views.admin_employee_toggle_status, name='admin_employee_toggle_status'),
    path('management/reviews/', views.admin_review_list, name='admin_review_list'),
    path('management/promos/', views.admin_promo_list, name='admin_promo_list'),
    path('management/promos/add/', views.admin_promo_add, name='admin_promo_add'),
    path('management/promos/<int:pk>/edit/', views.admin_promo_edit, name='admin_promo_edit'),
    path('management/stats/sales/', views.admin_sales_stats, name='admin_sales_stats'),
    path('management/stats/products/', views.admin_product_stats, name='admin_product_stats'),
    path('management/stats/customers/', views.admin_customer_stats, name='admin_customer_stats'),
    path('management/stats/delivery/', views.admin_delivery_stats, name='admin_delivery_stats'),
    
    # Cart URLs
    path('cart/', views.cart_detail, name='cart'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    
    # Information pages
    path('glossary/', views.glossary, name='glossary'),
    path('privacy/', views.privacy, name='privacy'),
    
    # Public URLs
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('reviews/', views.reviews, name='reviews'),
    path('promotions/', views.promotions, name='promotions'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('category/<int:pk>/', views.category_products, name='category_products'),
    path('manufacturer/<int:pk>/', views.manufacturer_products, name='manufacturer_products'),
    path('promo/apply/', views.apply_promo, name='apply_promo'),
    path('pickup-points/', views.pickup_points_list, name='pickup_points'),
    
    # Reviews
    path('product/<int:product_id>/add_review/', views.add_review, name='add_review'),
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
] 