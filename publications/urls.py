from django.urls import path
from . import views

urlpatterns = [
    path("publication/", views.PublicationView.as_view()),
    path("publication/<int:pk>/", views.PublicationDetailView.as_view()),
    path("comment/<int:pk>/", views.CommentView.as_view()),
    path("comment/RUD/<int:pk>/", views.CommentDetailView.as_view()),
]