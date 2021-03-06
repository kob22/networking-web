from rest_framework import serializers

from . import models


class UserSerializer(serializers.Serializer):
    uid = serializers.IntegerField(
        min_value=1,
        error_messages={
            "invalid": "Ensure UID is any non-negative integer number",
            "min_value": "Ensure UID is any non-negative integer number",
        },
    )


class FriendshipSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data["first_friend"] == data["second_friend"]:
            raise serializers.ValidationError(
                {
                    "Error": "Friends UIDs must be different!",
                },
                code="invalid",
            )
        # validate friendship, first friend ID  is always smaller than second ID, if not swap them
        if data["first_friend"] > data["second_friend"]:
            data["first_friend"], data["second_friend"] = (
                data["second_friend"],
                data["first_friend"],
            )
        return data

    class Meta:
        model = models.Friendship
        fields = ("first_friend", "second_friend")
        extra_kwargs = {
            "first_friend": {
                "error_messages": {
                    "invalid": "Ensure UID is any non-negative integer number",
                    "min_value": "Ensure UID is any non-negative integer number",
                }
            },
            "second_friend": {
                "error_messages": {
                    "invalid": "Ensure UID is any non-negative integer number",
                    "min_value": "Ensure UID is any non-negative integer number",
                }
            },
        }
