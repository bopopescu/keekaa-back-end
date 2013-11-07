from django.db import models
from django.contrib.contenttypes import generic
from django.utils.timezone import now
from website.actions.models import Vote, Comment, Favorite
from website.library.models import DujourDefaultModel
from website.library.default_functions import create_uuid
from website.media.models import Image
from website.users.models import UserProfile


class Brand(DujourDefaultModel):
    uuid = models.CharField(
        max_length=36, unique=True, default=create_uuid)
    name = models.CharField(max_length=255)
    url_name = models.CharField(max_length=255)
    address = models.TextField(default='')
    description = models.TextField(default='')
    updated_time = models.DateTimeField(default=now)
    created_time = models.DateTimeField(default=now)
    IPaddress = models.GenericIPAddressField()
    is_active = models.BooleanField(default=True)

    # relational field
    owner = models.ForeignKey(UserProfile)
    vote_set = generic.GenericRelation(Vote)
    comment_set = generic.GenericRelation(Comment)
    favorite_set = generic.GenericRelation(Favorite)

    def __str__(self):
        return self.name


class Item(DujourDefaultModel):
    uuid = models.CharField(
        max_length=36, unique=True, default=create_uuid)
    name = models.CharField(max_length=255)
    size = models.CharField(max_length=3, default='')
    price = models.DecimalField(
        max_digits=9, decimal_places=2, default=0.00)
    color = models.CharField(max_length=32, default='')
    description = models.TextField(default='')
    url = models.URLField()
    brand_name = models.CharField(max_length=255, default='')
    updated_time = models.DateTimeField(default=now)
    created_time = models.DateTimeField(default=now)
    IPaddress = models.GenericIPAddressField()
    is_active = models.BooleanField(default=True)

    # relational fields
    vote_set = generic.GenericRelation(Vote)
    comment_set = generic.GenericRelation(Comment)
    favorite_set = generic.GenericRelation(Favorite)
    brand = models.ForeignKey(Brand, null=True)
    owner = models.ForeignKey(UserProfile, default=0)
    image_set = models.ManyToManyField(Image, through='ItemTag')

    def __str__(self):
        return self.name


class ItemTag(DujourDefaultModel):
    uuid = models.CharField(
        max_length=36, unique=True, default=create_uuid)
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)
    num = models.IntegerField(default=0)
    updated_time = models.DateTimeField(default=now)
    created_time = models.DateTimeField(default=now)
    IPaddress = models.GenericIPAddressField()
    is_active = models.BooleanField(default=True)

    # relational fields
    owner = models.ForeignKey(UserProfile)
    comment_set = generic.GenericRelation(Comment)
    vote_set = generic.GenericRelation(Vote)
    favorite_set = generic.GenericRelation(Favorite)
    image = models.ForeignKey(Image)
    item = models.ForeignKey(Item)
