from django.urls import path

from .views import FindFriendsView, FriendshipCreateView, FriendshipDeleteView

app_name = "friendship"

urlpatterns = [
    path("friendship", FriendshipCreateView.as_view(), name="friendship_create"),
    path(
        "friendship/<int:uid1>/<int:uid2>",
        FriendshipDeleteView.as_view(),
        name="friendship_delete",
    ),
    path("friendship/<int:uid>", FindFriendsView.as_view(), name="find_friends"),
]
