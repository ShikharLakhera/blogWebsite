from django import forms
from .models import BlogPost

class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title.strip()) < 4:
            raise forms.ValidationError("Title must be at least 4 characters long.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content and len(content.strip()) < 20:
            raise forms.ValidationError("Content must be at least 20 characters long.")
        return content
