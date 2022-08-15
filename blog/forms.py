from django import forms
from blog.models import Post

# Create Post Form
class PostForm(forms.ModelForm):
    title = forms.CharField(label='',
                            widget=forms.TextInput(attrs={
                                'class': 'form-control', 'placeholder': 'Enter Title'
                            }))
    content = forms.CharField(label='',
                            widget=forms.Textarea(attrs={
                                'class': 'form-control', 
                                'placeholder': 'Enter Content',
                                'rows': '5'
                            }))
    
    
    class Meta:
        model = Post
        fields = ['title', 'content']