from app1.views import TodoListView, TodoCreateView, TodoUpdateView, TodoDeleteView
from django.urls import path

urlpatterns = [
    path('',TodoListView.as_view()),
    path('api/todo/',TodoListView.as_view()),
    path('api/todo/create/',TodoCreateView.as_view()),
    path('api/todo/update/<int:pk>',TodoUpdateView.as_view()),
    path('api/todo/delete/<int:pk>',TodoDeleteView.as_view()),
]
