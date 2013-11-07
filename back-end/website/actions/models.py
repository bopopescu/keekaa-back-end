from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.forms import ModelForm
from django.utils.timezone import now
from website.users.models import UserProfile
from website.library.default_functions import create_uuid
from website.library.models import DujourDefaultModel, DujourDefaultModel_MPTT
from mptt.models import TreeForeignKey


class Action(DujourDefaultModel):
    uuid = models.CharField(
        max_length=36, unique=True, default=create_uuid)
    request_method = models.IntegerField()
    created_time = models.DateTimeField(default=now, db_index=True)
    parent_type = models.ForeignKey(
        ContentType, related_name='parent_action_set')
    parent_id = models.PositiveIntegerField()
    child_type = models.ForeignKey(
        ContentType, related_name='child_action_set', null=True)
    child_id = models.PositiveIntegerField(null=True)
    has_error = models.BooleanField(default=0)
    IPaddress = models.GenericIPAddressField()
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)

    # relationships
    owner = models.ForeignKey(UserProfile)
    parent = generic.GenericForeignKey('parent_type', 'parent_id')
    child = generic.GenericForeignKey('child_type', 'child_id')

    def __unicode__(self):
        return self.owner.username + ' ' + ' ' + self.parent_type.model

    def user_voted(self, user_id):

        userProfile = User.objects.get(pk=user_id).get_profile()
        return self.vote_set.filter(owner=userProfile.id,
                                    is_active=True).exists()


class Vote(models.Model):
# base class is models.Model (as opposed to DujourDefaultModel)
# because the base model contains
# class methods that involve votes that all other classes use.
# They cannot be used with this class

    uuid = models.CharField(
        max_length=36, unique=True, default=create_uuid)
    value = models.BooleanField(default=1)
    created_time = models.DateTimeField(default=now)
    IPaddress = models.GenericIPAddressField()
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)

    # relational fields
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    parent = generic.GenericForeignKey(
        'content_type', 'object_id')
    owner = models.ForeignKey(UserProfile)

    def obj_type(self):
        return type(self).__name__.lower()

    def __unicode__(self):
        return unicode(self.pk)


class Favorite(DujourDefaultModel):
    uuid = models.CharField(
        max_length=36, unique=True, default=create_uuid)
    value = models.BooleanField(default=1)
    created_time = models.DateTimeField(default=now)
    IPaddress = models.GenericIPAddressField()
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)

    # relational fields
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    parent = generic.GenericForeignKey(
        'content_type', 'object_id')
    owner = models.ForeignKey(UserProfile)

    def __unicode__(self):
        return str(self.id)


class Comment(DujourDefaultModel_MPTT):
    uuid = models.CharField(
        max_length=36, unique=True, default=create_uuid)
    message = models.TextField()
    created_time = models.DateTimeField(default=now)
    IPaddress = models.GenericIPAddressField()
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)

    # relational fields
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    # default NULL?
    parent = generic.GenericForeignKey(
        'content_type', 'object_id')  # can be updated
    parent_comment = TreeForeignKey(
        'self', null=True, blank=True, related_name='children')
    owner = models.ForeignKey(
        UserProfile, related_name='owner_comment_set')
    vote_set = generic.GenericRelation(Vote)
    favorite_set = generic.GenericRelation(Favorite)
    total_votes = models.PositiveIntegerField(default=0)

    class MPTTMeta:
        parent_attr = 'parent_comment'
#        order_insertion_by = ['']

    def __unicode__(self):
        return self.message[:5]

#################### MODEL FORMS ######################


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('message',)
