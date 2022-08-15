from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from users.forms import (UserRegistrationForm, ProfileUpdateForm, UserUpdateForm, 
                         CustomPasswordResetForm, CustomSetPasswordForm)
from django.contrib import messages
from django.contrib.auth import logout, login
from users.utils.decorators import login_required
from users.token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from users.models import CustomUser
from users.utils.tasks import send_confirmation_email
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView


#Dashboard homepage
@login_required 
def dashboard(request):
    if request.user.confirmed == False:
        print('You are not confirmed')
        # pass
        return redirect('users-unconfirmed')
    return render(request, 'users/dashboard.html', {'title': 'User Dashboard'})

#Registration form
def register(request):
    if request.user.is_authenticated:
        return redirect('users-dashboard')
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Store form details in memory, not database
            user = form.save(commit=False)
            user.save()
            # Get the domain of the current site
            current_site = get_current_site(request)
            # Send confirmation mail to user
            user_email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            send_confirmation_email.delay('Confirm Your account', user_email, 
                                    'users/emails/confirm_email', 
                                    username=username, 
                                    domain=request.build_absolute_uri(current_site.domain),
                                    uid=urlsafe_base64_encode(force_bytes(user.pk)),
                                    token=account_activation_token.make_token(user))
            messages.success(request, 
                             message='Account created successfully!'
                             ' Please Confirm your account to complete the registration')
            return redirect('users-login')
    else:
        form = UserRegistrationForm()
    context = {
        'title': 'Register Page',
        'form': form
    }
    return render(request, 'users/register.html', context=context)
    
# Confirm account view
@login_required
def confirm_account(request, uidb64, token):
    #Check whether user has been confirmed
    if request.user.is_authenticated and request.user.confirmed:
        messages.info(request, "You have already confirmed your account")
        return redirect('users-landingpage')
    try:
        # Get userid from the token id
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.filter(pk=uid, email=request.user.email).first()
    except Exception as e:
        print(e)
        user = None
    # If there are no errors update the user status and save user
    if user is not None and account_activation_token.check_token(user, token):
        user.confirmed = True
        user.save()
        login(request, user)
        messages.success(request, "You have confirmed your account successfully.")
        return redirect('users-landingpage')
    else:
        messages.warning(request, "Token has expired or is invalid")
        return redirect('users-landingpage')
        
    
#Logout View
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully")
    return redirect('users-login')

# Landing page view
def landing_page(request):
    return render(request, 'users/landingpage.html', {'title': 'Landing Page'})

# Unconfirmed accounts
def unconfirmed_account(request):
    if request.user.is_anonymous or request.user.confirmed:
        return redirect('users-landingpage')
    return render(request, 'users/unconfirmed_account.html', {'title': 'Unconfirmed Account'})

# Resend confirmation emails
@login_required
def resend_confirmation(request):
    token = account_activation_token.make_token(request.user)
    # Get the domain of the current site
    current_site = get_current_site(request)
    send_confirmation_email.delay('Confirm Your account', request.user.email, 
                                    'users/emails/confirm_email', 
                                    username=request.user.username, 
                                    domain=request.build_absolute_uri(current_site.domain),
                                    uid=urlsafe_base64_encode(force_bytes(request.user.pk)),
                                    token=token)
    messages.success(request, "A new confirmation email has been sent to your email address.")
    return redirect('users-dashboard')

# Define profile view
@login_required
def user_profile(request):
    # Check whether form is a post route
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, 
                                   instance=request.user.profile)
        # Check for valid submission of forms
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your Profile has been updated successfully")
            return redirect('users-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'title': 'Profile Page',
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context=context)

# define a custom password reset view
class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_request.html'
    form_class = CustomPasswordResetForm
    extra_context = {
        'title': 'Password Reset Request'
    }
    email_template_name = 'users/emails/reset_password.html'
    html_email_template_name = 'users/emails/reset_password.html'
    subject_template_name = 'users/emails/reset_password_subject.txt'
    
    # Override form_valid
    def form_valid(self, form):
        messages.success(self.request, "Password Confirmation has been sent")
        return super().form_valid(form)

    
    success_url = reverse_lazy('users-password-reset-request')
    
# create a custom password reset confirm view
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    
    def form_valid(self, form):
        messages.success(self.request, f"Password has been reset successfully")
        return super().form_valid(form)    
    
    success_url = reverse_lazy('users-login')