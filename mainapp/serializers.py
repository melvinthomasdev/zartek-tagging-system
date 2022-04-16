from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.forms import ValidationError

from rest_framework import serializers

from .models import PostImage, Post, VOTE_CHOICES, Vote


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=30)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(max_length=128, trim_whitespace=False, write_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        User.objects.create(**validated_data)
        return super().create(validated_data)


class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def create(self, validated_data):
        return super().create(validated_data)


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=30)
    description = serializers.CharField(max_length=15)
    postimage = ImageSerializer(read_only=True, many=True)

    def create(self, validated_data):
        Post.objects.create(**validated_data)


class TagSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=15)

class PostTagSerializer(serializers.Serializer):
    post = PostSerializer()
    tag = TagSerializer()
    weight = serializers.IntegerField()


