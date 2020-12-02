from django.contrib import admin
from .models import Post, Category, Comment, PostSetting, CommentLike
from django.utils.translation import ngettext
from django.contrib import messages


class ChildrenItemInline(admin.TabularInline):
    model = Category
    fields = (
        'title', 'slug'
    )
    extra = 1
    show_change_link = True


class PostSettingInline(admin.TabularInline):
    model = PostSetting


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'publish_time', 'category', 'author', 'draft', 'create_at', 'update_at')
    search_fields = ('title', 'slug')
    list_filter = ('author',)
    date_hierarchy = 'publish_time'
    inlines = [
        PostSettingInline
    ]
    actions = ['make_published']

    def make_published(self, request, queryset):
        updated = queryset.update(draft=True)

        self.message_user(request, ngettext(
            '%d story was successfully marked as published.',
            '%d stories were successfully marked as published.',
            updated,
        ) % updated, messages.SUCCESS)
    make_published.short_description = "Mark selected stories as published"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'parent')
    search_fields = ('slug', 'title')
    list_filter = ('parent',)
    inlines = [
        ChildrenItemInline,
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'is_confirmed', 'like_count', 'dislike_count')
    search_fields = ('post',)
    date_hierarchy = 'create_at'


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('author', 'get_post', 'condition')
