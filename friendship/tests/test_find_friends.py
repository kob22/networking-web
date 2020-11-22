import json

from django.db import IntegrityError
from django.test import TransactionTestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from rest_framework import status
from rest_framework.test import APIRequestFactory

from friendship.models import Friendship
from friendship.views import FindFriendsView


class FindFriendsTest(TransactionTestCase):
    def setUp(self) -> None:
        for c in range(2555, 2705, 10):
            try:
                Friendship.objects.create(first_friend=15, second_friend=c)
            except IntegrityError:
                pass
        for c in range(2455, 2805, 20):
            try:
                Friendship.objects.create(first_friend=c, second_friend=10)
            except IntegrityError:
                pass

    def test_find_friends_for_non_existing_UID(self):

        factory = APIRequestFactory()
        friendship_view = FindFriendsView.as_view()
        request = factory.get(reverse("friendship:find_friends", args=(252154152,)))
        response = friendship_view(request, uid=252154152)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {"friends": []})
        self.assertEqual(response["content-type"], "application/json")

    def test_find_friends_for_existing_UID(self):

        factory = APIRequestFactory()
        friendship_view = FindFriendsView.as_view()
        request = factory.get(reverse("friendship:find_friends", args=(15,)))
        response = friendship_view(request, uid=15)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(
            json.loads(response.content),
            {"friends": [x for x in range(2555, 2705, 10)]},
        )
        self.assertEqual(response["content-type"], "application/json")

        friendship_view = FindFriendsView.as_view()
        request = factory.get(reverse("friendship:find_friends", args=(10,)))
        response = friendship_view(request, uid=10)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(
            json.loads(response.content),
            {"friends": [x for x in range(2455, 2805, 20)]},
        )
        self.assertEqual(response["content-type"], "application/json")

        friendship_view = FindFriendsView.as_view()
        request = factory.get(reverse("friendship:find_friends", args=(2795,)))
        response = friendship_view(request, uid=2795)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(json.loads(response.content), {"friends": [10]})
        self.assertEqual(response["content-type"], "application/json")

    def test_find_friends_with_non_integer(self):

        factory = APIRequestFactory()
        with self.assertRaises(NoReverseMatch):
            request = factory.get(reverse("friendship:find_friends", args=("FIRST",)))

    def test_find_friends_with_negative_integer(self):

        factory = APIRequestFactory()
        with self.assertRaises(NoReverseMatch):
            request = factory.get(reverse("friendship:find_friends", args=(-15,)))
