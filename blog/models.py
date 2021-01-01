from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from datetime import datetime
from ckeditor.fields import RichTextField

MAIN_CATEGORY = (
    ('Tech', 'تکنولوژی'),
    ('Car', 'خودرو'),
    ('Science', 'علمی'),
)


class Category(models.Model):
    title = models.CharField(_('Title'), max_length=50)
    slug = models.SlugField(_("Slug"), db_index=True, unique=True)
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)
    parent = models.ForeignKey('self', verbose_name=_("Parent"), on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='children', related_query_name='children')
    main_category = models.CharField(_('Main category'), max_length=10, choices=MAIN_CATEGORY, blank=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.slug


class Post(models.Model):
    title = models.CharField(_("Title"), max_length=128)
    slug = models.SlugField(_("Slug"), db_index=True, unique=True)
    # content = models.TextField(_("Content"))
    content = RichTextField(verbose_name=_('Content'), null=True, blank=True)
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)
    publish_time = models.DateTimeField(_("Publish at"), db_index=True, default=timezone.now())
    draft = models.BooleanField(_("Draft"), default=True, db_index=True)
    image = models.ImageField(_("image"), upload_to='post/images', null=True, blank=True)
    image2 = models.ImageField(_("image"), upload_to='post/images', null=True, blank=True)
    image3 = models.ImageField(_("image"), upload_to='post/images', null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), related_name='posts',
                               related_query_name='children', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name=_('Category'), on_delete=models.SET_NULL,
                                 related_name='posts',
                                 null=True, blank=True)
    summary = models.CharField(_("Summary"), max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['-publish_time']

    def __str__(self):
        return self.title


class PostSetting(models.Model):
    post = models.OneToOneField("Post", verbose_name=_("post"), on_delete=models.CASCADE, related_name='post_setting',
                                related_query_name='post_setting')
    comment = models.BooleanField(_("comment"))
    author = models.BooleanField(_("author"))
    allow_discussion = models.BooleanField(_("allow discussion"))

    class Meta:
        verbose_name = _("PostSetting")
        verbose_name_plural = _("PostSettings")


class Comment(models.Model):
    content = models.TextField(verbose_name=_('Comment'), null=True, blank=True)
    post = models.ForeignKey(Post, verbose_name=_("Post"), on_delete=models.CASCADE, related_name='comments',
                             related_query_name='comments')
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(_("Confirm"), default=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['-create_at']

    def __str__(self):
        return self.post.title

    @property
    def like_count(self):
        q = self.comment_like.filter(condition=True)
        return q.count()

    @property
    def dislike_count(self):
        q = self.comment_like.filter(condition=False)
        return q.count()


class CommentLike(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, verbose_name=_('Comment'), on_delete=models.CASCADE,
                                related_name='comment_like')
    condition = models.BooleanField(_("Condition"))
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)

    class Meta:
        unique_together = [['author', 'comment']]
        verbose_name = _("CommentLike")
        verbose_name_plural = _("CommentLikes")

    def __str__(self):
        return str(self.condition)

    @property
    def get_post(self):
        return self.comment.post


class UrlHit(models.Model):
    post = models.OneToOneField(Post, verbose_name=_('post'), on_delete=models.CASCADE, related_name='url_hit',
                                related_query_name='url_hit')
    url = models.CharField(max_length=150, unique=True)
    hits = models.PositiveIntegerField(default=0)
    daily_hits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.url)

    def increase(self):
        self.hits += 1
        self.save()

    def get_daily_hits(self):
        return self.daily_hits

    def set_daily_hits(self, daily_hits):
        self.daily_hits = daily_hits
        self.save()


class HitCount(models.Model):
    url_hit = models.ForeignKey(UrlHit, editable=True, on_delete=models.CASCADE)
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(null=True)

    def updating_date(self):
        self.update_date = timezone.now()
        self.save()

    def get_date(self):
        return self.update_date.date()

    def set_user(self, user):
        self.user = user
        self.save()
