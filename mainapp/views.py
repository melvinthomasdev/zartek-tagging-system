from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.pagination import LimitOffsetPagination

from .serializers import PostSerializer, UserSerializer
from .models import Post, Vote
from .helpers import get_user_reccommendations

# Create your views here.


@api_view(["POST", ])
@permission_classes([AllowAny, ])
def create_user_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")
        print(password)
        try:
            user = User.objects.get(username=username)
            return Response(
                {
                    "message": "Account with this username already exists!!",
                    "username": user.username,
                },
                status=status.HTTP_409_CONFLICT
            )
        except ObjectDoesNotExist:
            user = User.objects.create_user(username=username, password=password)
    else:
        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
    return Response(
        {
            "message": "Account created",
            "username": user.username,
        },
        status=status.HTTP_201_CREATED
    )

class VotePostview(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, id):
        user_vote = request.data.get('vote')
        if user_vote is None:
            return Response({
                "message": "you need to provide a value for your vote"
            }, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        try:
            post = Post.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response(
                {
                    "message": "post not found!",
                    "id": id
                },
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            vote_object = Vote.objects.get(user=user, post=post)
            vote_object.vote = user_vote
            vote_object.save()
        except:
            Vote.objects.create(user=user, post=post, vote=user_vote)

        return Response(
            {
                "message": "Success"
            },
            status=status.HTTP_200_OK
        )

class IndexView(APIView, LimitOffsetPagination):

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        data = get_user_reccommendations(request.user)
        for post in Post.objects.all():
            if request.user not in post.disliked_users:
                if post not in data:
                    data.append(post)
        page = self.paginate_queryset(data, request)
        serializer = PostSerializer(page, many=True, context={"user": request.user})
        return self.get_paginated_response(serializer.data)


class GetLikedUsers(APIView, LimitOffsetPagination):

    permission_classes = (IsAdminUser, )

    def get(self, request, id):
        try:
            post = Post.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response(
                {
                    "message": "post Not Found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        page = self.paginate_queryset(post.liked_users, request)
        serializer = UserSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
