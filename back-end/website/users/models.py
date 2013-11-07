import datetime
import json
import pytz

from dateutil.relativedelta import relativedelta
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from website.settings import Maximum_Portable_Devices_Per_User
from website.library.default_functions import create_uuid
from website.library.models import DujourDefaultModel
from taggit.managers import TaggableManager


class UserProfile(DujourDefaultModel):
    uuid = models.CharField(
        max_length=36,
        unique=True,
        default=create_uuid
    )
    username = models.CharField(max_length=32)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    updated_time = models.DateTimeField(default=now)
    created_time = models.DateTimeField(default=now)
    last_login_time = models.DateTimeField(default=now)
    email = models.EmailField()
    # optional fields

    '''
    Device tokens will be stored in json string format used
    for push notification.

    The valid format of device_tokens will be the following:
    (ps, device_type can be iphone, android)
    {
        "FE66489F30...": {
                "last_registration": "2009-11-06 20:41:06",
                "device_type":"android"
        }
    }
    '''
    device_tokens = models.TextField(default='{}')

    about_me = models.CharField(max_length=1024, default='')
    location = models.CharField(max_length=2048, default='')
    age = models.IntegerField(null=True, blank=True)
    fashion_statement = models.CharField(max_length=2048, default='')
    website = models.URLField(default='')
    gender = models.CharField(
        max_length=1, null=True)   # M: Male, F: Female
    birthday = models.DateTimeField(null=True)
    height = models.FloatField(null=True)   # kilogram
    weight = models.FloatField(null=True)   # meter
    phone = models.CharField(max_length=32, null=True)
    is_active = models.BooleanField(default=True)
    notification_count = models.IntegerField(default=0)
    statement = models.TextField(default='')
    last_notification = models.DateTimeField(default=datetime.datetime(
        1970, 1, 1, tzinfo=pytz.timezone("US/Pacific")))

    # relational fields
    user = models.OneToOneField(User, unique=True, null=True)
    to_friends = models.ManyToManyField("self", through='Friendship',
                                        symmetrical=False,
                                        related_name='from_friends')
    to_subscribers = models.ManyToManyField("self", through='UserSubscription',
                                            symmetrical=False,
                                            related_name='from_subscribers')
    to_notifiers = models.ManyToManyField("self", through='Notification',
                                          symmetrical=False,
                                          related_name='from_notifiers')
    image_collection_set = models.ManyToManyField(
        "media.Image", related_name='userprofile_set')
    wordbox_collection_set = models.ManyToManyField(
        "media.WordBox", related_name='userprofile_set')
    total_collections = models.IntegerField(default=0)
    total_images = models.IntegerField(default=0)
    total_groups = models.IntegerField(default=0)
    total_friends = models.IntegerField(default=0)
    total_notifications = models.IntegerField(default=0)

    # GenericForeign key from Comment for User's wall
    comment_set = generic.GenericRelation('actions.Comment')

    profile_image_thumbnail = models.OneToOneField(
        'media.Image', related_name='profile_of_thumbnail', null=True)
    profile_image_standard = models.OneToOneField(
        'media.Image', related_name='profile_of_standard', null=True)

    def __unicode__(self):
        return u'Profile of a user: %s' % self.user.username

    def full_name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def age(self):
        if self.birthday is None:
            return 0
        else:
            age = now().year - self.birthday.year
        if self.birthday > now() - relativedelta(years=age):
            age -= 1
        return age

    def reset_notification_date(self):
        self.last_notification = now()
        self.save()

    # return all active and accepted friends for current UserProfile
    def friends(self):
        return (self.to_friends.filter(from_friendships__from_user=self,
                                       from_friendships__is_active=1,
                                       from_friendships__was_accepted=1) |
                self.from_friends.filter(to_friendships__to_user=self,
                                         to_friendships__is_active=1,
                                         to_friendships__was_accepted=1)
                ).distinct()

    def subscriptions(self):
        return self.to_subscribers.filter(
            from_usersubscriptions__is_active=True)

    def total_subscriptions(self):  # return total number of subscriptions
        return self.to_subscribers.filter(
            from_usersubscriptions__is_active=True).count()

    def subscribers(self):
        return self.from_subscribers.filter(
            to_usersubscriptions__is_active=True)

    def total_subscribers(self):  # return total number of subscribers
        return self.from_subscribers.filter(
            to_usersubscriptions__is_active=True).count()

    # return total number of active images the user uploaded
    def total_images(self):
        return self.image_set.filter(is_active=True).count()

    # return total number of wordboxes the user has created
    def total_wordboxes(self):
        return self.wordbox_set.filter(is_active=True).count()

    # return all active and accepted friends for current UserProfile
    def notifications(self):
        return self.from_notifications.filter(is_active=True)

    def all_friendships(self):  # return all friends for current UserProfile
        return self.from_friends.all() | self.to_friends.all()

    # This member function can get user profile object from django user pk
    #b = models.UserProfile().get_UserProfile(2)
    def get_UserProfile(self, pk):
        try:
            UserProfile_obj = UserProfile.objects.get(user=pk)
        except UserProfile.DoesNotExist:
            UserProfile_obj = UserProfile()
            try:
                User_obj = User.objects.get(id=pk)

                class request:
                    POST = {u'username': User_obj.username,
                            u'first_name': User_obj.first_name,
                            u'last_name': User_obj.last_name,
                            u'email': User_obj.email}
                UserProfile_obj.create(request, User_obj)
                return UserProfile_obj
            except User.DoesNotExist:
                return UserProfile_obj
        return UserProfile_obj

    def register_device(self, device_token, device_type, hw_addr):
        ''' Register a portable device to the database,
            and the 3rd party provider

            Arguments:
            device_token - push token for the device
            device_type - iphone, android
            hw_addr - Unique string to identify the device (MAC address)

        '''
        try:
            tokens = json.loads(self.device_tokens)
        except ValueError:
            self.device_tokens = {}
            self.save()
            raise ValueError(
                'Can not load the device_tokens, reset to empty.'
            )

        if tokens.keys().__len__() >= Maximum_Portable_Devices_Per_User:
            print "Raise something here"

        if not device_token in tokens:
            tokens[device_token] = {
                'last_registration': now().replace(microsecond=0).isoformat(),
                'device_type': device_type,
                'hw_addr': hw_addr
            }

        self.device_tokens = json.dumps(tokens)
        self.save()

    def unregister_device(self, device_token):
        ''' Unregister a portable device from the database,
            and 3rd party provider

            Arguments:
            device_token - push token for the device

        '''
        try:
            tokens = json.loads(self.device_tokens)
        except ValueError:
            self.device_tokens = {}
            self.save()
            raise ValueError(
                'Can not load the device_tokens, reset to empty.'
            )

        if device_token in tokens:
            del tokens[device_token]
        else:
            raise ObjectDoesNotExist('The device_token doesn\'t exist.')

        self.device_tokens = json.dumps(tokens)
        self.save()

    def get_devices(self):
        ''' Get all the portable devices of a user.

            For example, it returns the following dictionary:
            {
                "device_token": {
                    "last_registration": "2009-11-06 20:41:06",
                    "device_type": "android"
                    "hw_addr": "08:ed:b9:25:e0:2e"
                }
            }

        '''
        try:
            return json.loads(self.device_tokens)
        except ValueError:
            self.device_tokens = {}
            self.save()
            raise ValueError(
                'Can not load the device_tokens, reset to empty.'
            )


class Notification(DujourDefaultModel):
    uuid = models.CharField(
        max_length=36, unique=True, default=create_uuid)
    from_user = models.ForeignKey(
        UserProfile, related_name='to_notifications')
    to_user = models.ForeignKey(
        UserProfile, related_name='from_notifications')
    is_active = models.BooleanField(default=True)
    was_read = models.BooleanField(default=False)
    IPaddress = models.GenericIPAddressField()
    created_time = models.DateTimeField(default=now)
    updated_time = models.DateTimeField(default=now)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    # relationships
    resource = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.pk


class UserSubscription(DujourDefaultModel):
    uuid = models.CharField(
        max_length=36, unique=True, default=create_uuid)
    from_user = models.ForeignKey(
        UserProfile, related_name='to_usersubscriptions')
    to_user = models.ForeignKey(
        UserProfile, related_name='from_usersubscriptions')
    created_time = models.DateTimeField(default=now)
    updated_time = models.DateTimeField(default=now)
    IPaddress = models.GenericIPAddressField()
    status = models.IntegerField(
        null=True)     # 1: accepted, 2: rejected, 3: unfriend
    is_active = models.BooleanField(default=True)


class Friendship(DujourDefaultModel):
    uuid = models.CharField(
        max_length=36, unique=True, default=create_uuid)
    from_user = models.ForeignKey(
        UserProfile, related_name='to_friendships')
    to_user = models.ForeignKey(
        UserProfile, related_name='from_friendships')
    updated_time = models.DateTimeField(default=now)
    created_time = models.DateTimeField(default=now)
    IPaddress = models.GenericIPAddressField()
    status = models.IntegerField(
        null=True)     # 1: accepted, 2: rejected, 3: unfriend
    is_active = models.BooleanField(default=True)
    was_accepted = models.BooleanField(default=True)

    # other relationships
    notification = generic.GenericRelation(Notification)

    def reset_notification(self):
        notification = self.notification.all()[0]
        notification.is_active = True
        notification.was_read = False
        notification.save()
        return True


class Community(DujourDefaultModel):
    uuid = models.CharField(
        max_length=36, unique=True, default=create_uuid)
    name = models.CharField(max_length=32)
    description = models.TextField(default='')
    updated_time = models.DateTimeField(default=now)
    created_time = models.DateTimeField(default=now)
    # The IP address user used when uploaded this photo
    IPaddress = models.GenericIPAddressField()
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)

    # relationships
    creator = models.ForeignKey(
        UserProfile, related_name='created_community_set')
    member_set = models.ManyToManyField(UserProfile,
                                        through='CommunityMembership',
                                        related_name='community_set')
# The creator of a community is automatically a member
#    total_members         = models.IntegerField(default=1)
    total_subscribers = models.IntegerField(default=1)
        # The creator of a community is automatically a subscriber
    total_admins = models.IntegerField(
        default=1)  # The creator of a community is automatically an admin
    total_collections = models.IntegerField(default=0)

    tags = TaggableManager()

    profile_image_thumbnail = models.OneToOneField(
        'media.Image', related_name='community_of_thumbnail', null=True)
    profile_image_standard = models.OneToOneField(
        'media.Image', related_name='community_of_standard', null=True)

    def total_images(self):
        return self.image_set.all().count()

    def total_wordboxes(self):
        return self.wordbox_set.all().count()

    def total_members(self):
        return self.member_set.all().count()

    def _total_posts(self):
        return self.total_images() + self.total_wordboxes()

    def delete(self):
        for membership in self.communitymembership_set.all():
            membership.is_active = False
            membership.save()
        return super(Community, self).delete()

    # extra fields
#    total_posts = property(_total_posts)


class CommunityCategory(DujourDefaultModel):
    uuid = models.CharField(
        max_length=36, unique=True, default=create_uuid)
    name = models.CharField(max_length=32)
    description = models.TextField(default='')
    updated_time = models.DateTimeField(default=now)
    created_time = models.DateTimeField(default=now)
    # The IP address user used when uploaded this photo
    IPaddress = models.GenericIPAddressField()
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)

    # relationships
    community_set = models.ManyToManyField(
        Community, related_name='communitycategory_set')

    def total_communities(self):
        return self.community_set.all().count()


class CommunityMembership(DujourDefaultModel):
    uuid = models.CharField(
        max_length=36, unique=True, default=create_uuid)
    kind = models.IntegerField(default=0)
    updated_time = models.DateTimeField(default=now)
    created_time = models.DateTimeField(default=now)
    is_active = models.BooleanField(default=True)
    last_visited = models.DateTimeField(default=now)

    # relationships
    community = models.ForeignKey(Community)
    member = models.ForeignKey(UserProfile)

    def __str__(self):
        return str(self.id)

    def reset_last_visited_date(self):
        self.last_visited = now()
        self.save()


def check_user_profile_exist_and_create_one_if_not_exist(user_obj):
    try:
        UserProfile.objects.get(user=user_obj)
    except UserProfile.DoesNotExist:
        user_profile_obj2 = UserProfile()
        user_profile_obj2.create_user(user_obj.username, user_obj)
        return False
    except UserProfile.MultipleObjectsReturned:
        return True
    return True
