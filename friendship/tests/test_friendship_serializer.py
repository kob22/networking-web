from django.test import TestCase
from rest_framework.exceptions import ValidationError

from friendship.models import Friendship
from friendship.serializers import FriendshipSerializer


class FriendshipSerializerTest(TestCase):
    def setUp(self) -> None:
        self.friends_id = {"first_friend": 1, "second_friend": 5}
        self.friendship = Friendship.objects.create(**self.friends_id)
        self.serializer = FriendshipSerializer(instance=self.friends_id)

    def test_serializer_contains_only_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ["first_friend", "second_friend"])

    def test_serializer_contains_correct_data(self):
        self.assertEqual(self.serializer.data, self.friends_id)

    def test_create_object_from_serializer(self):
        data = {"first_friend": 325325, "second_friend": 43634634}
        friendship_serialized = FriendshipSerializer(data=data)
        friendship_serialized.is_valid()
        friendship_serialized.save()

        friendship = Friendship.objects.filter(
            first_friend=data["first_friend"], second_friend=data["second_friend"]
        ).first()
        self.assertEqual(
            friendship_serialized.data, FriendshipSerializer(instance=friendship).data
        )

    def test_serializer_validation_invalid_data(self):
        data = {"first_friend": "A", "second_friend": "4Z3634634"}
        friendship_serialized = FriendshipSerializer(data=data)

        with self.assertRaises(ValidationError):
            friendship_serialized.is_valid(raise_exception=True)

        self.assertEqual(
            friendship_serialized.errors,
            {
                "first_friend": ["Ensure UID is any non-negative integer number"],
                "second_friend": ["Ensure UID is any non-negative integer number"],
            },
        )

    def test_serializer_validation_not_completed_data(self):
        data = {"first_friend": 256346}
        friendship_serialized = FriendshipSerializer(data=data)

        with self.assertRaises(ValidationError):
            friendship_serialized.is_valid(raise_exception=True)

        self.assertEqual(
            friendship_serialized.errors, {"second_friend": ["This field is required."]}
        )

        data = {"second_friend": 256346}
        friendship_serialized = FriendshipSerializer(data=data)

        with self.assertRaises(ValidationError):
            friendship_serialized.is_valid(raise_exception=True)

        self.assertEqual(
            friendship_serialized.errors, {"first_friend": ["This field is required."]}
        )

        data = {"first_fariend": 3252532, "second_friesnd": 256346}
        friendship_serialized = FriendshipSerializer(data=data)

        with self.assertRaises(ValidationError):
            friendship_serialized.is_valid(raise_exception=True)

        self.assertEqual(
            friendship_serialized.errors,
            {
                "first_friend": ["This field is required."],
                "second_friend": ["This field is required."],
            },
        )

    def test_serializer_validation_same_id(self):
        data = {"first_friend": 256346, "second_friend": 256346}
        friendship_serialized = FriendshipSerializer(data=data)

        with self.assertRaises(ValidationError):
            friendship_serialized.is_valid(raise_exception=True)

        self.assertEqual(
            friendship_serialized.errors, {"Error": ["Friends UIDs must be different!"]}
        )

    def test_serializer_validation_with_too_much_attr(self):
        data = {"first_friend": 256346, "second_friend": 2563461, "third_friend": 3223}
        friendship_serialized = FriendshipSerializer(data=data)

        friendship_serialized.is_valid(raise_exception=True)
        friendship_serialized.save()

        friendship = Friendship.objects.filter(
            first_friend=data["first_friend"], second_friend=data["second_friend"]
        ).first()
        self.assertEqual(
            friendship_serialized.data, FriendshipSerializer(instance=friendship).data
        )
