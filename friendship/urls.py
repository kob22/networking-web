from django.urls import path

from .views import add_friendship, find_friends, remove_friendship

app_name = "friendship"

urlpatterns = [
    path("add_friendship/", add_friendship, name="add_friendship"),
    path("remove_friendship/", remove_friendship, name="remove_friendship"),
    path("find_friends/<int:uid>/", find_friends, name="find_friends"),
]
