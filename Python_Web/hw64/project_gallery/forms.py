from django import forms
from .models import Project, ProjectGallery
from .validators import validate_image_security_and_dimensions

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        
        for file in result:
            if file:
                validate_image_security_and_dimensions(file)
                
        return result

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ProjectGalleryForm(forms.Form):
    images = MultipleFileField(label='Select images', required=False, widget=MultipleFileInput(attrs={'class': 'form-control'}))

class AddImagesForm(forms.Form):
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        label="Оберіть проєкт",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    images = MultipleFileField(
        label='Оберіть зображення',
        required=True,
        widget=MultipleFileInput(attrs={'class': 'form-control'})
    )
