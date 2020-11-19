from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Friendship
from .serializers import FriendshipSerializer, UserSerializer


@api_view(["POST"])
def add_friendship(request):
    """
    creates friendship relation
    """

    serializer = FriendshipSerializer(data=request.data)

    if serializer.is_valid():

        # try to save relation
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except IntegrityError as cm_error:
            """
            Check if friendship already exists, if exists, django will return integrity error,
            but integrity error doesn't have any additional data so I check if 'Unique Friendship' is in error message
            This isn't great solution. It is possible to check if object already exists in validation,
            but database also have to check uniques before writing, so integrity error still can show up.
            """
            if "Unique Friendship" in str(cm_error):
                return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# I was thinking about different approach, I wanted to use delete method with UIDs in urls
@api_view(["POST"])
def remove_friendship(request):
    """
    remove friendship relation
    """

    serializer = FriendshipSerializer(data=request.data)

    # check if data (UIDs) are valid
    if serializer.is_valid():

        # find object in DB
        try:
            friendship = Friendship.objects.get(
                first_friend=serializer.data["first_friend"],
                second_friend=serializer.data["second_friend"],
            )

        except Friendship.DoesNotExist:
            # if object not exists, return OK, do nothing
            return Response(status=status.HTTP_200_OK)

        except Friendship.MultipleObjectsReturned:
            # if multiple objects exist, remove all (not should happened)
            Friendship.objects.filter(
                first_friend=serializer.data["first_friend"],
                second_friend=serializer.data["second_friend"],
            ).delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        friendship.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def find_friends(request, uid):

    serializer = UserSerializer(data={"uid": uid})

    # check if data (UIDs) are valid
    if serializer.is_valid():
        friends = Friendship.objects.find_friends(uid)

        return Response(list(friends), status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
