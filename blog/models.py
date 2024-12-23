from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse

from accounts.models import User
from home.models import Tag
from literature.models import Category


class Blog(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='blogs')
    category = models.ManyToManyField(Category, related_name='cblogs')
    picture = models.ImageField(upload_to='blog_images/')
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120)
    body = models.TextField()
    tag = models.ManyToManyField(Tag, related_name='blogs', blank=True)
    comment = GenericRelation('home.Comment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('blog:blog_detail', args=[self.id, self.slug])





