from . import views
from django.urls import path

urlpatterns = [
    path('dashboard/', views.ArticlesListView.as_view(), name='admin_articles')
]
