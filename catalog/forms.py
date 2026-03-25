from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Product, UserProfile


class CustomUserCreationForm(UserCreationForm):
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
        fields = ['email', 'password1']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].help_text = 'Ще получите имейл за потвърждение на регистрацията.'
        self.fields['password1'].help_text = 'Минимум 6 символа.'
        # Премахване на полето за потвърждение на паролата
        if 'password2' in self.fields:
            del self.fields['password2']

    def _generate_username_from_email(self, email):
        """Генерира уникално потребителско име от имейл адрес"""
        import re
        # Вземи частта преди @
        base_username = email.split('@')[0]
        # Замени специални символи с _
        base_username = re.sub(r'[^a-zA-Z0-9_]', '_', base_username)
        # Ограничи до 30 символа
        base_username = base_username[:30]
        
        # Провери дали username съществува
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            # Добави номер ако съществува
            username = f"{base_username}_{counter}"
            counter += 1
            # Ограничи до 150 символа (максимум за Django username)
            if len(username) > 150:
                username = username[:150]
        
        return username

    def clean(self):
        """Валидира данните без password2"""
        cleaned_data = forms.Form.clean(self)
        return cleaned_data

    def _post_clean(self):
        """Валидира паролата без password2"""
        forms.Form._post_clean(self)
        password = self.cleaned_data.get('password1')
        if password:
            try:
                from django.contrib.auth.password_validation import validate_password
                validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password1', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email')
        # Автоматично генерирай username от email
        user.username = self._generate_username_from_email(email)
        user.email = email
        if commit:
            user.save()
        return user

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
    sells_to = forms.MultipleChoiceField(
        choices=Product.SELLS_TO_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label='Продава на'
    )
    
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'phone', 'messenger_link', 'babh_number', 'category', 'city', 'seller_type', 'sells_to', 'is_active']
        labels = {
            'title': 'Заглавие',
            'description': 'Описание',
            'price': 'Цена',
            'phone': 'Телефон за връзка',
            'messenger_link': 'Messenger линк (опция)',
            'babh_number': 'БАБХ номер (опция)',
            'category': 'Категория',
            'city': 'Населено място',
            'seller_type': 'Тип продавач',
            'is_active': 'Активна обява',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Въведете заглавие'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'maxlength': '2000', 'placeholder': 'Въведете описание'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Въведете цена'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Напр. 0888123456', 'maxlength': '20'}),
            'messenger_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://m.me/xxxxxxx', 'maxlength': '300'}),
            'babh_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Напр. BG123456789', 'maxlength': '30'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'seller_type': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'description': 'Максимум 2000 символа',
            'price': 'Цена в € (евро)',
            'phone': 'Телефонен номер за контакт (опционално)',
            'messenger_link': 'Отворете Messenger → Вашият профил → Три точки (⋮) → "Копирай линк" (опционално)',
            'babh_number': 'Регистрационен номер в БАБХ (опционално)',
            'seller_type': 'Изберете типа на продавача',
            'sells_to': 'Изберете на кого продавате (може да изберете повече от едно)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.sells_to:
            self.fields['sells_to'].initial = self.instance.sells_to
        
        # Подобри текста на празната опция за seller_type
        self.fields['seller_type'].empty_label = 'Избери тип продавач'
    
    def clean_title(self):
        """Валидира заглавието за опасно съдържание"""
        title = self.cleaned_data.get('title', '')
        
        # Проверка за HTML тагове
        if '<' in title or '>' in title:
            raise forms.ValidationError('Заглавието не може да съдържа HTML тагове')
        
        # Проверка за скриптове
        dangerous_patterns = ['<script', 'javascript:', 'onerror=', 'onclick=']
        title_lower = title.lower()
        for pattern in dangerous_patterns:
            if pattern in title_lower:
                raise forms.ValidationError('Заглавието съдържа неразрешено съдържание')
        
        return title.strip()
    
    def clean_description(self):
        """Валидира описанието за опасно съдържание"""
        description = self.cleaned_data.get('description', '')
        
        # Проверка за дължина
        if len(description) > 2000:
            raise forms.ValidationError(f'Описанието трябва да е максимум 2000 символа. Вашето е {len(description)} символа.')
        
        # Проверка за HTML тагове (позволяваме емоджи)
        if '<' in description or '>' in description:
            raise forms.ValidationError('Описанието не може да съдържа HTML тагове')
        
        # Проверка за скриптове
        dangerous_patterns = ['<script', 'javascript:', 'onerror=', 'onclick=', '<iframe']
        description_lower = description.lower()
        for pattern in dangerous_patterns:
            if pattern in description_lower:
                raise forms.ValidationError('Описанието съдържа неразрешено съдържание')
        
        return description.strip()
    
    def clean_phone(self):
        """Валидира телефонния номер"""
        phone = self.cleaned_data.get('phone', '')
        if not phone:
            return phone
        
        # Премахваме интервали и тирета
        phone = phone.replace(' ', '').replace('-', '')
        
        # Проверка за HTML/JavaScript
        if '<' in phone or '>' in phone or 'script' in phone.lower():
            raise forms.ValidationError('Невалиден телефонен номер')
        
        return phone
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Конвертираме sells_to в списък ако не е
        sells_to = self.cleaned_data.get('sells_to')
        if isinstance(sells_to, list):
            instance.sells_to = sells_to
        else:
            instance.sells_to = list(sells_to) if sells_to else []
        
        if commit:
            instance.save()
        return instance


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
