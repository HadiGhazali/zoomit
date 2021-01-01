from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from .models import Post, Category, Comment
from account.serializers import UserSerializer

User = get_user_model()


# class CommentSerializer(serializers.ModelSerializer):
#     author_detail = UserSerializer(read_only=True, source='author')
#
#     class Meta:
#         model = Comment
#         fields = "__all__"


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=128)
    slug = serializers.SlugField()
    content = serializers.CharField()
    create_at = serializers.ReadOnlyField()
    update_at = serializers.ReadOnlyField()
    publish_time = serializers.DateTimeField()
    draft = serializers.BooleanField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    image = serializers.ImageField(allow_null=True)
    image2 = serializers.ImageField(allow_null=True)
    image3 = serializers.ImageField(allow_null=True)

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def validate_slug(self, slug):
        try:
            Post.objects.get(slug=slug)
            raise serializers.ValidationError('slug must be unique')
        except Post.DoesNotExist:
            return slug

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.content = validated_data.get('content', instance.content)
        instance.publish_time = validated_data.get('publish_time', instance.publish_time)
        instance.image = validated_data.get('image', instance.image)
        instance.image2 = validated_data.get('image2', instance.image2)
        instance.image3 = validated_data.get('image3', instance.image3)
        instance.draft = validated_data.get('draft', instance.draft)
        instance.save()
        return instance


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    content = serializers.CharField()
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    create_at = serializers.DateTimeField(read_only=True)
    update_at = serializers.DateTimeField(read_only=True)
    author_detail = UserSerializer(read_only=True, source='author')
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    is_confirmed = serializers.BooleanField()

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.content = validated_data.get('content', instance.content)
        instance.post = validated_data.get('post', instance.post)
        instance.is_confirmed = validated_data.get('is_confirmed', instance.is_confirmed)
        instance.save()
        return instance
