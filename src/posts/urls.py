from django.urls import path
from .views import (
    post_list_and_create,
)

app_name = 'posts'

# define urlpatters for posts > goes into main uri file
urlpatterns = [
    path('', post_list_and_create, name='main-board'),
]
