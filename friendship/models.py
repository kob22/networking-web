from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


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
