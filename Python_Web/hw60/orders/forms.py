from django import forms
from django.contrib.auth.models import User
from .models import Order

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Email")
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Підтвердження паролю")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        labels = {
            'username': 'Ім\'я користувача (логин)',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Це ім'я користувача вже зайняте.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Цей email вже зареєстрований.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Паролі не співпадають.")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label="Ім'я користувача")
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")


class OrderBriefForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['project_name', 'project_type', 'budget', 'timeline', 'contacts', 'description']
        widgets = {
            'project_name': forms.TextInput(attrs={'placeholder': 'наприклад, Crypto Swapper Bot'}),
            'budget': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'наприклад, 500.00'}),
            'timeline': forms.TextInput(attrs={'placeholder': 'наприклад, 2 тижні'}),
            'contacts': forms.TextInput(attrs={'placeholder': 'Telegram: @username, або email/телефон'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Опишіть детально ваше технічне завдання...'}),
        }

    def clean_budget(self):
        budget = self.cleaned_data.get('budget')
        if budget is None or budget <= 0:
            raise forms.ValidationError("Бюджет повинен бути більшим за 0 USD.")
        return budget

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description or len(description.strip()) < 20:
            raise forms.ValidationError("Будь ласка, введіть детальніший опис проекту (щонайменше 20 символів).")
        return description

    def clean_contacts(self):
        contacts = self.cleaned_data.get('contacts')
        if not contacts or len(contacts.strip()) < 5:
            raise forms.ValidationError("Вкажіть коректні контакти для зв'язку (мінімум 5 символів).")
        return contacts


from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(attrs={'class': 'terminal-input'}),
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напишіть ваші враження від співпраці...', 'class': 'terminal-input'}),
        }

