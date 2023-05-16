from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, 'Draft'), (1, 'Published'))
# app_name = 'nomad'


class Post(models.Model):
    """
    Post Model
    """
    CASUAL = 'Casual'
    BUSINESS = 'Business'
    HIKING = 'Hiking'
    PLEASURE = 'Pleasure'
    OTHER = 'Other'

    TRIP_TYPES = [
        (CASUAL, 'Casual'),
        (BUSINESS, 'Business'),
        (HIKING, 'Hiking'),
        (PLEASURE, 'Pleasure'),
        (OTHER, 'Other')
    ]

    title = models.CharField(max_length=200, unique=True, default='')
    slug = models.SlugField(max_length=200, unique=True)
    trip_type = models.CharField(
        max_length=50, choices=TRIP_TYPES, default=CASUAL)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='blogpost_like', blank=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title
        # return self.trip_type

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"
