
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView,DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Category
from .forms import PostForm
from datetime import datetime
from .filters import PostFilter
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404,render
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

class PostsList(ListView):
    queryset = Post.objects.order_by('-time_in')
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

class PostDetail(DetailView):
    queryset = Post.objects.order_by('-time_in')
    template_name = 'post.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

class PostsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset

        return context
class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/articles/create/':
            post.type = 'Статья'
        post.save()
        return super().form_valid(form)
class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')

class AddPost(PermissionRequiredMixin, PostCreate):
    permission_required = ('news.add_post',)

class ChangePost(PermissionRequiredMixin, PostUpdate):
    permission_required = ('news.change_post')


class CategoryListView(PostsList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context
@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'Вы подписали на рассылку новостей в категории'
    return render(request, 'subscribe.html', {'category':category,'message': message})
