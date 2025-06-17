from django import forms
from .models import Contact
from blogHome.models import BlogPost
from django.contrib import messages

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'content']

class CreateBlog(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        errors = []
        
        if title and len(title) < 3:
            errors.append("Title must be at least 3 characters long.")
        
        if content and len(content) < 20:
            errors.append("Content must be at least 20 characters long.")
                    
        if errors:
            raise forms.ValidationError(errors)
        
        return cleaned_data
