from django.urls import path
from .views import (
   PostList, PostDetail, PostCreate, NewsCreate, PostUpdate, PostDelete, PostSearch, NewsDelete, NewsUpdate,
   CategoryListView, subscribe,
)

urlpatterns = [
   path('news/', PostList.as_view(), name='post_list'),
   path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/search/', PostSearch.as_view(), name='post_search'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
   path('news<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/create/', PostCreate.as_view(), name='post_create'),
   path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('articles<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]
