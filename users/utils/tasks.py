from django.core.mail import send_mail
from django.template.loader import render_to_string
from myproject.settings import EMAIL_HOST_USER
from celery import shared_task
from PIL import Image
from django.contrib.auth.forms import PasswordResetForm
from users.models import CustomUser

@shared_task
def send_confirmation_email(subject, to, template, **kwargs):
    #Create a text and html message for the email
    msg_text = render_to_string(template + '.txt', context={**kwargs})
    msg_html = render_to_string(template + '.html', context={**kwargs})
    
    #Send email to user
    send_mail(subject=subject, message=msg_text, from_email=EMAIL_HOST_USER,
              recipient_list=[to], html_message=msg_html)
    
    return "Done"

# Function to save profile image(Reducing Image sizes)
# @shared_task
def save_profile_pic(image_path):
    img = Image.open(image_path)
    if img.height > 300 and img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(image_path)  
    return "Image Resize Completed"

@shared_task
def password_reset_email(subject_template_name, email_template_name, context,
              from_email, to_email, html_email_template_name):
    # print(type(args[3]['user']))
    context['user'] = CustomUser.objects.get(pk=context['user'])
    PasswordResetForm.send_mail(None,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name)
    return "Done"