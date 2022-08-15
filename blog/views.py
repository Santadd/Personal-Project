from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import Post, CustomLoginRequiredMixin, CustomUserPassesTestMixin
from blog.forms import PostForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect


# create Blog list View
class PostListView(ListView):
    model = Post
    template_name = 'blog/posts_list.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6
    
    
# create User Blog list View
class UserPostListView(CustomLoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/view_posts.html'
    context_object_name = 'posts'
    extra_context = {
        'title': 'My Blog Posts'
    }
    
    # override the get_query_set
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-date_posted')
    
    
# Create A detailed post view
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    extra_context = {
        'title': 'Blog Detail'
    }

class PostCreateView(CustomLoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    extra_context = {
        'title': 'Add Post',
        'header1': 'Create New Post',
        'header2': 'Add Post'
    }
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, f"New Post has been added successfully")
        return super().form_valid(form) 
    
    success_url = reverse_lazy('blog-userposts')
    

class PostUpdateView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    extra_context = {
        'title': 'Update Post',
        'header1': 'Update Post',
        'header2': 'Post Update'
    }
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, f"Post has been updated successfully")
        return super().form_valid(form) 
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
    success_url = reverse_lazy('blog-userposts')
    
class PostDeleteView(CustomLoginRequiredMixin, CustomUserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/view_posts.html'
    context_object_name = 'post'
    extra_context = {
        'title': 'Post Delete',
    }
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
    
    # Modify form valid(Add message upon deletion)
    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, f"Post has been deleted successfully")
        return HttpResponseRedirect(success_url)
    
    success_url = reverse_lazy('blog-userposts')