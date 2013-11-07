""" URLconf

The Api URL dispatcher.

"""

from django.conf.urls import patterns, include
from tastypie.api import Api
from website.api.v1.user_resources import CommunityResource, \
    CommunityCategoryResource, CommunityMembershipResource, UserResource, \
    UsernameResource, MeResource, EmailResource, FriendshipResource, \
    UserSubscriptionResource, SubscriberResource
from website.api.v1.media_resources import ImageResource, WordBoxResource, \
    UserCollectionResource, MediaResource
from website.api.v1.action_resources import CommentResource, \
    CollectionResource, VoteResource, NewsfeedResource
from website.api.v1.brand_resources import BrandResource, ItemResource, \
    ItemTagResource

v1_api = Api(api_name='v1')
v1_api.register(BrandResource())
v1_api.register(CommentResource())
v1_api.register(CommunityResource())
v1_api.register(CommunityCategoryResource())
v1_api.register(CommunityMembershipResource())
v1_api.register(CollectionResource())
v1_api.register(UserResource())
v1_api.register(UsernameResource())
v1_api.register(MeResource())
v1_api.register(EmailResource())
v1_api.register(FriendshipResource())
v1_api.register(UserSubscriptionResource())
v1_api.register(SubscriberResource())
v1_api.register(VoteResource())
v1_api.register(NewsfeedResource())
v1_api.register(ImageResource())
v1_api.register(WordBoxResource())
v1_api.register(MediaResource())
v1_api.register(UserCollectionResource())
v1_api.register(ItemResource())
v1_api.register(ItemTagResource())

urlpatterns = patterns('',
                       (r'', include(v1_api.urls)),
                       )
