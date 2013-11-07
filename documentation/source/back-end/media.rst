********
Media
********

.. _media-images:

Images
======

Description
-----------

To post an image to the webserver, send a POST request to "/v1/image/" with a json object that has the "title" field in it. If the POST is successful, the header will contain a "Location" field with the new IMAGE_URI. To get information about te newly created image, send a GET request to "/v1/image/IMAGE_URI". The documentation is below.

Get information about an Image
------------------------------

You can get the following information about an Image by issuing a HTTP **GET** request to **/v1/image/IMAGE_ID**. The following is returned:

.. csv-table::
    :widths: 10 60 30
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "owner",             "URI for the user that created the comment",                "string"
    "title",             "Text representing the title",                              "string"
    "description",       "Description of the image",                                 "string"
    "created_time",      "The time the comment was created",                         "string, rfc-3339 standard"
    "updated_time",      "The time the comment was updated",                         "string, rfc-3339 standard"
    "obj_type",          "the type of resource",                                     "string"
    "resource_uri",      "URI of the current object",                                "string"
    "comment",           "URI for all the comments belonging to this Image",         "string"
    "vote",              "URI for all the vote belonging to this Image",             "string"
    "collection",        "All the collections this image belongs to",                "array"
    "has_owner",         "Is the ownder portrayed in the image",                     "boolean"
    "total_votes",       "The number of times this collection was voted on",         "integer"
    "total_comments",    "The number of comments for the image",                     "integer"
    "total_collected",   "The number of users that have collected the image",        "integer"
    "versions",          "Height, Width, URL information for different versions of the image",  "array"
..	"user_voted", "True if the session user voted on the collection", "boolean"

.. code-block:: js

    {
        "collection": [],
        "comment": "/v1/comment/?parent=/v1/image/30f8dc6c-57ab-5151-be3c-6d3d03781724/",
        "created_time": "2012-04-18 04:30:20",
        "description": "my first image description",
        "has_owner": false,
        "obj_type": "image",
        "owner": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
        "resource_uri": "/v1/image/30f8dc6c-57ab-5151-be3c-6d3d03781724/",
        "title": "adfasdfasdfads TITLE",
        "total_comments": 0,
        "total_favorites": 0,
        "total_votes": 0,
        "updated_time": "2012-04-18 04:30:20",
        "versions": [
            {
                "height": 803,
                "resource_uri": "https://d956iao6yp65z.cloudfront.net/images/1322037362_6266c855-e043-5237-9508-c827577341db_0535x0803.jpg",
                "width": 535
            },
            {
                "height": 401,
                "resource_uri": "https://d956iao6yp65z.cloudfront.net/images/1322037362_6266c855-e043-5237-9508-c827577341db_0535x0803.jpg",
                "width": 267
            },
            {
                "height": 200,
                "resource_uri": "https://d956iao6yp65z.cloudfront.net/images/1322037362_6266c855-e043-5237-9508-c827577341db_0535x0803.jpg",
                "width": 133
            },
            {
                "height": 100,
                "resource_uri": "https://d956iao6yp65z.cloudfront.net/images/1322037362_6266c855-e043-5237-9508-c827577341db_0535x0803.jpg",
                "width": 66
            }
        ]
    }

Get all Images belonging to a User
----------------------------------

You can get all the Images belonging to a User by issuing a HTTP **GET** request to **/v1/image/** with the following parameters


.. csv-table::
    :widths: 10 60 10 20
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "owner",            "URI of the user object",                          "string",           "yes" 
    "offset",           "The index of the first object after the query has been ordered",      "integer", "no"
    "limit",            "The number of comments to be returned after all comments are ordered. Default = "all comments", "string", "no"
    "order_by",         "The default is "-created_time" where the '-' signifies reverse chronological order.",   "string", "no"

Example code:

.. code-block:: js

    /v1/image/?owner=/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/

The following JSON object is returned:

.. csv-table::
    :widths: 20 70 10
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "meta",              "Information regarding the query: 'limit' 'next' 'offset' 'previous', 'total_count'," "string"
    "object",            "Array of returned objects",                                "Array"

Example code:

.. code-block:: js

    {
        "meta": {
            "limit": 20,
            "next": null,
            "offset": 0,
            "previous": null,
            "total_count": 2
        },
    "objects": [{
        "collection": [],
        "comment": "/v1/comment/?parent=/v1/image/b62fb9b4-9c13-50c3-8c85-2c87e96553b3/",
        "created_time": "2011-11-22 10:46:39",
        "description": "my first image description",
        "has_owner": false,
        "obj_type": "image",
        "owner": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
        "resource_uri": "/v1/image/b62fb9b4-9c13-50c3-8c85-2c87e96553b3/",
        "title": "adfasdfasdfads TITLE",
        "total_comments": 25,
        "total_favorites": 1,
        "total_votes": 3,
        "updated_time": "2012-03-29 03:38:38",
        "versions": [
        ...
        ]
    }, {
        "collection": [],
        "comment": "/v1/comment/?parent=/v1/image/e14d8621-6c1a-5870-a102-29edcc52d739/",
        "created_time": "2011-11-22 10:46:39",
        "description": "",
        "has_owner": false,
        "obj_type": "image",
        "owner": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
        "resource_uri": "/v1/image/e14d8621-6c1a-5870-a102-29edcc52d739/",
        "title": "a long title that may not fit entirely in the tiny-box. is this ",
        "total_comments": 2,
        "total_favorites": 0,
        "total_votes": 0,
        "updated_time": "2011-11-22 10:46:39",
        "versions": [
        ...
        ]
        }]
    }

Usage: If you want to get all the active images that are uploaded by all users, use the "order_by=-created_time" to get reverse-chronological order. This is actually the default. However, it is recommended that the front-end send this parameter just in case the backend API changes in the future and the front-end still wants the same functionality. 

Also, you want the most recent images uploaded by a user. Add the owner filter.

Create an Image
-------------------
You can upload an Image by attaching a file and issuing a HTTP **Multipart POST (RFC1867)** request to **/v1/image/** with a JSON object containing the following Key/Value:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "owner",             "URI for the user that created the image",     "string",	"yes"
    "title",             "Text representing the title",                 "string",	"yes"
    "description",       "Description of the image",                    "string",	"yes"

If the POST is successful, you will receive the following Response Header:

.. code-block:: js

    Status Code: 201
    Date: Sat, 10 Mar 2012 18:51:45 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8
    Location: http://www.dujour.im/v1/image/e14d8621-6c1a-5870-a102-29edcc52d739/

You will get "Status Code: 201". Furthermore, the URI of the newly created resource will be under the "Location" field.
If the image file type is not supported by the back-end, you will get "Status Code: 415 (Unsupported media type)" error. It will be better to check if the images are valid jpg, png, gif files in the front-end.



Update an Image
-------------------

You can update a comment by issuing a HTTP **PUT** request to **/v1/wordbox/WORDBOX_ID/** with a JSON object containing the following Keys/Values:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "title",            "Text representing the title",                  "string",       "no"
    "message",          "Text representing the content",                "string",       "no"

If the PUT is successful, you will receive the following Response Header:

.. code-block:: js

    Status Code: 204
    Date: Sat, 10 Mar 2012 19:24:35 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8

You will get "Status Code: 204" if the PUT request is successful.

The easiest way to update is to **PUT** the entire collection (with id WORDBOX_ID) JSON object to **/v1/wordbox/WORDBOX_ID/** and update the required fields (listed above). All the other fields will be ignored.



Get all Images belonging to a Collection
----------------------------------------

You can get all the Images related to a Collection by issuing a HTTP **GET** request to **/v1/image/** with the following parameters. (i.e. /v1/image/?collection=/v1/collection/f7d5e2f5-cf65-5b41-a294-764a2d2c98ef/)

.. csv-table::
    :widths: 10 60 10 20
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "collection",       "URI of the collection object",                     "string",           "yes" 
    "offset",           "The index of the first object after the query has been ordered",       "integer", "no"
    "limit",            "The number of comments to be returned after all comments are ordered. Default = "all comments", "string", "no"
    "order_by",         "Currently, this is not an option. The default is "-created_time" where the '-' signifies reverse chronological order.",   "string", "no"

The results are the same as the section above for getting Images that belonging to a User

Update an Image
---------------

You can update the parameters of a image by issuing a HTTP PUT request to IMAGE_ID resource with the parameters that you would like to update and its new values. If the update was completely successful, then nothing is returned.

If there were some fields that could not be written, then those fields would generate an error: 


.. csv-table::
   :header: "Name", "Description", "Type"
   :widths: 20, 80, 20

   "ERROR",	"A specific parameter was not updated successfully", "String"

.. code-block:: js

	{
	   "ERROR": {
		   "message": "The field 'message' could not be updated.",
		   "size": "The field 'size' could not be updated."
	   }
	}

Those fields that do no generate an error, have been written successfully

Delete an image
---------------

You can delete an image by issuing a HTTP **DELETE** request to the IMAGE_ID object.

If the delete is successful, then nothing is returned. Otherwise, an error is returned.




.. _media-collection:

Collection
===========

Description
------------

A collection is a set of images and wordboxes. 

Get information about a collection
----------------------------------

You can get the following information about a collection by issuing a HTTP **GET** request to **/v1/collection/COMMENT_ID**. The following is returned:

.. csv-table::
    :widths: 10 60 30
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "name",              "Name of the collection",                                   "string"
    "owner",             "URI for the user that created the comment",                "string"
    "description",       "Description of the collection",                            "string"
    "location",          "Location of the collection",                               "string"
    "created_time",      "The time the comment was created",                         "string, rfc-3339 standard"
    "obj_type",          "the type of resource",                                     "string"
    "resource_uri",      "URI of the current object",                                "string"
    "comment",           "URI for all the comments belonging to this collection",    "string"
    "vote",              "URI for all the vote belonging to this collection",        "string"
    "image",             "Array of URI's of images belonging to this collection",    "array of strings"
    "total_votes",       "The number of times this collection was voted on",         "integer"
    "total_comments",    "The number of comments for this collection",               "integer"
    "total_images",      "The number of images in this collection",                  "integer"
    "total_favorites",   "The number of times this comment was favorited",           "integer"
..	"user_voted", "True if the session user voted on the collection", "boolean"

.. code-block:: js

    {
        "comment": "/v1/comment/?parent=/v1/collection/3d319b9a-5889-5526-b02f-0e620c1c563b/",
        "created_time": "2012-03-17T08:26:40",
        "description": "a new collection",
        "image": ["/v1/image/cf1a4919-aa52-5bd2-ad25-87ac2a3a0b7f/", "/v1/image/84261c79-f949-5605-bae8-ad783bdcfd55/", "/v1/image/bd341d56-57f3-5503-9bcc-a4b08f79a9d5/"],
        "location": "Stanford",
        "name": "My first collection",
        "obj_type": "collection",
        "owner": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
        "resource_uri": "/v1/collection/3d319b9a-5889-5526-b02f-0e620c1c563b/",
        "total_comments": 3,
        "total_favorites": 9,
        "total_images": 3,
        "total_votes": 6
    }

Get all collections belonging to a user
---------------------------------------

You can get all the collections related to a user by issuing a HTTP **GET** request to **/v1/collection/** with the following parameters


.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "owner",            "URI of the user object",                          "string",           "yes" 
    "offset",           "The index of the first object after the query has been ordered",      "integer", "no"
    "limit",            "The number of comments to be returned after all comments are ordered. Default = "all comments", "string", "no"
    "order_by",         "Currently, this is not an option. The default is "-created_time" where the '-' signifies reverse chronological order.",   "string", "no"

Example code:

.. code-block:: js

    /v1/collection/?owner=/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/


The following JSON object is returned:

.. csv-table::
    :widths: 20 70 10
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "meta",              "Information regarding the query: 'limit' 'next' 'offset' 'previous', 'total_count'," "string"
    "object",            "Array of returned objects",                              "Array"

Example code:

.. code-block:: js

    {
        "meta": {
            "limit": 20,
            "next": null,
            "offset": 0,
            "previous": null,
            "total_count": 2
        },
        "objects": [{
            "comment": "/v1/comment/?parent=/v1/collection/d63bcf62-caea-5abf-a510-bf4b1e33b0f7/",
            "created_time": "2011-11-23T08:06:37",
            "description": "Test collection",
            "image": "/v1/image/?collection=/v1/collection/d63bcf62-caea-5abf-a510-bf4b1e33b0f7/",
            "location": "Stanford",
            "name": "Collection 1",
            "obj_type": "collection",
            "owner": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
            "resource_uri": "/v1/collection/d63bcf62-caea-5abf-a510-bf4b1e33b0f7/",
            "total_comments": 200,
            "total_favorites": 3330,
            "total_images": 50,
            "total_votes": 60
        }, {
            "comment": "/v1/comment/?parent=/v1/collection/3d319b9a-5889-5526-b02f-0e620c1c563b/",
            "created_time": "2012-03-17T08:26:40",
            "description": "a new collection",
            "image": "/v1/image/?collection=/v1/collection/3d319b9a-5889-5526-b02f-0e620c1c563b/",
            "location": "California",
            "name": "Tastypie Collection 3",
            "obj_type": "collection",
            "owner": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
            "resource_uri": "/v1/collection/3d319b9a-5889-5526-b02f-0e620c1c563b/",
            "total_comments": 3,
            "total_favorites": 0,
            "total_images": 3,
            "total_votes": 0
        }]
    }

Create a collection
-------------------

You can create a collection by issuing a HTTP **POST** request to the **/v1/collection/** uri with a JSON object containing the following Key/Value:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "name",             "Name of the collection",                       "string",       "yes"
    "owner",            "URI for the user that created the comment",    "string",       "yes"
    "description",      "Description of the collection",                "string",       "no"
    "location",         "Location of the collection",                   "string",       "no"
    "image",            "Array of URI's of images belonging to this collection",    "array of strings", "yes"


If the POST is successful, you will receive the following Response Header:

.. code-block:: js

    Status Code: 201
    Date: Sat, 10 Mar 2012 18:51:45 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8
    Location: http://www.dujour.im/v1/collection/3d319b9a-5889-5526-b02f-0e620c1c563b/

You will get "Status Code: 201". Furthermore, the URI of the newly created resource will be under the "Location" field.

Update a Collection
-------------------

You can update a comment by issuing a HTTP **PUT** request to the **/v1/collection/COLLECTION_ID/** uri with a JSON object containing the following Keys/Values:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "name",             "Name of the collection",                       "string",       "no"
    "owner",            "URI for the user that created the comment",    "string",       "no"
    "description",      "Description of the collection",                "string",       "no"
    "location",         "Location of the collection",                   "string",       "no"
    "image",            "Array of URI's of images belonging to this collection",    "array of strings", "yes"

If the PUT is successful, you will receive the following Response Header:

.. code-block:: js

    Status Code: 204
    Date: Sat, 10 Mar 2012 19:24:35 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8

You will get "Status Code: 204" if the PUT request is successful.

The easiest way to update is to **PUT** the entire collection (with id COLLECTION_ID) JSON object to **/v1/collection/COLLECTION_ID/** and update the required fields (listed above). All the other fields will be ignored.

Add Images to a Collection
--------------------------

You can add Images to a Collection by issuing a HTTP **POST** request to the **/v1/collection/COLLECTION_ID/add/** uri with a JSON object containing the following Keys/Values:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "image",            "Array of Image URI's",                         "array",        "yes"

For example:

.. code-block:: js

    {
        "image": [
            "/v1/image/b62fb9b4-9c13-50c3-8c85-2c87e96553b3/",
            "/v1/image/517f3334-9f6a-51dd-853a-c6f565ded546/"
        ]
    }

If the Images are successfully added to the Collection, you will receive the following Response Header:

.. code-block:: js

    Status Code: 201
    Date: Sun, 06 May 2012 06:43:02 GMT
    Transfer-Encoding: chunked
    Connection: keep-alive
    Server: nginx/1.0.5
    Content-Type: text/html; charset=utf-8
    Location: http://www.dujour.im/v1/community/dec0c7df-1656-560f-80d8-380ee7ffe6bc/add/

You will get "Status Code: 201" if the POST request is successful.

Remove Images from a Community
--------------------------------

You can remove Images from a Community by issuing a HTTP **POST** request to the **/v1/community/COMMUNITY_ID/remove/** uri with a JSON object containing the following Keys/Values:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "image",            "Array of Image URI's",                         "array",        "yes"

For example:

.. code-block:: js

    {
        "image": [
            "/v1/image/b62fb9b4-9c13-50c3-8c85-2c87e96553b3/",
            "/v1/image/517f3334-9f6a-51dd-853a-c6f565ded546/"
        ]
    }

If the Images are successfully removed to the Community, you will receive the following Response Header:

.. code-block:: js

    Status Code: 201
    Date: Sun, 06 May 2012 06:43:02 GMT
    Transfer-Encoding: chunked
    Connection: keep-alive
    Server: nginx/1.0.5
    Content-Type: text/html; charset=utf-8
    Location: http://www.dujour.im/v1/community/dec0c7df-1656-560f-80d8-380ee7ffe6bc/add/

You will get "Status Code: 201" if the POST request is successful.

Add WordBoxes to a Community
----------------------------

Same as above for Images. Just use 'wordbox' instead of 'image'.

Remove WordBoxes from a Community
---------------------------------

Same as above for Images. Just use 'wordbox' instead of 'image'.



Delete a collection
-------------------

You can delete a collection by issuing a HTTP **DELETE** request to **/v1/collection/COLLECTION_ID**.

If the DELETE is successful, you will receive the following Response Header:

.. code-block:: js

    Status Code: 204
    Date: Sat, 10 Mar 2012 19:24:35 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8

You will get "Status Code: 204".



.. _media-WordBox:

WordBox
=======

Description
-----------

A wordbox is a text media item.

Get information about a wordbox 
-------------------------------

You can get the following information about a wordbox by issuing a HTTP **GET** request to **/v1/wordbox/WORDBOX_ID**. The following is returned:

.. csv-table::
    :widths: 10 60 30
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "owner",             "URI for the user that created the comment",                "string"
    "title",             "Text representing the title",                              "string"
    "message",           "Text representing the content",                            "string"
    "created_time",      "The time the comment was created",                         "string, rfc-3339 standard"
    "updated_time",      "The time the comment was updated",                         "string, rfc-3339 standard"
    "obj_type",          "the type of resource",                                     "string"
    "resource_uri",      "URI of the current object",                                "string"
    "comment",           "URI for all the comments belonging to this wordbox",       "string"
    "vote",              "URI for all the vote belonging to this wordbox",           "string"
    "total_votes",       "The number of times this collection was voted on",         "integer"
    "total_comments",    "The number of comments for this wordbox",                  "integer"
    "total_collected",   "The number of users that have collected the wordbox",      "integer"
..	"user_voted", "True if the session user voted on the collection", "boolean"

.. code-block:: js

    {
        "comment": "/v1/comment/?parent=/v1/wordbox/0f97c2b6-1bb7-52ff-8d15-1a5e10bebc91/",
        "created_time": "2012-01-16T04:47:00",
        "message": "Dujour is great, and it has great team. We are going to change the world!",
        "obj_type": "wordbox",
        "owner": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
        "resource_uri": "/v1/wordbox/0f97c2b6-1bb7-52ff-8d15-1a5e10bebc91/",
        "title": "Dujour Team",
        "total_comments": 8,
        "total_favorites": 45,
        "total_votes": 20,
        "updated_time": "2012-03-11T14:34:59"
    }

Get all Wordboxes belonging to a User
---------------------------------------

You can get all the wordboxes related to a User by issuing a HTTP **GET** request to **/v1/wordbox/** with the following parameters

.. csv-table::
    :widths: 10 60 10 20
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "owner",            "URI of the user object",                          "string",           "yes" 
    "offset",           "The index of the first object after the query has been ordered",      "integer", "no"
    "limit",            "The number of comments to be returned after all comments are ordered. Default = "all comments", "string", "no"
    "order_by",         "Currently, this is not an option. The default is "-created_time" where the '-' signifies reverse chronological order.",   "string", "no"

Example code:

.. code-block:: js

    /v1/wordbox/?owner=/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/


The following JSON object is returned:

.. csv-table::
    :widths: 20 70 10
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "meta",              "Information regarding the query: 'limit' 'next' 'offset' 'previous', 'total_count'," "string"
    "object",            "Array of returned objects",                                "Array"

Example code:

.. code-block:: js

    {
        "meta": {
            "limit": 20,
            "next": null,
            "offset": 0,
            "previous": null,
            "total_count": 2
        },
        "objects": [
            {
                "comment": "/v1/comment/?parent=/v1/wordbox/0f97c2b6-1bb7-52ff-8d15-1a5e10bebc91/",
                "created_time": "2012-01-16T04:47:00",
                "message": "Dujour is great, and it has great team. We are going to change the world!",
                "obj_type": "wordbox",
                "owner": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
                "resource_uri": "/v1/wordbox/0f97c2b6-1bb7-52ff-8d15-1a5e10bebc91/",
                "title": "Dujour Team",
                "total_comments": 8,
                "total_favorites": 45,
                "total_votes": 20,
                "updated_time": "2012-03-11T14:34:59"
            },
            {
                "comment": "/v1/comment/?parent=/v1/wordbox/edb219e2-2c44-5099-b5c0-dc5150124870/",
                "created_time": "2012-01-16T04:55:52",
                "message": "my wordbox message",
                "obj_type": "wordbox",
                "owner": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
                "resource_uri": "/v1/wordbox/edb219e2-2c44-5099-b5c0-dc5150124870/",
                "title": "my wordbox message",
                "total_comments": 1,
                "total_favorites": 0,
                "total_votes": 0,
                "updated_time": "2012-01-16T04:55:52"
            }
        ]
    }

Get all Wordboxes belonging to a Community
------------------------------------------

You can get all the Wordboxes related to a Community by issuing a HTTP **GET** request to **/v1/wordbox/** with the following parameters


.. csv-table::
    :widths: 10 60 10 20
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "community",        "URI of the community object",                          "string",           "yes" 
    "offset",           "The index of the first object after the query has been ordered",      "integer", "no"
    "limit",            "The number of comments to be returned after all comments are ordered. Default = "all comments", "string", "no"
    "order_by",         "Currently, this is not an option. The default is "-created_time" where the '-' signifies reverse chronological order.",   "string", "no"

The results are the same as the section above for getting wordboxes that belonging to a User

Get all Wordboxes belonging to a Collection 
-------------------------------------------

You can get all the Wordboxes related to a Collection by issuing a HTTP **GET** request to **/v1/wordbox/** with the following parameters. (i.e. /v1/wordbox/?collection=/v1/collection/f7d5e2f5-cf65-5b41-a294-764a2d2c98ef/)

.. csv-table::
    :widths: 10 60 10 20
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "collection",       "URI of the collection object",                     "string",           "yes" 
    "offset",           "The index of the first object after the query has been ordered",       "integer", "no"
    "limit",            "The number of comments to be returned after all comments are ordered. Default = "all comments", "string", "no"
    "order_by",         "Currently, this is not an option. The default is "-created_time" where the '-' signifies reverse chronological order.",   "string", "no"

The results are the same as the section above for getting Images that belonging to a User

Create a wordbox
----------------

You can create a wordbox by issuing a HTTP **POST** request to the **/v1/wordbox/** uri with a JSON object containing the following Key/Value:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "title",            "Text representing the title",                  "string",       "yes"
    "message",          "Text representing the content",                "string",       "no"

If the POST is successful, you will receive the following Response Header:

.. code-block:: js

    Status Code: 201
    Date: Sat, 10 Mar 2012 18:51:45 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8
    Location: http://www.dujour.im/v1/collection/3d319b9a-5889-5526-b02f-0e620c1c563b/

You will get "Status Code: 201". A JSON object representing the created object will be returned.

Update a wordbox
-------------------

You can update a comment by issuing a HTTP **PUT** request to the **/v1/wordbox/WORDBOX_ID/** uri with a JSON object containing the following Keys/Values:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "title",            "Text representing the title",                  "string",       "no"
    "message",          "Text representing the content",                "string",       "no"

If the PUT is successful, you will receive the following Response Header:

.. code-block:: js

    Status Code: 204
    Date: Sat, 10 Mar 2012 19:24:35 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8

You will get "Status Code: 204" if the PUT request is successful. A JSON object representing the updated object will be returned.

The easiest way to update is to **PUT** the entire collection (with id WORDBOX_ID) JSON object to **/v1/wordbox/WORDBOX_ID/** and update the required fields (listed above). All the other fields will be ignored.

Delete a wordbox
-------------------

You can delete a collection by issuing a HTTP **DELETE** request to **/v1/wordbox/WORDBOX_ID**.

If the DELETE is successful, you will receive the following Response Header:

.. code-block:: js

    Status Code: 204
    Date: Sat, 10 Mar 2012 19:24:35 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8

You will get "Status Code: 204".
