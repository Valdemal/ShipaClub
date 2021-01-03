from django.urls import path
from .views import NewsIndexView, about, rules, allNews,NewsEditView, NewsDeleteView, NewsCreateView

app_name = 'main'

urlpatterns = [
    path('create/', NewsCreateView.as_view(), name='create'),
    path('delete/<int:pk>/',NewsDeleteView.as_view(), name='delete'),
    path('edit/<int:pk>/', NewsEditView.as_view(), name='edit'),
    path('allnews/', allNews, name='allnews'),
    path('', NewsIndexView.as_view(), name='index'),
    path('about/',about, name='about'),
    path('rules/', rules, name='rules')
]