from django.urls import path

from . import views

urlpatterns = [path("friendships/<int:pk>/", views.FriendshipView.as_view())]
