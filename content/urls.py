from django.urls import path
from .views import add_post_view, one_post_view, like_view, liked_view, add_comment_view

app_name = 'account'

urlpatterns = [
    path('<int:id>/', one_post_view, name="one_post"),
    path('<int:id>/like/', like_view, name="like"),
    path('<int:id>/liked/', liked_view, name="liked"),
    path('add_post', add_post_view, name="add_post"),
    path('<int:id>/add_comment', add_comment_view, name="add_comment"),
]