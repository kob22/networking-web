from rest_framework import serializers

from . import models


class FriendshipSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data["first_friend"] == data["second_friend"]:
            raise serializers.ValidationError(
                {
                    "Error": "Friends UIDs must be different!",
                },
                code="invalid",
            )
        return data

    class Meta:
        model = models.Friendship
        fields = ("first_friend", "second_friend")
        extra_kwargs = {
            "first_friend": {
                "error_messages": {
                    "invalid": "Ensure UID is any non-negative integer number"
                }
            },
            "second_friend": {
                "error_messages": {
                    "invalid": "Ensure UID is any non-negative integer number"
                }
            },
        }
