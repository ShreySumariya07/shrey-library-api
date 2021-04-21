from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.SignUpView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('bookListAdd/', views.BooksView.as_view()),
    path('bookDetail/<int:book_id>/', views.BookView.as_view())
]
