import datetime
from django.http import HttpRequest
from django.utils import simplejson as json
from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import TestApiClient
client = TestApiClient()
from tastypie.test import ResourceTestCase
from website.library.default_functions import create_uuid
from website.library.helper_functions import parse_uri, construct_detail_uri, \
    construct_list_uri, construct_filter_uri
from website.library.validators import is_valid_uri
from website.api.v1.action_resources import *
from website.api.v1.media_resources import *
from website.api.v1.user_resources import *
from website.api.v1.brand_resources import *
from website.actions.models import *
from website.users.models import *
from website.media.models import *
from website.brands.models import *


class ItemResourceTest(TestCase):
    '''
        Test the API for ItemTagResource
        test_GET_detail
        test_GET_list
        test_POST_detail
        test_POST_list
        test_PATCH_detail
        test_PATCH_list
        test_POST_detail
        test_POST_list
        test_DELETE_detail
        test_DELETE_list
    '''

    def setUp(self):
        self.api = 'v1'
        self.resource_name = ItemResource._meta.resource_name
        self.image = []
        self.user = []
        self.userprofile = []
        self.comment = []
        self.vote = []
        self.item = []

        # 2 Users
        self.user.append(User.objects.create(username='derek', password='pbkdf2_sha256$10000$dHTAmULqmZJ0$184sglB5QqBMVaWa4Xy8MlkPgHJ7nBo2j0NLTW/xHkM='))  # self.user1.set_password('dc')
        self.userprofile.append(UserProfile.objects.create(uuid=create_uuid(),
                                                           username='derek', first_name='Derek', middle_name='', last_name='Chang',
                                                           email='derek@dujour.im',
                                                           user=self.user[-1]))
        self.user.append(User.objects.create(username='michael', password='pbkdf2_sha256$10000$dHTAmULqmZJ0$184sglB5QqBMVaWa4Xy8MlkPgHJ7nBo2j0NLTW/xHkM='))
#        self.user2.set_password('zk')
        self.userprofile.append(UserProfile.objects.create(uuid=create_uuid(),
                                                           username='zikegcwk', first_name='Michael', middle_name='', last_name='Zhang',
                                                           email='michael@dujour.im',
                                                           user=self.user[-1]))
        # 1 Images
        self.image.append(Image.objects.create(uuid=create_uuid(),
                                               title='image1', IPaddress='127.0.0.1',
                                               owner=self.userprofile[0]))
        self.image.append(Image.objects.create(uuid=create_uuid(),
                                               title='image2', IPaddress='127.0.0.1',
                                               owner=self.userprofile[0]))
#        # 1 Brand
#        self.brand.append(Brand.objects.create(uuid=create_uuid(),
#                                        name='Levis',IPaddress='127.0.0.1',
#                                        description='clothing retailer',
#                                        address='somwhere',
#                                        url_name='www.levis.com',
#                                        owner=self.userprofile[0]))

        # 1 Item
        self.item.append(Item.objects.create(uuid=create_uuid(),
                                             name='shirt', IPaddress='127.0.0.1',
                                             owner=self.userprofile[0],
                                             brand_name='Express',
                                             color='black',
                                             description='a nice t-shirt',
                                             price='39.99',
                                             size='M',
                                             url='www.express.com'))

        # 1 Comment
        self.comment.append(Comment.objects.create(uuid=create_uuid(),
                                                   message='comment for Item 1 by User 1', IPaddress='127.0.0.1',
                                                   parent=self.item[0], owner=self.userprofile[0]))

        # 1 Vote
        self.vote.append(Vote.objects.create(uuid=create_uuid(),
                                             IPaddress='127.0.0.1',
                                             parent=self.item[0], owner=self.userprofile[0]))

        # Define what Item fields can be modified
        self.fields = {'name': True,
                       'owner': True,
                       'brand_name': False,
                       'description': False,
                       'size': False,
                       'price': False,
                       'color': False,
                       'url': False,
                       'total_votes': False,
                       'total_comments': False,
                       'comment': False,
                       'vote': False,
                       'created_time': False,
                       'updated_time': False,
                       'resource_uri': False}

        self.list_uri = construct_list_uri(
            version=self.api, resource=self.resource_name)
        self.detail_uri = construct_detail_uri(version=self.api,
                                               resource=self.resource_name, uuid=self.item[0].uuid)

    def test_GET_detail(self):
        '''
            Test GET request to the detail endpoint. Check if the returned fields are correct.
            Also check for proper filtering.
        '''

        # sign in ?

        item = self.item[0]

        # GET Item detail
        resp = client.get(self.detail_uri, data=None)
        # check status code if object was successfully received
        self.assertEqual(resp.status_code, 200, 'Status code should be 200. Instead, it is {status_code}.'.format(status_code=resp.status_code))
        GET_data = json.loads(resp.content)

        # check the number of returned fields
        self.assertEqual(len(GET_data), len(self.fields), 'Total number of fields outputed is {wrong_num}. It should be {right_num}.'.format(wrong_num=len(GET_data), right_num=len(self.fields)))
        # make sure all the right fields are outputed in the API
        for key in self.fields:
            self.assertTrue(key in GET_data, 'Field \'{field}\' is not in the returned JSON object.'.format(field=key))

        # check the accuracy of each field
        self.assertEqual(GET_data['name'], item.name,
                         'Value for Field \'name\' is incorrect.')
        self.assertEqual(GET_data['brand_name'], item.brand_name,
                         'Value for Field \'brand_name\' is incorrect.')
        self.assertEqual(GET_data['description'], item.description,
                         'Value for Field \'description\' is incorrect.')
        self.assertEqual(GET_data['size'], item.size,
                         'Value for Field \'size\' is incorrect.')
        self.assertEqual(GET_data['color'], item.color,
                         'Value for Field \'color\' is incorrect.')
        self.assertEqual(GET_data['price'], item.price,
                         'Value for Field \'price\' is incorrect.')
        self.assertEqual(GET_data['url'], item.url,
                         'Value for Field \'price\' is incorrect.')
        self.assertEqual(GET_data['total_comments'], item.total_comments(
        ), 'Value for Field \'total_comments\' is incorrect.')
        self.assertEqual(GET_data['total_votes'], item.total_votes(
        ), 'Value for Field \'total_votes\' is incorrect.')
        # take out microsecond and use timezone javascript standard
        t = item.created_time
        self.assertEqual(GET_data['created_time'],
                         datetime.datetime(t.year, t.month, t.day, t.hour, t.minute, t.second, 0, t.tzinfo).isoformat(),
                         'Value for Field \'created_time\' is incorrect.')
        t = item.updated_time
        self.assertEqual(GET_data['updated_time'],
                         datetime.datetime(t.year, t.month, t.day, t.hour, t.minute, t.second, 0, t.tzinfo).isoformat(),
                         'Value for Field \'updated_time\' is incorrect.')
        owner_uri = construct_detail_uri(version=self.api, resource=UserResource._meta.resource_name, uuid=item.owner.uuid)
        self.assertEqual(GET_data['owner'], owner_uri,
                         'Value for Field \'owner\' is incorrect.')
        item_uri = construct_detail_uri(version=self.api,
                                        resource=ItemResource._meta.resource_name, uuid=item.uuid)
        comment_filter_uri = construct_filter_uri(version=self.api, resource=CommentResource._meta.resource_name, parameter='parent', filter_uri=item_uri)
        self.assertEqual(GET_data['comment'], comment_filter_uri,
                         'Value for Field \'comment\' is incorrect.')
        vote_filter_uri = construct_filter_uri(version=self.api, resource=VoteResource._meta.resource_name, parameter='parent', filter_uri=item_uri)
        self.assertEqual(GET_data['vote'], vote_filter_uri,
                         'Value for Field \'vote\' is incorrect.')
        resource_uri = construct_detail_uri(version=self.api,
                                            resource=self.resource_name, uuid=item.uuid)
        self.assertEqual(GET_data['resource_uri'], resource_uri,
                         'Value for Field \'resource_uri\' is incorrect.')


class ItemTagResourceTest(TestCase):
    '''
        Test the API for ItemTagResource
        test_GET_detail
        test_GET_list
        test_POST_detail
        test_POST_list
        test_PATCH_detail
        test_PATCH_list
        test_POST_detail
        test_POST_list
        test_DELETE_detail
        test_DELETE_list
    '''

    def setUp(self):
        self.api = 'v1'
        self.resource_name = ItemTagResource._meta.resource_name
        self.image = []
        self.user = []
        self.userprofile = []
        self.brand = []
        self.item = []
        self.itemtag = []

        # 2 Users
        self.user.append(User.objects.create(username='derek', password='pbkdf2_sha256$10000$dHTAmULqmZJ0$184sglB5QqBMVaWa4Xy8MlkPgHJ7nBo2j0NLTW/xHkM='))  # self.user1.set_password('dc')
        self.userprofile.append(UserProfile.objects.create(uuid=create_uuid(),
                                                           username='derek', first_name='Derek', middle_name='', last_name='Chang',
                                                           email='derek@dujour.im',
                                                           user=self.user[-1]))
        self.user.append(User.objects.create(username='michael', password='pbkdf2_sha256$10000$dHTAmULqmZJ0$184sglB5QqBMVaWa4Xy8MlkPgHJ7nBo2j0NLTW/xHkM='))
#        self.user2.set_password('zk')
        self.userprofile.append(UserProfile.objects.create(uuid=create_uuid(),
                                                           username='zikegcwk', first_name='Michael', middle_name='', last_name='Zhang',
                                                           email='michael@dujour.im',
                                                           user=self.user[-1]))
        # 1 Images
        self.image.append(Image.objects.create(uuid=create_uuid(),
                                               title='image1', IPaddress='127.0.0.1',
                                               owner=self.userprofile[0]))
        self.image.append(Image.objects.create(uuid=create_uuid(),
                                               title='image2', IPaddress='127.0.0.1',
                                               owner=self.userprofile[0]))
#        # 1 Brand
#        self.brand.append(Brand.objects.create(uuid=create_uuid(),
#                                        name='Levis',IPaddress='127.0.0.1',
#                                        description='clothing retailer',
#                                        address='somwhere',
#                                        url_name='www.levis.com',
#                                        owner=self.userprofile[0]))

        # 1 Item
        self.item.append(Item.objects.create(uuid=create_uuid(),
                                             name='shirt', IPaddress='127.0.0.1',
                                             owner=self.userprofile[0]))
        self.item.append(Item.objects.create(uuid=create_uuid(),
                                             name='pants', IPaddress='127.0.0.1',
                                             owner=self.userprofile[0]))

        # 1 ItemTag
        self.itemtag.append(ItemTag.objects.create(uuid=create_uuid(),
                                                   num=1, x=0, y=0, IPaddress='127.0.0.1',
                                                   owner=self.userprofile[0],
                                                   image=self.image[0],
                                                   item=self.item[0]))
        self.itemtag.append(ItemTag.objects.create(uuid=create_uuid(),
                                                   num=2, x=.5, y=.5, IPaddress='127.0.0.1',
                                                   owner=self.userprofile[0],
                                                   image=self.image[0],
                                                   item=self.item[1]))

        # Define what ItemTag fields can be modified
        self.fields = {'item': True,
                       'image': True,
                       'x': True,
                       'y': True,
                       'num': True,
                       'owner': False,
                       'created_time': False,
                       'updated_time': False,
                       'resource_uri': False}

        self.list_uri = construct_list_uri(
            version=self.api, resource=self.resource_name)
        self.detail_uri = construct_detail_uri(version=self.api,
                                               resource=self.resource_name, uuid=self.itemtag[0].uuid)

    def test_GET_detail(self):
        '''
            Test GET request to the detail endpoint. Check if the returned fields are correct.
            Also check for proper filtering.
        '''

        # sign in ?

        itemtag = self.itemtag[0]

        # GET ItemTag detail
        resp = client.get(self.detail_uri, data=None)
        # check status code if object was successfully received
        self.assertEqual(resp.status_code, 200, 'Status code should be 200. Instead, it is {status_code}.'.format(status_code=resp.status_code))
        GET_data = json.loads(resp.content)

        # check the number of returned fields
        self.assertEqual(len(GET_data), len(self.fields), 'Total number of fields outputed is {wrong_num}. It should be {right_num}.'.format(wrong_num=len(GET_data), right_num=len(self.fields)))
        # make sure all the right fields are outputed in the API
        for key in self.fields:
            self.assertTrue(key in GET_data, 'Field \'{field}\' is not in the returned JSON object.'.format(field=key))

        # check the accuracy of each field
        self.assertEqual(GET_data['num'], itemtag.num, 'Value for Field \'num\' is incorrect.')
        self.assertEqual(GET_data['x'], itemtag.x, 'Value for Field \'x\' is incorrect.')
        self.assertEqual(GET_data['y'], itemtag.y, 'Value for Field \'y\' is incorrect.')
        # take out microsecond and use timezone javascript standard
        t = itemtag.created_time
        self.assertEqual(GET_data['created_time'],
                         datetime.datetime(t.year, t.month, t.day, t.hour, t.minute, t.second, 0, t.tzinfo).isoformat(),
                         'Value for Field \'created_time\' is incorrect.')
        t = itemtag.updated_time
        self.assertEqual(GET_data['updated_time'],
                         datetime.datetime(t.year, t.month, t.day, t.hour, t.minute, t.second, 0, t.tzinfo).isoformat(),
                         'Value for Field \'updated_time\' is incorrect.')
        owner_uri = construct_detail_uri(version=self.api, resource=UserResource._meta.resource_name, uuid=itemtag.owner.uuid)
        self.assertEqual(GET_data['owner'], owner_uri,
                         'Value for Field \'owner\' is incorrect.')
        image_uri = construct_detail_uri(version=self.api, resource=itemtag.image.obj_type(), uuid=itemtag.image.uuid)
        self.assertEqual(GET_data['image'], image_uri,
                         'Value for Field \'image\' is incorrect.')
        item_uri = construct_detail_uri(version=self.api,
                                        resource=itemtag.item.obj_type(), uuid=itemtag.item.uuid)
        self.assertEqual(GET_data['item'], item_uri,
                         'Value for Field \'item\' is incorrect.')
        resource_uri = construct_detail_uri(version=self.api,
                                            resource=self.resource_name, uuid=itemtag.uuid)
        self.assertEqual(GET_data['resource_uri'], resource_uri,
                         'Value for Field \'resource_uri\' is incorrect.')

    def test_GET_list(self):
        '''
            Test GET request to the list endpoint. Check if the returned fields are correct.
        '''

        # sign in ?

        itemtag = self.itemtag[0]
        image = self.image[0]

        # GET ItemTag list
        resp = client.get('{list_uri}?limit=0'.format(
            list_uri=self.list_uri), data=None)
        # check status code if object was successfully received
        self.assertEqual(resp.status_code, 200, 'Status code should be 200. Instead, it is {status_code}.'.format(status_code=resp.status_code))
        GET_data = json.loads(resp.content)

        # check list dictionary
        self.assertTrue('meta' in GET_data,
                        'GET list should return a Field \'meta\'')
        self.assertTrue('objects' in GET_data,
                        'GET list should return a Field \'objects\'')
        # assuming tastypie GET list endpoint works...
        self.assertEqual(len(GET_data['objects']), ItemTag.objects.filter(is_active=True).count(), 'Number of returned elements does not match number of objects in the database')

        # Filters
        # Image
        image_uri = construct_detail_uri(
            version=self.api, resource='image', uuid=image.uuid)
        # set limit=0 so that all the objects are returned (not paginated)
        resp = client.get('{itemtag_uri}?image={image_uri}&limit=0'.format(
            itemtag_uri=self.list_uri, image_uri=image_uri))
        # check status code if object was successfully received
        self.assertEqual(resp.status_code, 200, 'Status code should be 200. Instead, it is {status_code}.'.format(status_code=resp.status_code))
        GET_data = json.loads(resp.content)
        # check if the the number of filtered objects is correct
        filtered_itemtag_uuids = ItemTag.objects.filter(is_active=True,
                                                        image=image).values_list('uuid', flat=True)
        self.assertEqual(len(GET_data['objects']), filtered_itemtag_uuids.count(), 'Number of returned filtered elements does not match number of filtered objects in the database')
        # check that the objects in the list is what you would get from the database

        for obj in GET_data['objects']:
            uuid = parse_uri(obj['resource_uri'])['uuid']
            self.assertTrue(uuid in filtered_itemtag_uuids, 'Returned object in list does not match any returned object from the database')

    def test_POST_detail(self):
        '''
            Test POST request to the detail endpoint.
            This method is not allowed.
        '''

        # POST object to list URI
        resp = client.post(self.detail_uri, data={})
        # check status is 405: Method Not Allowed
        self.assertEqual(resp.status_code, 405, 'Status code should be 405. Instead, it is {status_code}.'.format(status_code=resp.status_code))

    def test_POST_list(self):
        '''
            Test POST request to the list endpoint. Check if the posted information is correct.
        '''

        # POST a new itemtag to the backend
        user = self.userprofile[0]

        # sign in
        sign_in_resp = client.get('/{version}/me/'.format(version=self.api), data={"user": user.username, "password": "dbdczk", "stay_signed_in": "True"})
        # check that sign-in was successful
        self.assertEqual(sign_in_resp.status_code, 200, 'Status code should be 200. Instead, it is {status_code}.'.format(status_code=sign_in_resp.status_code))

        # record initial number of itemtag objects
        initial_num_itemtags = ItemTag.objects.filter(is_active=True).count()

        # create test object to POST to the server
        new_item = self.item[1]
        new_image = self.image[1]
        new_owner = user  # owner must be person who signs in. otherwise, it will be overwritten by default to be the person who signs in
        image_uri = construct_detail_uri(version=self.api, resource=ImageResource._meta.resource_name, uuid=new_image.uuid)
        item_uri = construct_detail_uri(version=self.api, resource=ItemResource._meta.resource_name, uuid=new_item.uuid)
        owner_uri = construct_detail_uri(version=self.api, resource=UserResource._meta.resource_name, uuid=new_owner.uuid)
        x = .7
        y = .8
        num = 1
        POST_data = {'image': image_uri, 'item': item_uri, 'owner':
                     owner_uri, 'num': num, 'x': x, 'y': y}

        # POST object to list URI
        resp = client.post(self.list_uri, data=POST_data)
        # check status code if object was successfully created
        self.assertEqual(resp.status_code, 201, 'Status code should be 201. Instead, it is {status_code}.'.format(status_code=resp.status_code))

        # URI of the new object that is created in the database
        new_uri = json.loads(resp.content)['resource_uri']
        # data of GETting new_uri
        GET_resp = client.get(new_uri, data=None)
        GET_data = json.loads(GET_resp.content)

        # make sure posted object exists
        self.assertEqual(resp.status_code, 201, 'Status code should be 201. Instead, it is {status_code}.'.format(status_code=resp.status_code))
        self.assertEqual(POST_data['image'], GET_data['image'],
                         'GET Value for Field \'image\' differs from POSTed Value')
        self.assertEqual(POST_data['item'], GET_data['item'],
                         'GET Value for Field \'item\' differs from POSTed Value')
        self.assertEqual(POST_data['owner'], GET_data['owner'],
                         'GET Value for Field \'owner\' differs from POSTed Value')
        self.assertEqual(POST_data['num'], GET_data['num'],
                         'GET Value for Field \'owner\' differs from POSTed Value')
        self.assertEqual(POST_data['x'], GET_data['x'],
                         'GET Value for Field \'x\' differs from POSTed Value')
        self.assertEqual(POST_data['y'], GET_data['y'],
                         'GET Value for Field \'y\' differs from POSTed Value')

        # check that the number of itemtags has increased by 1
        final_num_itemtags = ItemTag.objects.filter(is_active=True).count()
        self.assertEqual(initial_num_itemtags + 1, final_num_itemtags,
                         'Total number of objects (after posting) is not correct')

    def test_PATCH_detail(self):
        '''
            Test PATCH request to the detail endpoint. Check if specific fields have been updated successfully.
        '''

        # sign in
        sign_in_resp = client.get('/{0}/me/'.format(self.api), data={"user": self.userprofile[0].username, "password": "dbdczk", "stay_signed_in": "True"})
        # check that sign-in was successful
        self.assertEqual(sign_in_resp.status_code, 200, 'Status code should be 200. Instead, it is {status_code}.'.format(status_code=sign_in_resp.status_code))

        itemtag = self.itemtag[0]

        # create test object to PATCH to the server
        new_item = self.item[1]
        new_image = self.image[1]
        new_owner = self.userprofile[1]  # owner must be person who signs in. otherwise, it will be overwritten by default to be the person who signs in
        image_uri = construct_detail_uri(version=self.api, resource=ImageResource._meta.resource_name, uuid=new_image.uuid)
        item_uri = construct_detail_uri(version=self.api, resource=ItemResource._meta.resource_name, uuid=new_item.uuid)
        owner_uri = construct_detail_uri(version=self.api, resource=UserResource._meta.resource_name, uuid=new_owner.uuid)
        x = 1
        y = 1
        num = 100
        t = itemtag.created_time

        PATCH_data = {'item': item_uri,
                      'image': image_uri,
                      'x': y,
                      'y': x,
                      'num': num,
                      'owner': owner_uri,
                      'created_time': datetime.datetime(1, 1, 1, 0, 0, 0, 0, t.tzinfo).isoformat(),
                      'updated_time': datetime.datetime(1, 1, 1, 0, 0, 0, 0, t.tzinfo).isoformat(),
                      'resource_uri': 'NA'}

        # PATCH object to detail URI
        resp = client.patch(self.detail_uri, data=PATCH_data)

        # check status code if object was successfully updated
        self.assertEqual(resp.status_code, 202, 'Status code should be 202. Instead, it is {status_code}.'.format(status_code=resp.status_code))

        # URI of the new object that is created in the database
        new_uri = json.loads(resp.content)['resource_uri']

        # data of GETting new_uri
        GET_resp = client.get(new_uri, data=None)
        GET_data = json.loads(GET_resp.content)

        # make sure writable PATCHed fields are updated, unmodifiable fields are are not updated
        # if an AssertionError occurs here, check self.writeable_fields and verify the write permissions on that field
        for field, is_writable in self.fields.iteritems():
            if is_writable:
                # if the field is writable, show that the fields are updated
                self.assertEqual(PATCH_data[field], GET_data[field], 'GET Value for writable Field \'{field}\' differs from PATCHed Value. They should be the same.'.format(field=field))
            else:
                # if the field is not writable, show that the fields are not equal
                self.assertNotEqual(PATCH_data[field], GET_data[field], 'GET Value for non-writable Field \'{field}\' is the same as the PATCHed Value. They should be different.')

    def test_PATCH_list(self):
        '''
        Test PATCH request to the list endpoint.
        This method is not allowed.
        '''

        # PATCH object to list URI
        resp = client.patch(self.list_uri, data={})
        # check status is 405: Method Not Allowed
        self.assertEqual(resp.status_code, 405, 'Status code should be 405. Instead, it is {status_code}.'.format(status_code=resp.status_code))

    def test_PUT_detail(self):
        '''
            Test PUT request to the detail endpoint.
            This method is not allowed.
        '''
        # PUT object to list URI
        resp = client.put(self.list_uri, data={})
        # check status is 405: Method Not Allowed
        self.assertEqual(resp.status_code, 405, 'Status code should be 405. Instead, it is {status_code}.'.format(status_code=resp.status_code))

    def test_PUT_list(self):
        '''
            Test PUT request to the list endpoint.
            This method is not allowed.
        '''

        # PUT object to list URI
        resp = client.put(self.list_uri, data={})
        # check status is 405: Method Not Allowed
        self.assertEqual(resp.status_code, 405, 'Status code should be 405. Instead, it is {status_code}.'.format(status_code=resp.status_code))

    def test_DELETE_detail(self):
        '''
            Test DELETE request to the detail endpoint. Check if the object has been deleted successfully.
        '''

        # sign in

        itemtag = self.itemtag[0]

        # record initial number of itemtag objects
        initial_num_comments = ItemTag.objects.filter(is_active=True).count()

        # DELETE resource uri:
        resp = client.delete(self.detail_uri, data=None)

        # check for successful delete status code
        self.assertEqual(resp.status_code, 204, 'Status code should be 204. Instead, it is {status_code}.'.format(status_code=resp.status_code))

        # check to see the object has been deactivated (i.e. is_active=False)
        self.assertFalse(ItemTag.objects.get(pk=itemtag.pk).is_active, 'Resource was not deleted successfully. \'is_active\' is still True')

        # check that the number of itemtag has decreased by 1
        final_num_comments = ItemTag.objects.filter(is_active=True).count()
        self.assertEqual(initial_num_comments - 1, final_num_comments,
                         'Total number of objects (after deletion) is not correct')

    def test_DELETE_list(self):
        '''
            Test DELETE request to the detail endpoint.
            This method is not allowed.
        '''

        # DELETE object to list URI
        resp = client.delete(self.list_uri, data={})
        # check status is 405: Method Not Allowed
        self.assertEqual(resp.status_code, 405, 'Status code should be 405. Instead, it is {status_code}.'.format(status_code=resp.status_code))
