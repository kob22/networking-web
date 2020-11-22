import json

from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory

from friendship.models import Friendship
from friendship.views import FriendshipCreateView


class AddFriendTest(TestCase):
    def test_add_friendship(self):
        friendship_data = {"first_friend": 6785, "second_friend": 2332515}
        factory = APIRequestFactory()
        friendship_view = FriendshipCreateView.as_view()
        request = factory.post(
            reverse("friendship:friendship_create"),
            json.dumps(friendship_data),
            content_type="application/json",
        )
        response = friendship_view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), friendship_data)
        self.assertEqual(response["content-type"], "application/json")

        friendship = Friendship.objects.filter(
            first_friend=friendship_data["first_friend"],
            second_friend=friendship_data["second_friend"],
        ).first()

        self.assertEqual(friendship.first_friend, friendship_data["first_friend"])
        self.assertEqual(friendship.second_friend, friendship_data["second_friend"])

    def test_add_friendship_with_invalid_UID(self):
        friendship_data = {"first_friend": "A", "second_friend": "Fasfa"}
        factory = APIRequestFactory()
        friendship_view = FriendshipCreateView.as_view()
        request = factory.post(
            reverse("friendship:friendship_create"),
            json.dumps(friendship_data),
            content_type="application/json",
        )
        response = friendship_view(request)
        response.render()

        should_response = {
            "first_friend": ["Ensure UID is any non-negative integer number"],
            "second_friend": ["Ensure UID is any non-negative integer number"],
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), should_response)
        self.assertEqual(response["content-type"], "application/json")

    def test_add_friendship_with_negative_UID(self):
        friendship_data = {"first_friend": -23, "second_friend": -12}
        factory = APIRequestFactory()
        friendship_view = FriendshipCreateView.as_view()
        request = factory.post(
            reverse("friendship:friendship_create"),
            json.dumps(friendship_data),
            content_type="application/json",
        )
        response = friendship_view(request)
        response.render()

        should_response = {
            "first_friend": ["Ensure UID is any non-negative integer number"],
            "second_friend": ["Ensure UID is any non-negative integer number"],
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), should_response)
        self.assertEqual(response["content-type"], "application/json")

    def test_add_friendship_without_whole_data(self):
        friendship_data = {"first_frienad": 6785, "second_frienda": 2332515}
        factory = APIRequestFactory()
        friendship_view = FriendshipCreateView.as_view()
        request = factory.post(
            reverse("friendship:friendship_create"),
            json.dumps(friendship_data),
            content_type="application/json",
        )
        response = friendship_view(request)
        response.render()

        should_response = {
            "first_friend": ["This field is required."],
            "second_friend": ["This field is required."],
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), should_response)
        self.assertEqual(response["content-type"], "application/json")

    def test_add_friendship_with_additiona_attr(self):
        friendship_data = {
            "first_friend": 6785,
            "second_friend": 2332515,
            "third_friend": 12421,
        }
        factory = APIRequestFactory()
        friendship_view = FriendshipCreateView.as_view()
        request = factory.post(
            reverse("friendship:friendship_create"),
            json.dumps(friendship_data),
            content_type="application/json",
        )
        response = friendship_view(request)
        response.render()

        friendship_data.pop("third_friend", None)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), friendship_data)
        self.assertEqual(response["content-type"], "application/json")

        friendship = Friendship.objects.filter(
            first_friend=friendship_data["first_friend"],
            second_friend=friendship_data["second_friend"],
        ).first()

        self.assertEqual(friendship.first_friend, friendship_data["first_friend"])
        self.assertEqual(friendship.second_friend, friendship_data["second_friend"])

    def test_add_many_friendship(self):
        friendship_data = [
            {"first_friend": 6785, "second_friend": 2332515},
            {"first_friend": 67285, "second_friend": 23325115},
        ]
        factory = APIRequestFactory()
        friendship_view = FriendshipCreateView.as_view()
        request = factory.post(
            reverse("friendship:friendship_create"),
            json.dumps(friendship_data),
            content_type="application/json",
        )
        response = friendship_view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {
                "non_field_errors": [
                    "Invalid data. Expected a dictionary, but got list."
                ]
            },
        )
        self.assertEqual(response["content-type"], "application/json")


class AddFriendIfExistsTest(TransactionTestCase):
    def test_add_friendship_when_already_exists(self):
        friendship_data = {"first_friend": 6785, "second_friend": 2332515}

        friendship = Friendship.objects.create(**friendship_data)

        factory = APIRequestFactory()
        friendship_view = FriendshipCreateView.as_view()
        request = factory.post(
            reverse("friendship:friendship_create"),
            json.dumps(friendship_data),
            content_type="application/json",
        )
        response = friendship_view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), friendship_data)
        self.assertEqual(response["content-type"], "application/json")

        friendship = Friendship.objects.filter(
            first_friend=friendship_data["first_friend"],
            second_friend=friendship_data["second_friend"],
        ).first()

        self.assertEqual(friendship.first_friend, friendship_data["first_friend"])
        self.assertEqual(friendship.second_friend, friendship_data["second_friend"])

    def test_add_friendship_when_already_exists_with_diff_id_order(self):
        friendship_data_swap = {"first_friend": 2332515, "second_friend": 6785}
        friendship_data = {"first_friend": 6785, "second_friend": 2332515}
        friendship = Friendship.objects.create(**friendship_data)

        factory = APIRequestFactory()
        friendship_view = FriendshipCreateView.as_view()
        request = factory.post(
            reverse("friendship:friendship_create"),
            json.dumps(friendship_data_swap),
            content_type="application/json",
        )
        response = friendship_view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), friendship_data)
        self.assertEqual(response["content-type"], "application/json")

        friendship = Friendship.objects.filter(
            first_friend=friendship_data["first_friend"],
            second_friend=friendship_data["second_friend"],
        ).first()

        self.assertEqual(friendship.first_friend, friendship_data["first_friend"])
        self.assertEqual(friendship.second_friend, friendship_data["second_friend"])
