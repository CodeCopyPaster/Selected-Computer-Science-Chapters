from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import date
from dateutil.relativedelta import relativedelta
from .models import User, Product, Order, OrderItem

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(
        max_length=20,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^\+375 \((?:29|33|44|25)\) [0-9]{3}-[0-9]{2}-[0-9]{2}$',
                message="Номер телефона должен быть в формате: '+375 (29) XXX-XX-XX'"
            )
        ],
        widget=forms.TextInput(attrs={'placeholder': '+375 (29) XXX-XX-XX', 'class': 'form-control'})
    )
    address = forms.CharField(max_length=255, required=False, label='Адрес',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    birth_date = forms.DateField(
        required=True,
        label='Дата рождения',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'max': date.today().isoformat()
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone', 'address', 'birth_date')

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            age = relativedelta(timezone.now().date(), birth_date).years
            if age < 18:
                raise forms.ValidationError('Вы должны быть старше 18 лет для регистрации.')
        return birth_date

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'manufacturer', 'image', 'available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['pickup_point', 'promo']
        widgets = {
            'pickup_point': forms.Select(attrs={'class': 'form-control'}),
            'promo': forms.Select(attrs={'class': 'form-control'}),
        }

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1}),
        }

class OrderManagementForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class PromoCodeForm(forms.Form):
    code = forms.CharField(max_length=50, required=True)

class EmployeeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'position', 'phone', 'address']
        widgets = {
            'position': forms.TextInput(attrs={'placeholder': 'Например: Менеджер'}),
            'phone': forms.TextInput(attrs={'placeholder': '+375 (XX) XXX-XX-XX'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if not user.role:
            user.role = User.EMPLOYEE
        if commit:
            user.save()
        return user 