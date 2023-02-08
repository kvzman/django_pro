from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin

from .forms import PostForm
from .models import Post
from .filters import PostFilter


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
