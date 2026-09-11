from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Коментар'
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Ваш коментар...', 'maxlength': 500})
        }

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text:
            if len(text) > 500:
                raise ValidationError('Максимальна довжина коментаря — 500 символів.')
            if text != strip_tags(text):
                raise ValidationError('HTML теги заборонені в коментарях.')
        return text
