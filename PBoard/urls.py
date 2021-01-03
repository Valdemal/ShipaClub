from django.urls import path
from .views import index, PostCreateView, by_rubric, PostDeleteView, estimations, api_rubrics

app_name = 'pboard'

urlpatterns = [
    path('api/rubrics/', api_rubrics),
    path('estimations/', estimations, name='estimations'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='delete'),
    path('add/', PostCreateView.as_view(), name='add'),
    path('<str:rubric_name>/', by_rubric, name='by_rubric'),
    path('', index, name='index'),
]