from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Friendship
from .serializers import FriendshipSerializer, UserSerializer


class FriendshipCreateView(APIView):
    """
    creates friendship relation
    """

    def post(self, request, format=None):
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


class FriendshipDeleteView(APIView):
    """Delete friendship view"""

    def delete(self, request, uid1, uid2, format=None):
        """
        remove friendship relation
        """

        data = {"first_friend": uid1, "second_friend": uid2}
        serializer = FriendshipSerializer(data=data)

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


class FindFriendsView(APIView):
    """Find friends for given UID"""

    def get(self, request, uid, format=None):
        serializer = UserSerializer(data={"uid": uid})

        # check if data (UIDs) are valid
        if serializer.is_valid():
            friends = Friendship.objects.find_friends(uid)

            return Response({"friends": list(friends)}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
