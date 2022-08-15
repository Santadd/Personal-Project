from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
import os

# Create your models here.
class CustomUser(AbstractUser):
    confirmed = models.BooleanField(default=False)
 
    def __str__(self):
        return self.username


def save_profile_pic(image_path):
    img = Image.open(image_path)
    if img.height > 300 and img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(image_path)  
    return "Image Resize Completed"
  
# Create a User Profile Models
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(default='N/A')
    phone_no = models.CharField(default='N/A', max_length=120) 
    location = models.CharField(default='N/A', max_length=250)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    def __str__(self):
        return f"{self.user.username} Profile"
    
    # Overwrite the save method to reduce image size
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        #Resize the image
        save_profile_pic(self.image.path)
        