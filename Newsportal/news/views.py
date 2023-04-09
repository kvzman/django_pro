from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin

from .forms import PostForm
from .models import Post, Category
from .filters import PostFilter

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.cache import cache
import logging


logger = logging.getLogger(__name__)
logger.info('INFO')


class PostList(ListView):
    model = Post
    ordering = 'post_time'
    template_name = 'post.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'one_post.html'
    context_object_name = 'one_post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_one_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class NewsCreate(PostCreate):

    def form_valid(self, form):
        post = form.save(commit=False)
        post.cat_type = 'NW'
        return super().form_valid(form)


class PostUpdate(UpdateView):
    permission_required = ('news.change_one_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class NewsUpdate(PostUpdate):

    def form_valid(self, form):
        post = form.save(commit=False)
        post.cat_type = 'NW'
        return super().form_valid(form)


class PostDelete(DeleteView):
    permission_required = ('news.delete_one_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class NewsDelete(PostDelete):

    def form_valid(self, form):
        post = form.save(commit=False)
        post.cat_type = 'NW'
        return super().form_valid(form)


class PostSearch(PostList):
    template_name = 'search.html'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-post_time')
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
    message = 'вы успешно подписались на рассылку по категории'
    return render(
        request,
        'subscribe.html',
        {'category': category, 'message': message},
    )
