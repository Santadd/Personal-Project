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

# Error 404 page
def error_404(request, exception):
    context = {
        'title': 'Error 404 Page'
    }
    return render(request, 'main/404.html', status=404, context=context)

# Error 500 page
def error_500(request):
    context = {
        'title': 'Error 500 Page'
    }
    return render(request, 'main/500.html', status=500, context=context)