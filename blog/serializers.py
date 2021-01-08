from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from .models import Post, Category, Comment, PostSetting
from account.serializers import UserSerializer

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PostSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostSetting
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    # comment_detail = CommentSerializer(read_only=True, many=True, source='comments')
    post_setting_details = PostSettingSerializer(read_only=True, source='post_setting')

    class Meta:
        model = Post
        fields = "__all__"
