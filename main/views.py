from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Post

#Create Homepage
def homepage(request):
    #Query for Posts
    posts = Post.objects.all()
    context = {
        'title': 'Home',
        'posts': posts
    }
    return render(request, 'main/homepage.html', context=context) 