from django.urls import path

from . import views

urlpatterns = [path("followers/<int:user_follow_id>/", views.FollowerView.as_view())]
