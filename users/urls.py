from django.urls import path
from users import views
from django.contrib.auth import views as auth_views
from users.forms import LoginForm 

#Register all urls of the main app
urlpatterns = [
    path('dashboard/', view=views.dashboard, name='users-dashboard'), 
    path('landing_page/', view=views.landing_page, name='users-landingpage'),
    path('auth/unconfirmed_account', view=views.unconfirmed_account, name='users-unconfirmed'),
    path('auth/resend_confirmation', view=views.resend_confirmation, name='users-resend-confirmation'),
    path('auth/register/', view=views.register, name='users-register'),
    path('auth/logout/', view=views.logout_view, name='users-logout'),
    path('profile/', view=views.user_profile, name='users-profile'),
    path('password-reset-request/', view=views.CustomPasswordResetView.as_view(), 
                                    name='users-password-reset-request'),
    path('password-reset-confirm/<uidb64>/<token>/', view=views.CustomPasswordResetConfirmView.as_view(), 
                                    name='password_reset_confirm'),
    path('auth/login/', view=auth_views.LoginView.as_view(template_name='users/login.html',
                                                          extra_context={'title':'Login'},
                                                          authentication_form=LoginForm,
                                                          redirect_authenticated_user=True),
                                                          name='users-login'),
    path('auth/confirm_account/<uidb64>/<token>/',
         view=views.confirm_account, name='users-confirm-account')
]