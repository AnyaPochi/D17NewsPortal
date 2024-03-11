from django.urls import path
# Импортируем созданные нами представления
from .views import (

   PostsList, PostDetail, PostsSearch, PostCreate, PostUpdate, PostDelete,CategoryListView,subscribe
)

urlpatterns = [
   path('', PostsList.as_view(), name = 'posts'),
   path('<int:pk>', PostDetail.as_view(),name='post'),
   path('search/', PostsSearch.as_view(), name='post_search'),
   path('create/', PostCreate.as_view(), name='news_create'),
   path('articles/create/', PostCreate.as_view(), name='article_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('articles/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   ]