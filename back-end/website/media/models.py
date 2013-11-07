from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from taggit.managers import TaggableManager
from website.users.models import UserProfile, Community
from website import settings
from website.actions.models import Comment, Vote, Favorite
from website.library.models import DujourDefaultModel
from website.library.default_functions import create_uuid


class Collection(DujourDefaultModel):
    uuid = models.CharField(
        max_length=36, unique=True, default=create_uuid)
    name = models.CharField(max_length=255)
    description = models.TextField(default='')
    location = models.CharField(max_length=255)
    updated_time = models.DateTimeField(default=now)
    created_time = models.DateTimeField(default=now)
    IPaddress = models.GenericIPAddressField()
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)

    # relational fields
    comment_set = generic.GenericRelation(Comment)
    vote_set = generic.GenericRelation(Vote)
    favorite_set = generic.GenericRelation(Favorite)
    owner = models.OneToOneField(UserProfile)

    def __unicode__(self):
        return self.name

    def user_voted(self, user_id):
        userProfile = User.objects.get(pk=user_id).get_profile
        return self.vote_set.filter(
            owner=userProfile.id, is_active=True).exists()

    def total_images(self):
        return self.image_set.filter(is_active=True).count()

    def total_wordboxes(self):
        return self.wordbox_set.filter(is_active=True).count()


class Image(DujourDefaultModel):
    uuid = models.CharField(
        max_length=36, unique=True, default=create_uuid)
    title = models.CharField(max_length=64)
    description = models.TextField(default='')
    created_time = models.DateTimeField(default=now)
    updated_time = models.DateTimeField(default=now)
    position = models.IntegerField(default=0)
    IPaddress = models.GenericIPAddressField()
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    has_owner = models.BooleanField(default=False)

# EXIF data
# ref: http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/EXIF.html

    cameraMake = models.CharField(max_length=52, null=True)
    cameraModel = models.CharField(max_length=52, null=True)
    has_Geolocation = models.BooleanField(default=False)
    GPS_latitude = models.FloatField(null=True)
        # Decimal Degrees (WGS84) used by Google map
    GPS_longitude = models.FloatField(null=True)
        # Decimal Degrees (WGS84) used by Google map
    GPS_altitude = models.FloatField(null=True)
        # Decimal Degrees (WGS84) used by Google map

    tags = TaggableManager()

    # relational fields
    owner = models.ForeignKey(UserProfile)
    comment_set = generic.GenericRelation(Comment)
    vote_set = generic.GenericRelation(Vote)
    favorite_set = generic.GenericRelation(Favorite)
    collection_set = models.ManyToManyField(
        Collection, related_name='image_set')
    community_set = models.ManyToManyField(
        Community, related_name='image_set')

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.title

    def total_items(self):
        return self.itemtag_set.filter(is_active=True).count()


class ImageVersion(models.Model):
    height = models.IntegerField()
    width = models.IntegerField()
    url = models.CharField(max_length=256)
    filesize = models.BigIntegerField()
    image = models.ForeignKey(Image)

    def get_uri(self):
        return settings.MEDIA_FARM_SERVER_URI + self.url


class WordBox(DujourDefaultModel):
    uuid = models.CharField(
        max_length=36, unique=True, default=create_uuid)
    title = models.CharField(max_length=64)
    message = models.CharField(max_length=140)
    created_time = models.DateTimeField(default=now)
    updated_time = models.DateTimeField(default=now)
    IPaddress = models.GenericIPAddressField()
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)

    tags = TaggableManager()

    # relational fields
    owner = models.ForeignKey(UserProfile)
    comment_set = generic.GenericRelation(Comment)
    vote_set = generic.GenericRelation(Vote)
    favorite_set = generic.GenericRelation(Favorite)
    community_set = models.ManyToManyField(
        Community, related_name='wordbox_set')
    collection_set = models.ManyToManyField(
        Collection, related_name='wordbox_set')

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.message
