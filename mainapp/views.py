from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import status
from  rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import PostSerializer, ImageSerializer, UserSerializer
from .models import Post, PostImage, Vote
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

@api_view(['GET', ])
def index_view(request):
    data={}
    queryset = get_user_reccommendations(request.user)
    print(len(queryset))
    for i in queryset:
        print(i)
    for post in Post.objects.all():
        if request.user not in post.disliked_users:
            post = PostSerializer(post).data
            if post not in queryset:
                queryset.append(post)
    data['length'] = len(queryset)
    data['posts'] = queryset
    return Response(data, status=status.HTTP_200_OK)
