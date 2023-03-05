"""BMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from application import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.IndexView.as_view(), name="index"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("createBike/", views.CreateBikeView.as_view(), name="createBike"),
    path("bikeList/", views.BikeListView.as_view(), name="bikeList"),
    path("borrow/", views.BorrowBikeView.as_view(), name="borrow"),
    path("borrow/<bikepk>", views.BorrowBikeView.as_view(), name="borrow"),
    path("userList/", views.UserListView.as_view(), name="user-view"),
    path("user/", views.UserListView.as_view(), name="user-view"), # dont change anything around the user-change, otherwise it gets messy
    path("user/<pk>", views.ChangeUserView.as_view(), name="user-change"),
]
