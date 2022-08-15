from django import forms
from users.models import CustomUser, Profile
from django.contrib.auth.forms import (UserCreationForm, PasswordResetForm, 
                                       SetPasswordForm, AuthenticationForm)
from users.utils.tasks import password_reset_email
from django.contrib import messages


#Create User Registration Form
class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='', help_text='',
                               widget=forms.TextInput(
                                attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(label='', help_text='',
                               widget=forms.EmailInput(
                                attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(label='', help_text='',
                               widget=forms.PasswordInput(
                                attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='', help_text='',
                               widget=forms.PasswordInput(
                                attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        #Check for existing user email
        user = CustomUser.objects.filter(email=email).first()
        if user is not None:
            raise forms.ValidationError('Email already exists') 
        return email
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Username'}))
    password = forms.CharField(label='',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}))
    
# User Update Form
class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='',
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control form-control-line', 
                                            'placeholder':'First Name'
                                            }))
    last_name = forms.CharField(label='',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control form-control-line', 
                                           'placeholder':'Last Name'
                                           }))
    username = forms.CharField(label='',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control form-control-line', 
                                           'placeholder':'Username'
                                           }))
    email = forms.EmailField(label='',
                            widget=forms.EmailInput(
                                attrs={'class': 'form-control form-control-line'
                                       , 'placeholder':'Email'
                                       }))
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email']
       
       
# Profile Update Form 
class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField()
    bio = forms.CharField(label='',
                          widget=forms.Textarea(
                              attrs={'class': 'form-control form-control-line', 
                                     'placeholder':'Enter Bio',
                                     'rows': '5'
                                     }))
    phone_no = forms.CharField(label='',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control form-control-line', 
                                          'placeholder':'Mobile Number'
                                          }))
    location = forms.CharField(label='',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control form-control-line', 
                                          'placeholder':'Location'
                                          }))
    
    class Meta:
        model = Profile
        fields = ['phone_no', 'location', 'bio', 'image']
        
# Custom Password Reset Form
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.CharField(label='',
                            widget=forms.EmailInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Enter email address'
                            }))
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_email = CustomUser.objects.filter(email=email).first()
        if user_email is None:
            raise forms.ValidationError('Email cannot be found')
        return email
    
    def send_mail(self, subject_template_name, email_template_name, context, 
                  from_email, to_email, html_email_template_name=None):
        context['user'] = context['user'].id
        password_reset_email.delay(subject_template_name=subject_template_name,
                        email_template_name=email_template_name,
                        context=context, from_email=from_email, to_email=to_email,
                        html_email_template_name=html_email_template_name)
        
    

    
# Custom Password Reset Form
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='',
                            widget=forms.PasswordInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Enter new password'
                            }))
    new_password2 = forms.CharField(label='',
                            widget=forms.PasswordInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Confirm Password'
                            }))
    
    def clean_new_password2(self):
        return super().clean_new_password2()
    
    
    