from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class Category(models.Model):
    title = models.CharField(_('Title'), max_length=50)
    slug = models.SlugField(_("Slug"), db_index=True, unique=True)
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)
    parent = models.ForeignKey('self', verbose_name=_("Parent"), on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='children', related_query_name='children')

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.slug


class Post(models.Model):
    title = models.CharField(_("Title"), max_length=128)
    slug = models.SlugField(_("Slug"), db_index=True, unique=True)
    content = models.TextField(_("Content"))
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)
    publish_time = models.DateTimeField(_("Publish at"), db_index=True)
    draft = models.BooleanField(_("Draft"), default=True, db_index=True)
    image = models.ImageField(_("image"), upload_to='post/images', null=True)
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
    content = models.TextField(_("Content"))
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
