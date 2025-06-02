from decimal import Decimal
from django.conf import settings
from .models import Product, Promo
from django.utils import timezone

class Cart:
    def __init__(self, request):
        """Инициализация корзины"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохраняем пустую корзину в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.promo_code = self.session.get('promo_code')

    def add(self, product, quantity=1, override_quantity=False):
        """Добавить продукт в корзину или обновить его количество"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Пометить сессию как измененную"""
        self.session.modified = True

    def remove(self, product):
        """Удалить продукт из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Перебор элементов в корзине и получение продуктов из базы данных"""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Подсчет всех товаров в корзине"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Подсчет стоимости товаров в корзине"""
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def get_total_items(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        """Очистка корзины"""
        del self.session[settings.CART_SESSION_ID]
        if 'promo_code' in self.session:
            del self.session['promo_code']
        self.save()

    def get_promo_discount(self):
        if not self.promo_code:
            return None

        try:
            promo = Promo.objects.get(
                code=self.promo_code,
                is_active=True,
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now()
            )
            total = self.get_total_price()
            discount_amount = (total * Decimal(promo.discount_percent) / 100).quantize(Decimal('0.01'))
            return {
                'code': promo.code,
                'discount_percent': promo.discount_percent,
                'discount_amount': discount_amount,
                'final_price': total - discount_amount
            }
        except Promo.DoesNotExist:
            if 'promo_code' in self.session:
                del self.session['promo_code']
            return None 