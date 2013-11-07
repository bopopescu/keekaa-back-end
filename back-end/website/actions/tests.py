import datetime

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.utils import simplejson as json
from django.test import TestCase
from tastypie.test import TestApiClient
client = TestApiClient()
from tastypie.test import ResourceTestCase
from website.library.default_functions import create_uuid
from website.library.helper_functions import parse_uri, construct_detail_uri, \
    construct_list_uri
from website.library.validators import is_valid_uri
from website.api.v1.action_resources import *
from website.api.v1.media_resources import *
from website.api.v1.user_resources import *
from website.api.v1.brand_resources import *
from website.actions.models import *
from website.users.models import *
from website.media.models import *
from website.brands.models import *


class CommentResourceTest(TestCase):
    '''
        Test the API for CommentResource
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
        self.resource_name = CommentResource._meta.resource_name
        self.image = []
        self.user = []
        self.userprofile = []
        self.comment = []

        # 2 Users
        self.user.append(User.objects.create(username='derek', password='pbkdf2_sha256$10000$dHTAmULqmZJ0$184sglB5QqBMVaWa4Xy8MlkPgHJ7nBo2j0NLTW/xHkM='))
        self.userprofile.append(UserProfile.objects.create(uuid=create_uuid(),
                                                           username='derek', first_name='Derek', middle_name='', last_name='Chang',
                                                           email='derek@dujour.im',
                                                           user=self.user[-1]))
        self.user.append(User.objects.create(username='michael', password='pbkdf2_sha256$10000$dHTAmULqmZJ0$184sglB5QqBMVaWa4Xy8MlkPgHJ7nBo2j0NLTW/xHkM='))
        self.userprofile.append(UserProfile.objects.create(uuid=create_uuid(),
                                                           username='zikegcwk', first_name='Michael', middle_name='', last_name='Zhang',
                                                           email='michael@dujour.im',
                                                           user=self.user[-1]))
        # 2 Images
        self.image.append(Image.objects.create(uuid=create_uuid(),
                                               title='image1', IPaddress='127.0.0.1',
                                               owner=self.userprofile[0]))
        self.image.append(Image.objects.create(uuid=create_uuid(),
                                               title='image2', IPaddress='127.0.0.1',
                                               owner=self.userprofile[1]))
        # 3 Comment
        self.comment.append(Comment.objects.create(uuid=create_uuid(),
                                                   message='comment by 1st User', IPaddress='127.0.0.1',
                                                   parent=self.image[0], owner=self.userprofile[0]))
        self.comment.append(Comment.objects.create(uuid=create_uuid(),
                                                   message='comment by 1st User', IPaddress='127.0.0.1',
                                                   parent=self.image[0], owner=self.userprofile[0]))
        self.comment.append(Comment.objects.create(uuid=create_uuid(),
                                                   message='comment by 2nd User', IPaddress='127.0.0.1',
                                                   parent=self.image[1], owner=self.userprofile[1]))

        # Define what Comment fields can be modified
        self.fields = {'parent': True,
                       'message': True,
                       'owner': False,
                       'created_time': False,
                       'name': False,
                       'username': False,
                       'resource_uri': False,
                       'total_votes': False}

        self.list_uri = construct_list_uri(
            version=self.api, resource=self.resource_name)
        self.detail_uri = construct_detail_uri(version=self.api,
                                               resource=self.resource_name, uuid=self.comment[0].uuid)

    def test_GET_detail(self):
        '''
        Test GET request to the detail endpoint.
        Check if the returned fields are correct.
        Also check for proper filtering.
        '''

        # sign in ?

        comment = self.comment[0]

        # GET comment detail
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
        self.assertEqual(GET_data['username'], comment.owner.username,
                         'Value for Field \'username\' is incorrect.')
        self.assertEqual(GET_data['name'], comment.owner.full_name(
        ), 'Value for Field \'name\' is incorrect.')
        self.assertEqual(GET_data['message'], comment.message,
                         'Value for Field \'message\' is incorrect.')
        self.assertEqual(GET_data['total_votes'], comment.total_votes,
                         'Value for Field \'total_votes\' is incorrect.')
        t = comment.created_time
        # take out microsecond and use timezone javascript standard
        self.assertEqual(GET_data['created_time'],
                         datetime.datetime(t.year, t.month, t.day, t.hour, t.minute, t.second, 0, t.tzinfo).isoformat(),
                         'Value for Field \'created_time\' is incorrect.')
        owner_uri = construct_detail_uri(version=self.api, resource=UserResource._meta.resource_name, uuid=comment.owner.uuid)
        self.assertEqual(GET_data['owner'], owner_uri,
                         'Value for Field \'owner\' is incorrect.')
        parent_uri = construct_detail_uri(version=self.api, resource=comment.parent.obj_type(), uuid=comment.parent.uuid)
        self.assertEqual(GET_data['parent'], parent_uri,
                         'Value for Field \'parent\' is incorrect.')
        resource_uri = construct_detail_uri(version=self.api,
                                            resource=self.resource_name, uuid=comment.uuid)
        self.assertEqual(GET_data['resource_uri'], resource_uri,
                         'Value for Field \'resource_uri\' is incorrect.')

    def test_GET_list(self):
        '''
            Test GET request to the list endpoint. Check if the returned fields are correct.
        '''

        # sign in ?

        comment = self.comment[0]
        parent = self.image[0]

        # GET comment list
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
        self.assertEqual(len(GET_data['objects']), Comment.objects.filter(is_active=True).count(), 'Number of returned elements does not match number of objects in the database')

        # Filters
        # parent
        parent_uri = construct_detail_uri(
            version=self.api, resource='image', uuid=parent.uuid)
        # set limit=0 so that all the objects are returned (not paginated)
        resp = client.get('{comment_uri}?parent={parent_uri}&limit=0'.format(
            comment_uri=self.list_uri, parent_uri=parent_uri))
        # check status code if object was successfully received
        self.assertEqual(resp.status_code, 200, 'Status code should be 200. Instead, it is {status_code}.'.format(status_code=resp.status_code))
        GET_data = json.loads(resp.content)
        # check if the the number of filtered objects is correct
        filtered_comment_uuids = Comment.objects.filter(is_active=True, object_id=parent.pk, content_type=ContentType.objects.get_for_model(parent)).values_list('uuid', flat=True)
        self.assertEqual(len(GET_data['objects']), filtered_comment_uuids.count(), 'Number of returned filtered elements does not match number of filtered objects in the database')
        # check that the objects in the list is what you would get from the database
        for obj in GET_data['objects']:
            uuid = parse_uri(obj['resource_uri'])['uuid']
            self.assertTrue(uuid in filtered_comment_uuids, 'Returned object in list does not match any returned object from the database')

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

        # POST a new comment to the backend
        comment = self.comment[0]
        user = self.userprofile[0]

        # sign in
        sign_in_resp = client.get('/{version}/me/'.format(version=self.api), data={"user": user.username, "password": "dbdczk", "stay_signed_in": "True"})
        # check that sign-in was successful
        self.assertEqual(sign_in_resp.status_code, 200, 'Status code should be 200. Instead, it is {status_code}.'.format(status_code=sign_in_resp.status_code))

        # record initial number of comment objects
        initial_num_comments = Comment.objects.filter(is_active=True).count()

        # create test object to POST to the server
        new_parent = comment.parent
        new_owner = self.userprofile[0]
        parent_uri = construct_detail_uri(version=self.api,
                                          resource=comment.parent.obj_type(), uuid=new_parent.uuid)
        owner_uri = construct_detail_uri(version=self.api, resource=UserResource._meta.resource_name, uuid=user.uuid)
        POST_data = {'parent': parent_uri, 'owner': owner_uri,
                     'message': 'my test POST comment'}

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
        self.assertEqual(POST_data['message'], GET_data['message'], 'GET Value for Field \'message\' differs from POSTed Value')
        self.assertEqual(POST_data['parent'], GET_data['parent'], 'GET Value for Field \'parent\' differs from POSTed Value')
        self.assertEqual(POST_data['owner'], GET_data['owner'],
                         'GET Value for Field \'owner\' differs from POSTed Value')

        # check that the number of comments has increased by 1
        final_num_comments = Comment.objects.filter(is_active=True).count()
        self.assertEqual(initial_num_comments + 1, final_num_comments,
                         'Total number of objects (after posting) is not correct')

    def test_PATCH_detail(self):
        '''
            Test PATCH request to the detail endpoint. Check if specific fields have been updated successfully.
        '''

        # sign in
        sign_in_resp = client.get('/{0}/me/'.format(self.api), data={"user": self.userprofile[0].username, "password": "dbdczk", "stay_signed_in": "True"})
        # check that sign-in was successful
        self.assertEqual(sign_in_resp.status_code, 200, 'Status code should be 200. Instead, it is {status_code}.'.format(status_code=sign_in_resp.status_code))

        comment = self.comment[0]

        # create test object to PATCH to the server
        parent_uri = construct_detail_uri(version=self.api, resource=ImageResource._meta.resource_name, uuid=self.image[1].uuid)
        owner_uri = construct_detail_uri(version=self.api, resource=UserResource._meta.resource_name, uuid=self.userprofile[1].uuid)
        message = 'my test PATCH comment'
        t = comment.created_time

        PATCH_data = {'parent': parent_uri,
                      'owner': owner_uri,
                      'message': message,
                      'created_time': datetime.datetime(1, 1, 1, 0, 0, 0, 0, t.tzinfo).isoformat(),
                      'name': 'NA',
                      'username': 'NA',
                      'resource_uri': 'NA',
                      'total_votes': -1}

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
            Test DELETE request to the detail endpoint. Check if the comment has been deleted successfully.
        '''

        # sign in

        comment = self.comment[0]

        # record initial number of comment objects
        initial_num_comments = Comment.objects.filter(is_active=True).count()

        # DELETE resource uri:
        resp = client.delete(self.detail_uri, data=None)

        # check for successful delete status code
        self.assertEqual(resp.status_code, 204, 'Status code should be 204. Instead, it is {status_code}.'.format(status_code=resp.status_code))

        # check to see the object has been deactivated (i.e. is_active=False)
        self.assertFalse(Comment.objects.get(pk=comment.pk).is_active, 'Resource was not deleted successfully. \'is_active\' is still True')

        # check that the number of comments has decreased by 1
        final_num_comments = Comment.objects.filter(is_active=True).count()
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


class VoteResourceTest(TestCase):
    '''
        Test the API for CommentResource
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
        self.resource_name = VoteResource._meta.resource_name
        self.image = []
        self.user = []
        self.userprofile = []
        self.vote = []

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
        # 3 Images
        self.image.append(Image.objects.create(uuid=create_uuid(),
                                               title='image1', IPaddress='127.0.0.1',
                                               owner=self.userprofile[0]))
        self.image.append(Image.objects.create(uuid=create_uuid(),
                                               title='image2', IPaddress='127.0.0.1',
                                               owner=self.userprofile[1]))
        self.image.append(Image.objects.create(uuid=create_uuid(),
                                               title='image3', IPaddress='127.0.0.1',
                                               owner=self.userprofile[1]))

        # 1 Vote
        self.vote.append(Vote.objects.create(uuid=create_uuid(),
                                             IPaddress='127.0.0.1',
                                             parent=self.image[0], owner=self.userprofile[0]))
        self.vote.append(Vote.objects.create(uuid=create_uuid(),
                                             IPaddress='127.0.0.1',
                                             parent=self.image[1], owner=self.userprofile[0]))

        # Define what Vote fields can be modified
        self.fields = {'name': False,
                       'username': False,
                       'owner': False,
                       'created_time': False,
                       'parent': False,
                       'resource_uri': False}

        self.list_uri = construct_list_uri(
            version=self.api, resource=self.resource_name)
        self.detail_uri = construct_detail_uri(version=self.api,
                                               resource=self.resource_name, uuid=self.vote[0].uuid)

    def test_GET_detail(self):
        '''
            Test GET request to the detail endpoint. Check if the returned fields are correct.
            Also check for proper filtering.
        '''

        # sign in ?

        vote = self.vote[0]

        # GET Vote detail
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
        self.assertEqual(GET_data['username'], vote.owner.username,
                         'Value for Field \'username\' is incorrect.')
        self.assertEqual(GET_data['name'], vote.owner.full_name(
        ), 'Value for Field \'name\' is incorrect.')
        t = vote.created_time
        # take out microsecond and use timezone javascript standard
        self.assertEqual(GET_data['created_time'],
                         datetime.datetime(t.year, t.month, t.day, t.hour, t.minute, t.second, 0, t.tzinfo).isoformat(),
                         'Value for Field \'created_time\' is incorrect.')
        owner_uri = construct_detail_uri(version=self.api, resource=UserResource._meta.resource_name, uuid=vote.owner.uuid)
        self.assertEqual(GET_data['owner'], owner_uri,
                         'Value for Field \'owner\' is incorrect.')
        parent_uri = construct_detail_uri(version=self.api,
                                          resource=vote.parent.obj_type(), uuid=vote.parent.uuid)
        self.assertEqual(GET_data['parent'], parent_uri,
                         'Value for Field \'parent\' is incorrect.')
        resource_uri = construct_detail_uri(version=self.api,
                                            resource=self.resource_name, uuid=vote.uuid)
        self.assertEqual(GET_data['resource_uri'], resource_uri,
                         'Value for Field \'resource_uri\' is incorrect.')

    def test_GET_list(self):
        '''
            Test GET request to the list endpoint. Check if the returned fields are correct.
        '''

        # sign in ?

        vote = self.vote[0]
        parent = self.image[0]

        # GET Vote list
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
        self.assertEqual(len(GET_data['objects']), Vote.objects.filter(is_active=True).count(), 'Number of returned elements does not match number of objects in the database')

        # Filters
        # parent
        parent_uri = construct_detail_uri(
            version=self.api, resource='image', uuid=parent.uuid)
        # set limit=0 so that all the objects are returned (not paginated)
        resp = client.get('{vote_uri}?parent={parent_uri}&limit=0'.format(
            vote_uri=self.list_uri, parent_uri=parent_uri))
        # check status code if object was successfully received
        self.assertEqual(resp.status_code, 200, 'Status code should be 200. Instead, it is {status_code}.'.format(status_code=resp.status_code))
        GET_data = json.loads(resp.content)
        # check if the the number of filtered objects is correct
        filtered_vote_uuids = Vote.objects.filter(is_active=True, object_id=parent.pk, content_type=ContentType.objects.get_for_model(parent)).values_list('uuid', flat=True)
        self.assertEqual(len(GET_data['objects']), filtered_vote_uuids.count(), 'Number of returned filtered elements does not match number of filtered objects in the database')
        # check that the objects in the list is what you would get from the database
        for obj in GET_data['objects']:
            uuid = parse_uri(obj['resource_uri'])['uuid']
            self.assertTrue(uuid in filtered_vote_uuids, 'Returned object in list does not match any returned object from the database')

        # Filters
        # parent & owner
        parent_uri_list = [construct_detail_uri(version=self.api,
                                                resource='image', uuid=im.uuid) for im in self.image]
        parent_id_list = [im.pk for im in self.image]
        owner = self.userprofile[0]
        owner_uri = construct_detail_uri(version=self.api, resource=UserResource._meta.resource_name, uuid=owner.uuid)
        # set limit=0 so that all the objects are returned (not paginated)
        resp = client.get('{vote_uri}?owner={owner_uri}&parent={parent_uri0},{parent_uri1},{parent_uri2}&limit=0'.format(vote_uri=self.list_uri, owner_uri=owner_uri, parent_uri0=parent_uri_list[0], parent_uri1=parent_uri_list[1], parent_uri2=parent_uri_list[2]))
        # check status code if object was successfully received
        self.assertEqual(resp.status_code, 200, 'Status code should be 200. Instead, it is {status_code}.'.format(status_code=resp.status_code))
        GET_data = json.loads(resp.content)
        # check if the the number of filtered objects is correct
        filtered_vote_uuids = Vote.objects.filter(is_active=True, owner=owner, object_id__in=parent_id_list, content_type=ContentType.objects.get_for_model(parent)).values_list('uuid', flat=True)
        self.assertEqual(len(GET_data['objects']), filtered_vote_uuids.count(), 'Number of returned filtered elements does not match number of filtered objects in the database')
        # check that the objects in the list is what you would get from the database
        for obj in GET_data['objects']:
            uuid = parse_uri(obj['resource_uri'])['uuid']
            self.assertTrue(uuid in filtered_vote_uuids, 'Returned object in list does not match any returned object from the database')

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

        # POST a new Vote to the backend
        vote = self.vote[0]
        user = self.userprofile[0]
        # sign in
        sign_in_resp = client.get('/{version}/me/'.format(version=self.api), data={"user": user.username, "password": "dbdczk", "stay_signed_in": "True"})
        # check that sign-in was successful
        self.assertEqual(sign_in_resp.status_code, 200, 'Status code should be 200. Instead, it is {status_code}.'.format(status_code=sign_in_resp.status_code))

        # record initial number of Vote objects
        initial_num_votes = Vote.objects.filter(is_active=True).count()

        ### Test POST Vote on a parent object that already has a Vote from this user. The total number votes should remain the same.

        # create test object to POST to the server
        new_parent = vote.parent
        parent_uri = construct_detail_uri(version=self.api,
                                          resource=vote.parent.obj_type(), uuid=new_parent.uuid)
        owner_uri = construct_detail_uri(version=self.api, resource=UserResource._meta.resource_name, uuid=user.uuid)
        POST_data = {'parent': parent_uri}

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
        self.assertEqual(POST_data['parent'], GET_data['parent'], 'GET Value for Field \'parent\' differs from POSTed Value')
        self.assertEqual(GET_data['owner'], owner_uri,
                         'GET Value for Field \'owner\' differs from POSTed Value')

        # check that the number of Votes has increased by 1
        final_num_votes = Vote.objects.filter(is_active=True).count()
        self.assertEqual(initial_num_votes, final_num_votes,
                         'Total number of objects (after posting) is not correct')

        ### Test POST Vote on a parent object that does not have a Vote from this user. The total number votes should increase by 1.

        # create test object to POST to the server
        new_parent = self.image[2]
        new_owner = self.userprofile[0]
        parent_uri = construct_detail_uri(version=self.api,
                                          resource=new_parent.obj_type(), uuid=new_parent.uuid)
        owner_uri = construct_detail_uri(version=self.api, resource=UserResource._meta.resource_name, uuid=new_owner.uuid)
        POST_data = {'parent': parent_uri}

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
        self.assertEqual(POST_data['parent'], GET_data['parent'], 'GET Value for Field \'parent\' differs from POSTed Value')
        self.assertEqual(GET_data['owner'], owner_uri,
                         'GET Value for Field \'owner\' differs from POSTed Value')

        # check that the number of Votes has increased by 1
        final_num_votes = Vote.objects.filter(is_active=True).count()
        self.assertEqual(initial_num_votes + 1, final_num_votes,
                         'Total number of objects (after posting) is not correct')

    def test_PATCH_detail(self):
        '''
            Test PATCH request to the detail endpoint.
            This method is not allowed.
        '''

        # PATCH object to list URI
        resp = client.patch(self.detail_uri, data={})
        # check status is 405: Method Not Allowed
        self.assertEqual(resp.status_code, 405, 'Status code should be 405. Instead, it is {status_code}.'.format(status_code=resp.status_code))

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
            Test DELETE request to the detail endpoint. Check if the vote has been deleted successfully.
        '''

        # sign in

        vote = self.vote[0]

        # record initial number of Vote objects
        initial_num_votes = Vote.objects.filter(is_active=True).count()

        # DELETE resource uri:
        resp = client.delete(self.detail_uri, data=None)

        # check for successful delete status code
        self.assertEqual(resp.status_code, 204, 'Status code should be 204. Instead, it is {status_code}.'.format(status_code=resp.status_code))

        # check to see the object has been deactivated (i.e. is_active=False)
        self.assertFalse(Vote.objects.get(pk=vote.pk).is_active, 'Resource was not deleted successfully. \'is_active\' is still True')

        # check that the number of Votes has decreased by 1
        final_num_votes = Vote.objects.filter(is_active=True).count()
        self.assertEqual(initial_num_votes - 1, final_num_votes,
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
