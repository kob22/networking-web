from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import FriendshipSerializer


@api_view(["POST"])
def add_friendship(request):
    """
    creates friendship relation
    """
    if request.method == "POST":
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
