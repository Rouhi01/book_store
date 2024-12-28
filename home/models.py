
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.urls import reverse


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ucomments')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    GenericRelation('home.like')

    reply = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='rcomments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_model_name(self):
        return self.content_type.model_class().__name__.lower()

    def get_absolute_url(self):
        return reverse('home:comment', args=[self.user.id, 'Comment', self.id])


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ulikes')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # parent_content_type = models.ForeignKey(
    #     ContentType,
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True,
    #     related_name='parent_likes'
    # )
    # parent_object_id = models.PositiveIntegerField(null=True, blank=True)
    # parent_object = GenericForeignKey('parent_content_type', 'parent_object_id')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    def __str__(self):
        return f'{self.user} liked {self.content_type}'


class Contact(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=80)
    topic = models.CharField(max_length=120)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email} - {self.topic}'


