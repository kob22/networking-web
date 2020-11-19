from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class FriendshipManager(models.Manager):
    def find_friends(self, UID):
        """
        returns a list of UIDs who are friends of the user
        to find friends, you have to search both columns,
        this code will create SQL statement
        SELECT second_friend where first_friend = UID
        UNION
        SELECT first_friend where second_fiend = UID
        """
        first = self.values_list("second_friend", flat=True).filter(first_friend=UID)
        second = self.values_list("first_friend", flat=True).filter(second_friend=UID)
        all_friends = first.union(second)
        return all_friends


class Friendship(models.Model):
    first_friend = models.PositiveBigIntegerField(
        blank=False,
        null=False,
        validators=[
            MinValueValidator(
                1, message="Ensure UID is any non-negative integer number"
            )
        ],
        error_messages={"invalid": "Ensure UID is any non-negative integer number"},
    )
    second_friend = models.PositiveBigIntegerField(
        blank=False,
        null=False,
        validators=[
            MinValueValidator(
                1, message="Ensure UID is any non-negative integer number"
            )
        ],
        error_messages={"invalid": "Ensure UID is any non-negative integer number"},
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = FriendshipManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["first_friend", "second_friend"], name="Unique Friendship"
            )
        ]

    def clean(self, *args, **kwargs):
        """
        check if both ids are different
        """
        errors = {}
        try:
            self.clean_fields()
        except ValidationError as e:
            errors = e.update_error_dict(errors)
        if not errors:
            self.check_order_UIDs()
        if self.first_friend == self.second_friend:
            raise ValidationError(
                {
                    "Error": "Friends UIDs must be different!",
                },
                code="invalid",
            )

    def save(self, *args, **kwargs):
        """
        saving friendship, first friend ID  is always smaller than second ID, if not swap them
        """
        self.check_order_UIDs()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Friendship between {self.first_friend} and {self.second_friend}"

    def check_order_UIDs(self):
        if self.first_friend > self.second_friend:
            self.first_friend, self.second_friend = (
                self.second_friend,
                self.first_friend,
            )
