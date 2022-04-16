import json

from django.contrib.auth.models import User

from mainapp.serializers import PostSerializer, PostTagSerializer

from .models import Tag, Vote, PostTag, Post


def get_user_reccommendations(user):
    rec = []
    tag_weights = {}
    posts = []
    votes = Vote.objects.filter(user=user)
    for vote in votes:
        post = vote.post
        post_tags = PostTag.objects.filter(post=post)
        for post_tag in post_tags:
            if post_tag.tag.text not in tag_weights.keys():
                tag_weights[post_tag.tag.text] = vote.vote * post_tag.weight
            else:
                tag_weights[post_tag.tag.text] += vote.vote * post_tag.weight
    sorted_tag_weights = {k:v for k, v in sorted(tag_weights.items(), key=lambda v: v[1], reverse=True)}

    for tag in sorted_tag_weights.keys():
        if sorted_tag_weights.get(tag)>0:
            tag_obj = Tag.objects.get(text=tag)
            post_tags = PostTag.objects.filter(tag=tag_obj)
            for post_tag in post_tags:
                posts.append(post_tag.post)
    for post in posts:
            if post not in rec:
                rec.append(post)

    return rec  

