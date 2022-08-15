from django.urls import path
from main import views

#Register all urls of the main app
urlpatterns = [
    path('', view=views.homepage, name='main-homepage'),
]