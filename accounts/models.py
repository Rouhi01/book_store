from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.urls import reverse
from .managers import UserManager
from django.contrib.contenttypes.fields import GenericRelation
from home.models import Like, Comment


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.email


class Profile(models.Model):
    GENDER_CHOICES = [
        ('', 'انتخاب جنسیت'),
        ('male', 'مرد'),
        ('female', 'زن'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    follower = models.PositiveIntegerField(default=0)
    following = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - Profile"


class Relation(models.Model):
    from_user = models.ForeignKey(User, models.CASCADE, related_name='followers')
    to_user = models.ForeignKey(User, models.CASCADE, related_name='followings')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} following {self.to_user}'


class Post(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='posts')
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120)
    content = models.TextField()
    tags = models.ManyToManyField('home.Tag', related_name='posts', blank=True)
    likes = GenericRelation('home.Like')
    comments = GenericRelation('home.Comment')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('accounts:post_detail', args=[self.user.id, self.id])

    def get_total_likes(self):
        model_name = self.__class__.__name__.lower()
        number_of_likes = Like.objects.filter(
            content_type=ContentType.objects.get(model=model_name),
            object_id=self.id
        ).count()
        return number_of_likes

    def get_total_comments(self):
        model_name = self.__class__.__name__.lower()
        number_of_comment = Comment.objects.filter(
            content_type=ContentType.objects.get(model=model_name),
            object_id=self.id
        ).count()
        return number_of_comment

    def is_liked(self, request):
        model_name = self.__class__.__name__.lower()
        liked = Like.objects.filter(
            user=request.user,
            content_type=ContentType.objects.get(model=model_name),
            object_id=self.id
        ).exists()
        return liked
