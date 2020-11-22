import json
from unittest import mock

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from rest_framework import status
from rest_framework.test import APIRequestFactory

from friendship.models import Friendship
from friendship.views import FriendshipDeleteView


class RemoveFriendTest(TestCase):
    def setUp(self) -> None:
        self.friendship_data = {"first_friend": 126785, "second_friend": 3252332515}

        self.friendship = Friendship.objects.create(**self.friendship_data)

    def test_remove_friendship(self):
        factory = APIRequestFactory()
        friendship_view = FriendshipDeleteView.as_view()
        request = factory.delete(
            reverse(
                "friendship:friendship_delete",
                args=(
                    self.friendship_data["first_friend"],
                    self.friendship_data["second_friend"],
                ),
            ),
            content_type="application/json",
        )
        response = friendship_view(
            request,
            uid1=self.friendship_data["first_friend"],
            uid2=self.friendship_data["second_friend"],
        )
        response.render()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(ObjectDoesNotExist):
            Friendship.objects.get(
                first_friend=self.friendship_data["first_friend"],
                second_friend=self.friendship_data["second_friend"],
            )

    def test_remove_friendship_with_swapped_UIDS(self):
        friendship_data_swapped = {
            "first_friend": self.friendship_data["second_friend"],
            "second_friend": self.friendship_data["first_friend"],
        }
        factory = APIRequestFactory()
        friendship_view = FriendshipDeleteView.as_view()
        request = factory.delete(
            reverse(
                "friendship:friendship_delete",
                args=(
                    self.friendship_data["first_friend"],
                    self.friendship_data["second_friend"],
                ),
            ),
            content_type="application/json",
        )
        response = friendship_view(
            request,
            uid1=self.friendship_data["first_friend"],
            uid2=self.friendship_data["second_friend"],
        )
        response.render()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(ObjectDoesNotExist):
            Friendship.objects.get(
                first_friend=self.friendship_data["first_friend"],
                second_friend=self.friendship_data["second_friend"],
            )

    def test_remove_non_existent_friendship(self):
        friendship_data = {"first_friend": 126785, "second_friend": 32523325151}
        factory = APIRequestFactory()
        friendship_view = FriendshipDeleteView.as_view()
        request = factory.delete(
            reverse(
                "friendship:friendship_delete",
                args=(
                    friendship_data["first_friend"],
                    friendship_data["second_friend"],
                ),
            ),
            content_type="application/json",
        )
        response = friendship_view(
            request,
            uid1=friendship_data["first_friend"],
            uid2=friendship_data["second_friend"],
        )
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with self.assertRaises(ObjectDoesNotExist):
            Friendship.objects.get(
                first_friend=friendship_data["first_friend"],
                second_friend=friendship_data["second_friend"],
            )

    # testing only one variant validation, to check if validation working
    def test_remove_friendship_with_negative_UIDs(self):
        friendship_data = {"first_friend": -23, "second_friend": -12}

        factory = APIRequestFactory()
        friendship_view = FriendshipDeleteView.as_view()
        with self.assertRaises(NoReverseMatch):
            request = factory.delete(
                reverse(
                    "friendship:friendship_delete",
                    args=(
                        friendship_data["first_friend"],
                        friendship_data["second_friend"],
                    ),
                ),
                content_type="application/json",
            )

    def test_remove_friendship_with_negative_UIDs_hard_code(self):
        friendship_data = {"first_friend": -23, "second_friend": -12}

        factory = APIRequestFactory()
        friendship_view = FriendshipDeleteView.as_view()
        request = factory.delete(
            "api/friendship/-12532/-23523",
            content_type="application/json",
        )
        response = friendship_view(
            request,
            uid1=friendship_data["first_friend"],
            uid2=friendship_data["second_friend"],
        )
        response.render()

        should_response = {
            "first_friend": ["Ensure UID is any non-negative integer number"],
            "second_friend": ["Ensure UID is any non-negative integer number"],
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), should_response)
        self.assertEqual(response["content-type"], "application/json")

    @mock.patch("friendship.models.Friendship.objects")
    def test_remove_friendship_if_db_return_many_objects(self, mock_friendships):
        # should not happened because first_friend and second_friend have unique constraint
        mock_friendships.get.side_effect = Friendship.MultipleObjectsReturned()
        mock_friendships.filter.return_value.delete.return_value = 1

        friendship_data = {"first_friend": 126785, "second_friend": 32523325151}
        factory = APIRequestFactory()
        friendship_view = FriendshipDeleteView.as_view()
        request = factory.delete(
            reverse(
                "friendship:friendship_delete",
                args=(
                    friendship_data["first_friend"],
                    friendship_data["second_friend"],
                ),
            ),
            content_type="application/json",
        )
        response = friendship_view(
            request,
            uid1=friendship_data["first_friend"],
            uid2=friendship_data["second_friend"],
        )
        response.render()

        self.assertTrue(mock_friendships.filter.return_value.delete.called)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
