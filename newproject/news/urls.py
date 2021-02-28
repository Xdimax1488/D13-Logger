from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    path('', NewsList.as_view(), name='news'),
    path('<int:pk>', NewsDetail.as_view(), name='post'),
    path('search/', PostSearch.as_view(), name='search'),
    path('add/', PostCreate.as_view(), name='create_post'),

    path('edit/<int:pk>', PostUpdateView.as_view(), name='post_edit'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('category/<int:pk>', PostCategory.as_view(), name='category'),
    path('category/subscribe/', subscribe_category, name='subscribe'),
    path('category/unsubscribe/', unsubscribe_category, name='unsubscribe'),

]
