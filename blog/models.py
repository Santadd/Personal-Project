from django.db import models
from django.utils import timezone
from users.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

# Create a Custom Login Required Mixin
class CustomLoginRequiredMixin(LoginRequiredMixin):
    """The LoginRequiredMixin extended to add a relevant message to the
        messages framework by setting the ``permission_denied_message``
        attribute."""
    
    permission_denied_message = "Please log in to access this page"
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.WARNING, self.permission_denied_message)
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
# Create a Custom User Passes Test Mixin
class CustomUserPassesTestMixin(UserPassesTestMixin):
    pass

#Create a blog post model
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    
