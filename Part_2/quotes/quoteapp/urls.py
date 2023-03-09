from django.urls import path
from . import views

app_name = 'quoteapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('author/', views.author, name='author'),
    path('quote/', views.quote, name='quote'),
    path('tag/', views.tag, name='tag'),
    path('detail/<int:quote_id>', views.detail, name='detail'),
    path('find_author/<int:author_id>', views.find_author, name='find_author'),
]