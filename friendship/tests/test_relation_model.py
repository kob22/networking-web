import datetime

import mock
import pytz
from django.core.exceptions import ValidationError
from django.test import TestCase

from friendship.models import Friendship


class FriendshipModelTest(TestCase):
    def test_create_simple_friendship(self):
        date_to_mock = datetime.datetime(2020, 10, 11, 15, 52, 12, tzinfo=pytz.utc)
        with mock.patch(
            "django.utils.timezone.now", mock.Mock(return_value=date_to_mock)
        ):

            friendship = Friendship(first_friend=1, second_friend=5)
            friendship.full_clean()
            friendship.save()

        friendship.refresh_from_db()
        self.assertEqual(friendship.first_friend, 1)
        self.assertEqual(friendship.second_friend, 5)
        self.assertEqual(friendship.created_at, date_to_mock)

    def test_create_friendship_with_first_wrong_integer_id(self):
        parameters = [0, -1, -100]
        for parameter in parameters:
            friendship = Friendship(first_friend=parameter, second_friend=5)
            with self.assertRaises(ValidationError) as error:
                friendship.full_clean()

            the_exception = error.exception
            self.assertEqual(
                the_exception.message_dict,
                {"first_friend": ["Ensure UID is any non-negative integer number"]},
            )

    def test_should_not_create_friendship_with_first_wrong_id(self):
        parameters = ["a", "%", "\sdf"]
        for parameter in parameters:
            friendship = Friendship(first_friend=parameter, second_friend=5)
            with self.assertRaises(ValidationError) as error:
                friendship.full_clean()

    def test_should_not_create_friendship_with_second_wrong_integer_id(self):
        parameters = [0, -1, -100]
        for parameter in parameters:
            friendship = Friendship(first_friend=2, second_friend=parameter)
            with self.assertRaises(ValidationError) as error:
                friendship.full_clean()

            the_exception = error.exception
            self.assertEqual(
                the_exception.message_dict,
                {"second_friend": ["Ensure UID is any non-negative integer number"]},
            )

    def test_should_not_create_friendship_with_second_wrong_id(self):
        parameters = ["a", "%", "\sdf"]
        for parameter in parameters:
            friendship = Friendship(first_friend=2, second_friend=parameter)
            with self.assertRaises(ValidationError) as error:
                friendship.full_clean()

    def test_should_not_create_friendship_with_the_same_ids(self):
        friendship = Friendship(first_friend=5, second_friend=5)
        with self.assertRaises(ValidationError) as error:
            friendship.full_clean()

        the_exception = error.exception
        self.assertEqual(
            the_exception.message_dict, {"Error": ["Friends UIDs must be different!"]}
        )

    def test_storage_order_friends_id(self):
        friendship = Friendship(first_friend=50, second_friend=5)
        self.assertGreater(friendship.first_friend, friendship.second_friend)
        friendship.full_clean()
        friendship.save()

        friendship.refresh_from_db()
        self.assertLess(friendship.first_friend, friendship.second_friend)

    def test_should_not_create_new_friendship_if_friendship_exist(self):
        friendship = Friendship(first_friend=6785, second_friend=2332515)
        friendship.save()

        same_friendship = Friendship(first_friend=6785, second_friend=2332515)
        with self.assertRaises(ValidationError) as error:
            same_friendship.full_clean()

        the_exception = error.exception
        self.assertEqual(
            the_exception.messages,
            ["Friendship with this First friend and Second friend already exists."],
        )

    def test_should_not_create_new_friendship_if_friendship_exist_with_diff_order_UIDs(
        self,
    ):
        friendship = Friendship(first_friend=67851, second_friend=23325152)
        friendship.save()

        same_friendship = Friendship(first_friend=23325152, second_friend=67851)
        with self.assertRaises(ValidationError) as error:
            same_friendship.full_clean()

        the_exception = error.exception
        self.assertEqual(
            the_exception.messages,
            ["Friendship with this First friend and Second friend already exists."],
        )
