from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Product, UserProfile


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='Потребителско име',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Въведете потребителско име'})
    )
    email = forms.EmailField(
        label='Имейл адрес',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Въведете имейл адрес'})
    )
    password1 = forms.CharField(
        label='Парола',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Въведете парола'})
    )
    terms_accepted = forms.BooleanField(
        label='Съгласен/на съм с общите условия',
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Превод на помощните текстове
        self.fields['username'].help_text = 'Задължително. 150 символа или по-малко. Само букви, цифри и @/./+/-/_'
        self.fields['email'].help_text = 'Задължително. Ще получите имейл за потвърждение на регистрацията.'
        self.fields['password1'].help_text = 'Паролата трябва да съдържа поне 8 символа и не може да бъде изцяло цифрова.'
        # Премахване на валидацията за password2
        if 'password2' in self.fields:
            del self.fields['password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Потребител с това име вече съществува.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Потребител с този имейл адрес вече съществува.")
        return email


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Потребителско име',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Въведете потребителско име'})
    )
    password = forms.CharField(
        label='Парола',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Въведете парола'})
    )

    error_messages = {
        'invalid_login': "Моля, въведете правилно потребителско име и парола.",
        'inactive': "Този акаунт е неактивен.",
    }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'phone', 'babh_number', 'category', 'city', 'is_active']
        labels = {
            'title': 'Заглавие',
            'description': 'Описание',
            'price': 'Цена',
            'phone': 'Телефон за връзка',
            'babh_number': 'БАБХ номер (опция)',
            'category': 'Категория',
            'city': 'Населено място',
            'is_active': 'Активна обява',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Въведете заглавие'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'maxlength': '250', 'placeholder': 'Въведете описание'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Въведете цена'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Напр. 0888123456', 'maxlength': '20'}),
            'babh_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Напр. BG123456789', 'maxlength': '30'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'description': 'Максимум 250 символа',
            'price': 'Цена в евро',
            'phone': 'Телефонен номер за контакт (опционално)',
            'babh_number': 'Регистрационен номер в БАБХ (опционално)',
        }


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(
        label='Потребителско име',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Потребителско име'})
    )
    email = forms.EmailField(
        label='Email',
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email адрес'})
    )

    class Meta:
        model = UserProfile
        fields = ['profile_image']
        labels = {
            'profile_image': 'Профилна снимка',
        }
        widgets = {
            'profile_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.username = self.cleaned_data['username']
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save()
                profile.save()
        return profile


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Стара парола',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Въведете стара парола'})
    )
    new_password1 = forms.CharField(
        label='Нова парола',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Въведете нова парола'})
    )
    new_password2 = forms.CharField(
        label='Потвърдете новата парола',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Въведете отново новата парола'})
    )

    error_messages = {
        'password_mismatch': 'Двете пароли не съвпадат.',
        'password_incorrect': 'Старата парола е грешна.',
    }


class DeleteAccountForm(forms.Form):
    confirm = forms.BooleanField(
        label='Потвърждавам, че искам да изтрия акаунта си',
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    password = forms.CharField(
        label='Парола за потвърждение',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Въведете паролата си'})
    )


class ContactForm(forms.Form):
    email = forms.EmailField(
        label='Email за обратна връзка',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Въведете вашия email'})
    )
    content = forms.CharField(
        label='Съдържание',
        max_length=250,
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'maxlength': '250', 'placeholder': 'Въведете вашето съобщение'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].help_text = 'Максимум 250 символа'
