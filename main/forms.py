from django import forms
from main.models import Post

class PostForm(forms.Form):
    content = forms.CharField(label='Content')
    def clean(self):
        content = self.cleaned_data.get('content')
        if len(str(content)) < 1:
            raise forms.ValidationError("Enter post!")
        elif len(str(content)) > 255:
            raise forms.ValidationError("Maximum of 255 characters allowed!")