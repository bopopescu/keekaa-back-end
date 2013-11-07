*********
Users
*********

.. _users-friendship:

Community
=========

Description
------------

A community is a set of users.

Get information about a Community
---------------------------------

You can get the following information about Community by issuing a HTTP **GET** request to **/v1/community/COMMUNITY_ID**. The following is returned:

.. csv-table::
    :widths: 10 60 30
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "creator",           "URI for the user that created the community",              "string"
    "member",            "URI for the all the members in a community",               "string"
    "communitycategory", "URI for the all the communitycategories a community belongs to","string"
    "total_members",     "Total number of members in the community",                 "string"
    "name",              "Name of the community",                                    "string"
    "description",       "Description of the community",                             "string"
    "created_time",      "The time the comment was created",                         "string, rfc-3339 standard"
    "updated_time",      "The time the comment was updated",                         "string, rfc-3339 standard"
    "obj_type",          "the type of resource",                                     "string"
    "total_images",      "The total number of images in the community",              "integer"
    "total_wordboxes",   "The total number of wordboxes in the community",           "integer"
    "total_images",      "The total number of members in the community",             "integer"
    "total_communitycategories", "The total number of communitycateogries the community belongs to", "integer"
    "profile_image_standard", "Profile images of standard size",                     "array"
    "profile_image_thumbnail", "Profile images of thumbnail size",                   "array"
    "tag",               "All the tags (string) associated with a community",        "array"
    "resource_uri",      "URI of the current object",                                "string"
    "vote",              "URI of the votes for the current object",                  "string"
    "wordbox",           "URI of the wordboxes for this object",                     "string"

Example code:

.. code-block:: js

    {
        "created_time": "2011-12-04 00:06:39",
        "creator": "/v1/user/e88864da-41bc-54c7-8ce1-37212fab3245/",
        "description": "The stylin' community",
        "member": "/v1/user/?community=/v1/community/80c6d918-32ef-5b0a-9450-fcf55e192bc3/",
        "name": "Michael's Style community",
        "member": "/v1/user/?community=/v1/community/dec0c7df-1656-560f-80d8-380ee7ffe6bc/",
        "communitycategory": "/v1/communitycategory/?community=/v1/community/53042c59-c814-5aed-9c9d-8b05c1f335da/",
        "obj_type": "community",
        "tag": [
            "vintage",
            "curvy"
        ],
        "resource_uri": "/v1/community/80c6d918-32ef-5b0a-9450-fcf55e192bc3/",
        "total_images": 2,
        "total_members": 0,
        "total_wordboxes": 1,
        "total_communitycategories": 1,
        "profile_image_standard": [
        {
            "height": 960,
            "resource_uri": "https://d956iao6yp65z.cloudfront.net/images/1322037489_72ac8ff1-d1af-530a-a534-efc25b674766_0640x0960.jpg",
            "width": 640
        },
        ...
        ],
        "profile_image_thumbnail": [
        {
            "height": 960,
            "resource_uri": "https://d956iao6yp65z.cloudfront.net/images/1322037489_72ac8ff1-d1af-530a-a534-efc25b674766_0640x0960.jpg",
            "width": 640
        },
        ...
        ],
        "updated_time": "2012-03-20T06:46:02"
    }

Get all CommunityCategories a Community belongs to
--------------------------------------------------

You can get all the CommunityCategories a Community belongs to by issuing a HTTP **GET** request to **/v1/communitycategory/** with the following parameters.

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "community",        "URI of the Community object",                      "string",           "yes" 
    "offset",           "The index of the first object after the query has been ordered",      "integer", "no"
    "limit",            "The number of comments to be returned after all comments are ordered. Default = ""all comments""", "string", "no"
    "order_by",         "Currently, this is not an option. The default is "-created_time" where the '-' signifies reverse chronological order.",   "string", "no"

Example code:

.. code-block:: js

    /v1/communitycategory/?community=/v1/community/53042c59-c814-5aed-9c9d-8b05c1f335da/

The following JSON object is returned:

.. csv-table::
    :widths: 20 70 10
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "meta",              "Information regarding the query. ""limit"", ""next"", ""offset"", ""previous"", ""total_count""", "string"
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
            "name": "Style",
            "obj_type": "communitycategory",
            ...
        },
        {
            "name": "Occasion",
            "obj_type": "communitycategory",
            ...
        }]

Get all Communities belonging to a User
---------------------------------------

You can get all the Images belonging to a User by issuing a HTTP **GET** request to **/v1/community/** with the following parameters


.. csv-table::
    :widths: 10 60 10 20
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "member",             "URI of the User object",                           "string",           "yes" 
    "offset",           "The index of the first object after the query has been ordered",      "integer", "no"
    "limit",            "The number of comments to be returned after all comments are ordered. Default = "all comments", "string", "no"
    "order_by",         "The default is "-created_time" where the '-' signifies reverse chronological order.",   "string", "no"

Example code:

.. code-block:: js

    /v1/community/?member=/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/

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
            "next": "/v1/community/?limit=20&user=%2Fv1%2Fuser%2F4d2c6f83-9a8c-56c2-9ae2-e1f66c7ccb64%2F&offset=20",
            "offset": 0,
            "previous": null,
            "total_count": 21
        },
        "objects": [
            {
                "comment": "/v1/comment/?parent=%2Fv1%2Fcommunity%2Fe14c1b58-001e-5c2b-9c68-7a23b3118f8a%2F",
                "communitycategory": "/v1/communitycategory/?community=%2Fv1%2Fcommunity%2Fe14c1b58-001e-5c2b-9c68-7a23b3118f8a%2F",
                "created_time": "2012-07-16T04:53:19+00:00",
                "creator": "/v1/user/4d2c6f83-9a8c-56c2-9ae2-e1f66c7ccb64/",
                "description": "Exploded Floral Prints in Every Possible Way!",
                "image": "/v1/image/?community=%2Fv1%2Fcommunity%2Fe14c1b58-001e-5c2b-9c68-7a23b3118f8a%2F",
                "member": "/v1/user/?community=%2Fv1%2Fcommunity%2Fe14c1b58-001e-5c2b-9c68-7a23b3118f8a%2F",
                "name": "In Bloom",
                "profile_image_standard": null,
                "profile_image_thumbnail": null,
                "resource_uri": "/v1/community/e14c1b58-001e-5c2b-9c68-7a23b3118f8a/",
                "tag": [],
                "total_communitycategories": 1,
                "total_images": 9,
                "total_members": 2,
                "total_wordboxes": 0,
                "updated_time": "2012-07-26T05:38:41+00:00",
                "vote": "/v1/vote/?parent=%2Fv1%2Fcommunity%2Fe14c1b58-001e-5c2b-9c68-7a23b3118f8a%2F",
                "wordbox": "/v1/wordbox/?community=%2Fv1%2Fcommunity%2Fe14c1b58-001e-5c2b-9c68-7a23b3118f8a%2F"
            },
            {
                "comment": "/v1/comment/?parent=%2Fv1%2Fcommunity%2F51adf8d8-d806-536a-b972-9da20d6d14e6%2F",
                "communitycategory": "/v1/communitycategory/?community=%2Fv1%2Fcommunity%2F51adf8d8-d806-536a-b972-9da20d6d14e6%2F",
                "created_time": "2012-07-16T04:56:55+00:00",
                "creator": "/v1/user/4d2c6f83-9a8c-56c2-9ae2-e1f66c7ccb64/",
                "description": "What I wear with a classic blazer!",
                "image": "/v1/image/?community=%2Fv1%2Fcommunity%2F51adf8d8-d806-536a-b972-9da20d6d14e6%2F",
                "member": "/v1/user/?community=%2Fv1%2Fcommunity%2F51adf8d8-d806-536a-b972-9da20d6d14e6%2F",
                "name": "...A Classic Blazer",
                "profile_image_standard": null,
                "profile_image_thumbnail": null,
                "resource_uri": "/v1/community/51adf8d8-d806-536a-b972-9da20d6d14e6/",
                "tag": [],
                "total_communitycategories": 2,
                "total_images": 9,
                "total_members": 1,
                "total_wordboxes": 0,
                "updated_time": "2012-07-16T04:56:55+00:00",
                "vote": "/v1/vote/?parent=%2Fv1%2Fcommunity%2F51adf8d8-d806-536a-b972-9da20d6d14e6%2F",
                "wordbox": "/v1/wordbox/?community=%2Fv1%2Fcommunity%2F51adf8d8-d806-536a-b972-9da20d6d14e6%2F"
            }
        ]
    }

Get all Images/Wordboxes (Media) for a community
------------------------------------------------

You can get all the images/wordboxes (media) of a community by issuing a HTTP **GET** request to **/v1/media/** with the following parameters

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "community",        "URI of the the community",                         "string",           "yes" 
    "offset",           "The index of the first object after the query has been ordered",      "integer", "no"
    "limit",            "The number of comments to be returned after all comments are ordered. Default = ""all comments""", "string", "no"

Example code:

.. code-block:: js

    http://www.dujour.im/v1/media/?community=/v1/community/2091d4db-972b-5104-8718-8a2575c1504c/

The following JSON object is returned:

.. csv-table::
    :widths: 20 70 10
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "meta",              "Information regarding the query. ""limit"", ""next"", ""offset"", ""previous"", ""total_count""", "string"
    "object",            "Array of returned Image and Wordbox objects",              "Array"

Example code:

.. code-block:: js

    {
        "meta": {
            "limit": 20,
            "next": null,
            "offset": 0,
            "previous": null,
            "total_count": 4
        },
        "objects": [{
            "obj_type": "image"
            ...
        }, {
            "obj_type": "wordbox",
            ...
        }, {
            "obj_type": "wordbox",
            ...
        }, {
            "obj_type": "image"
            ...
        }]
    }

Get all the Tags of a Community
-------------------------------

All the tags associated with a community can be found directly in the community resource: **/v1/community/COMMUNITY_ID**.The tags will be in an array found under the key "tag".

Create a Community
------------------

You can create an community by issuing a HTTP **POST** request to **/v1/community/** with a JSON object containing the following Key/Value:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "creator",          "URI for the user that created the community",      "string",       "yes"
    "name",             "Name of the community",                            "string",       "yes"
    "description",      "Description of the community",                     "string",       "no"

If the POST is successful, you will receive the following Response Header:

.. code-block:: js

    Status Code: 201
    Date: Sat, 10 Mar 2012 18:51:45 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8
    Location: http://www.dujour.im/v1/community/80c6d918-32ef-5b0a-9450-fcf55e192bc3/

You will get "Status Code: 201". A JSON object representing the updated object will be returned.

Update an Community
-------------------

You can update a community by issuing a HTTP **PUT** request to **/v1/community/COMMUNITY_ID** with a JSON object containing the following Keys/Values:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "name",             "Name of the community",                            "string",       "no"
    "description",      "Description of the community",                     "string",       "no"

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

The easiest way to update is to **PUT** the entire community (with id COMMUNITY_ID) JSON object to **/v1/community/COMMUNITY_ID/** and update the required fields (listed above). All the other fields will be ignored.

Add Images to a Community
-------------------------

You can add Images to a Community by issuing a HTTP **POST** request to **/v1/community/COMMUNITY_ID/add/** with a JSON object containing the following Keys/Values:

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

If the Images are successfully added to the Community, you will receive the following Response Header:

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

You can remove Images from a Community by issuing a HTTP **POST** request to **/v1/community/COMMUNITY_ID/remove/** with a JSON object containing the following Keys/Values:

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
--------------------------------

Same as above for Images. Just use 'wordbox' instead of 'image'.

Remove WordBoxes from a Community
----------------------------------

Same as above for Images. Just use 'wordbox' instead of 'image'.

Add Tags to a Community
-------------------------

You can add Tags to a Community by issuing a HTTP **POST** request to **/v1/community/COMMUNITY_ID/add_tag/** with a JSON object containing the following Keys/Values:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "tag",              "Array of tags (string)",                       "array",        "yes"

For example:

.. code-block:: js

    {
        "tag": [
            "vintage",
            "curvy"
        ]
    }

If the tags are successfully added to the Community, you will receive the following Response Header:

Set Tags for a Community
------------------------

Setting tags means that all the current tags are removed and the new tags are added.

You can set tags for a Community by issuing a HTTP **POST** request to **/v1/community/COMMUNITY_ID/set_tag/** with a JSON object containing the following Keys/Values:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "tag",              "Array of tags (string)",                       "array",        "yes"

For example:

.. code-block:: js

    {
        "tag": [
            "vintage",
            "curvy"
        ]
    }

If the tags are successfully set for the Community, you will receive the following Response Header:

.. code-block:: js

    Status Code: 201
    Date: Sun, 17 Jun 2012 01:47:37 GMT
    Transfer-Encoding: chunked
    Connection: keep-alive
    Server: nginx/1.0.5
    Content-Type: text/html; charset=utf-8
    Location: http://www.derek.dev.dujour.im/v1/community/4356b871-d2aa-5468-91da-7fd2dfa42923/settag/

You will get "Status Code: 201" if the POST request is successful.

Remove Tags from a Community
----------------------------

You can remove tags from a Community by issuing a HTTP **POST** request to **/v1/community/COMMUNITY_ID/remove_tag/** with a JSON object containing the following Keys/Values:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "tag",              "Array of tags (string)",                       "array",        "yes"

For example:

.. code-block:: js

    {
        "tag": [
            "vintage",
            "curvy"
        ]
    }

If the tags are successfully removed to the Community, you will receive the following Response Header:

.. code-block:: js

    Status Code: 201
    Date: Sat, 16 Jun 2012 22:55:24 GMT
    Transfer-Encoding: chunked
    Connection: keep-alive
    Server: nginx/1.0.5
    Content-Type: text/html; charset=utf-8
    Location: http://www.derek.dev.dujour.im/v1/community/4356b871-d2aa-5468-91da-7fd2dfa42923/removetag/

You will get "Status Code: 201" if the POST request is successful.

Delete an Community
-------------------

You can delete a community by issuing a HTTP **DELETE** request to **/v1/community/community_ID**.

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


CommunityCategory
=================

Description
-----------

A community cateogry is a collection of communities.

Get information about a CommunityCategory
-----------------------------------------

You can get the following information about Community Category by issuing a HTTP **GET** request to **/v1/communitycategory/COMMUNITYCATEGORY_ID**. The following is returned:

.. csv-table::
    :widths: 10 60 30
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "name",              "Name of the community",                                    "string"
    "description",       "Description of the community",                             "string"
    "created_time",      "The time the comment was created",                         "string, rfc-3339 standard"
    "updated_time",      "The time the comment was updated",                         "string, rfc-3339 standard"
    "obj_type",          "the type of resource",                                     "string"
    "total_communities", "The total number of communities in the community category", "integer"
    "community",         "URI for all the communities in this community category",   "string"
    "resource_uri",      "URI of the current object"                                 "string"

Example code:

.. code-block:: js

    {
        "community": "/v1/community/?communitycategory=/v1/communitycategory/617d3277-f4b8-5e2b-a771-e6a1a6396140/",
        "created_time": "2012-06-17T19:37:59+00:00",
        "description": "Check out the lastest styles!",
        "name": "Style",
        "obj_type": "communitycategory",
        "resource_uri": "/v1/communitycategory/617d3277-f4b8-5e2b-a771-e6a1a6396140/",
        "total_communities": 1,
        "updated_time": "2012-06-17T19:37:59+00:00"
    }

Get all Communities belonging to a CommunityCategory
----------------------------------------------------

You can get all the Communities belonging to a CommunityCategory by issuing a HTTP **GET** request to **/v1/community/** with the following parameters.

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "communitycategory","URI of the CommunityCategory object",              "string",           "yes" 
    "offset",           "The index of the first object after the query has been ordered",      "integer", "no"
    "limit",            "The number of comments to be returned after all comments are ordered. Default = ""all comments""", "string", "no"
    "order_by",         "Currently, this is not an option. The default is "-created_time" where the '-' signifies reverse chronological order.",   "string", "no"

Example code:

.. code-block:: js

    /v1/community/?communitycategory=/v1/communitycategory/617d3277-f4b8-5e2b-a771-e6a1a6396140/

The following JSON object is returned:

.. csv-table::
    :widths: 20 70 10
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "meta",              "Information regarding the query. ""limit"", ""next"", ""offset"", ""previous"", ""total_count""", "string"
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
            "name": "Vintage",
            "obj_type": "community",
            ...
        },
        {
            "name": "Pajamas",
            "obj_type": "community",
            ...
        }]
    }

Add Communities to a CommunityCategory
--------------------------------------

You can add Communities to a CommunityCategory by issuing a HTTP **POST** request to **/v1/communitycategory/COMMUNITYCATEGORY_ID/add_community/** with a JSON object containing the following Keys/Values:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "community",        "Array of Community URI's",                     "array",        "yes"

For example:

.. code-block:: js

    {
        "community": [
            "/v1/community/53042c59-c814-5aed-9c9d-8b05c1f335da/",
            "/v1/community/00058d0f-5472-579e-8a5c-5821cc68b1fc/"
        ]
    }

If the Communities are successfully added to the CommunityCategory, you will receive the following Response Header:

.. code-block:: js

    Status Code: 201
    Date: Sun, 17 Jun 2012 21:28:17 GMT
    Transfer-Encoding: chunked
    Connection: keep-alive
    Server: nginx/1.0.5
    Content-Type: text/html; charset=utf-8
    Location: http://www.derek.dev.dujour.im/v1/communitycategory/617d3277-f4b8-5e2b-a771-e6a1a6396140/add_community/

You will get "Status Code: 201" if the POST request is successful.

Remove Communities from a CommunityCategory
-------------------------------------------

You can remove Communities from a CommunityCategory by issuing a HTTP **POST** request to **/v1/communitycategory/COMMUNITYCATEGORY_ID/remove_community/** with a JSON object containing the following Keys/Values:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "community",        "Array of Community URI's",                     "array",        "yes"

For example:

.. code-block:: js

    {
        "community": [
            "/v1/community/53042c59-c814-5aed-9c9d-8b05c1f335da/",
            "/v1/community/00058d0f-5472-579e-8a5c-5821cc68b1fc/"
        ]
    }

If the Communities are successfully removed from the CommunityCategory, you will receive the following Response Header:

.. code-block:: js

    Status Code: 201
    Date: Sun, 17 Jun 2012 21:28:17 GMT
    Transfer-Encoding: chunked
    Connection: keep-alive
    Server: nginx/1.0.5
    Content-Type: text/html; charset=utf-8
    Location: http://www.derek.dev.dujour.im/v1/communitycategory/617d3277-f4b8-5e2b-a771-e6a1a6396140/add_community/

You will get "Status Code: 201" if the POST request is successful.

Friendship
==========

Description
-----------

Get information about a friendship
-----------------------------------

You can get the following information about a friendship by issuing a HTTP **GET** request to **/v1/friend/FRIENDSHIP_ID** with the following parameters:

.. csv-table::
    :widths: 10 60 10 20
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "user",             "URI of the a user object",                         "string",           "yes" 


The following is returned:

.. csv-table::
    :widths: 10 50 40
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "friend",            "URI for the friend of the original user",                  "string"
    "resource_uri"       "URI of the Friendship object"                              "string

Example code:

.. code-block:: js

    {
        "friend": "/v1/user/e88864da-41bc-54c7-8ce1-37212fab3245/",
        "resource_uri": "/v1/friend/1875f739-51f2-533c-a744-9d98f8df4f3d/"
    }

Get friends related to a user
------------------------------

You can get all the friends related to a media object by issuing a HTTP **GET** request to **/v1/friend/** with the following parameters:

.. csv-table::
    :widths: 10 60 10 20
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "parent",           "URI of the parent object",                         "string",           "no" 
    "offset",           "The index of the first object after the query has been ordered",      "integer", "no"
    "limit",            "The number of votes to be returned after all votes are ordered. Default = ""all comments""", "string", "no"

The following JSON object is returned:

.. csv-table::
    :widths: 10 80 10
    :header-rows: 1

    "Field",            "Description",                                       "Type"
    "meta",             "Information regarding the query. ""limit"", ""next"", ""offset"", ""previous"", ""total_count""", "string"
    "objects",          "Array of objects",                                  "integer" 

Example code:

.. code-block:: js

    {
        "meta": {
            "limit": 20,
            "next": null,
            "offset": 0,
            "previous": null,
            "total_count": 3
        },
        "objects": [{
            "friend": "/v1/user/e88864da-41bc-54c7-8ce1-37212fab3245/",
            "resource_uri": "/v1/friend/1875f739-51f2-533c-a744-9d98f8df4f3d/"
        }, {
            "friend": "/v1/user/3fc01072-8555-5509-9edc-061844f4a46a/",
            "resource_uri": "/v1/friend/99f4286e-b9d0-5e0d-b858-63f783bdf52c/"
        }]
    }

Create a friendship
---------------------

You can create a friendship by issuing a HTTP **POST** request to **/v1/friend/** uri with a JSON object containing the following Key/Value:

.. csv-table::
    :widths: 10 80 10
    :header-rows: 1

    "Key",              "Value",                                       "Type"
    "user1",            "URI of a user",                               "string"
    "user2",            "URI of another user",                         "string"

If the POST is successful, you will receive the following Response Header:

.. code-block:: js

    Status Code: 201
    Date: Sat, 10 Mar 2012 18:51:45 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8
    Location: http://www.derek.dev.dujour.im/v1/friend/d7c6527b-b17e-5eb1-8d89-468eee489fb0/

You will get "Status Code: 201". Furthermore, the URI of the newly created resource will be under the "Location" field.

Delete a friendship
--------------------

You can remove a friendship by issuing a HTTP **DELETE** request to the **/v1/friend/FRIENDSHIP_ID** uri.
If the DELETE is successful, you will receive the following Response Header

.. code-block:: js

    Status Code: 204
    Date: Sat, 10 Mar 2012 19:24:35 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8

You will get "Status Code: 204".

UserSubscription
================

Description
------------

A user can subscribe to another user through UserSubscriptions

Get information about an UserSubscription
------------------------------------------

You can get the following information about a UserSubscription by issuing a HTTP **GET** request to **/v1/usersubscription/USERSUBSCRIPTION_ID**. The following is returned:

.. csv-table::
    :widths: 10 60 30
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "to_user",           "URI of the user being subscribed to",                      "string"
    "from_user",         "URI of the subscriber",                                    "string"
    "updated_time",      "The time the comment was updated",                         "string, rfc-3339 standard"
    "obj_type",          "the type of resource",                                     "string"
    "resource_uri",      "URI of the current object"                                 "string"

Example code:

.. code-block:: js

    {
        "from_user": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
        "obj_type": "usersubscription",
        "resource_uri": "/v1/usersubscription/22d4e163-7b82-52cf-9295-24b1b3b5a60d/",
        "to_user": "/v1/user/e88864da-41bc-54c7-8ce1-37212fab3245/",
        "updated_time": "2012-02-23T05:01:12"
    }

Get all subscriptions belonging to a user
-----------------------------------------

You can get all the subscriptions belonging to a user by issuing a HTTP **GET** request to **/v1/usersubscription/** with the following parameters


.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "user",             "URI of the user",                                  "string",           "yes" 
    "offset",           "The index of the first object after the query has been ordered",      "integer", "no"
    "limit",            "The number of comments to be returned after all comments are ordered. Default = ""all comments""", "string", "no"
    "order_by",         "Currently, this is not an option. The default is "-created_time" where the '-' signifies reverse chronological order.",   "string", "no"

The following JSON object is returned:

.. csv-table::
    :widths: 20 70 10
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "meta",              "Information regarding the query. ""limit"", ""next"", ""offset"", ""previous"", ""total_count""", "string"
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
            "from_user": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
            "obj_type": "usersubscription",
            "resource_uri": "/v1/usersubscription/0743458b-4974-5aa8-bf42-1192fb08c7fa/",
            "to_user": "/v1/user/858fb3a9-2ff5-5eb9-8fdd-cd39a81164aa/",
            "updated_time": "2012-02-23T02:47:15"
        }, {
            "from_user": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
            "obj_type": "usersubscription",
            "resource_uri": "/v1/usersubscription/22d4e163-7b82-52cf-9295-24b1b3b5a60d/",
            "to_user": "/v1/user/e88864da-41bc-54c7-8ce1-37212fab3245/",
            "updated_time": "2012-02-23T05:01:12"
        }]
    }

Notice here that the "from_user" fields are the same. The "to_user" field represents the users whom the submitted "user" is subscribing to.

Get all subscribers of a user
-----------------------------------------

You can get all the subscribers of a user by issuing a HTTP **GET** request to **/v1/usersubscriber/** with the following parameters


.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "user",             "URI of the user",                                  "string",           "yes" 
    "offset",           "The index of the first object after the query has been ordered",      "integer", "no"
    "limit",            "The number of comments to be returned after all comments are ordered. Default = ""all comments""", "string", "no"
    "order_by",         "Currently, this is not an option. The default is "-created_time" where the '-' signifies reverse chronological order.",   "string", "no"

The following JSON object is returned:

.. csv-table::
    :widths: 20 70 10
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "meta",              "Information regarding the query. ""limit"", ""next"", ""offset"", ""previous"", ""total_count""", "string"
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
            "from_user": "/v1/user/3fc01072-8555-5509-9edc-061844f4a46a/",
            "obj_type": "usersubscription",
            "resource_uri": "/v1/usersubscriber/87028f77-90fa-5090-8208-0d817921b2af/",
            "to_user": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
            "updated_time": "2011-12-11T00:37:03"
        }, {
            "from_user": "/v1/user/e88864da-41bc-54c7-8ce1-37212fab3245/",
            "obj_type": "usersubscription",
            "resource_uri": "/v1/usersubscriber/261697bb-fe15-5ff1-8082-51c21ade8062/",
            "to_user": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
            "updated_time": "2012-02-26T03:16:39"
        }]
    }

Notice here that the "to_user" fields are the same. The "from_user" field represents the users subscribing to the submitted "user".

Create a UserSubscription
--------------------------

You can create a UserSubscription by issuing a HTTP **POST** request to the **/v1/usersubscription/** uri with a JSON object containing the following Key/Value:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "to_user",           "URI of the user being subscribed to",         "string",       "yes"
    "from_user",         "URI of the subscriber",                       "string",       "yes"

If the POST is successful, you will receive the following Response Header:

.. code-block:: js

    Status Code: 201
    Date: Sat, 10 Mar 2012 18:51:45 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8
    Location: http://www.dujour.im/v1/usersubscription/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/

You will get "Status Code: 201". A JSON object representing the created object will be returned.

If the subscription relationship already exists, then you will get "Forbidden Status Code: 403" with the message "This subscription already exists".

Update an Subscription 
----------------------

You can update a UserSubscription by issuing a HTTP **PUT** request to the **/v1/usersubscription/USERSUBSCRIPTION_ID/** uri with a JSON object containing the following Keys/Values:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "to_user",           "URI of the user being subscribed to",         "string",       "no"
    "from_user",         "URI of the subscriber",                       "string",       "no"

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

The easiest way to update is to **PUT** the entire UserSubscription (with id USERSUBSCRIPTION_ID) JSON object to **/v1/usersubscription/USERSUBSCRIPTION_ID/** and update the required fields (listed above). All the other fields will be ignored.

Delete an Item
---------------

You can delete a UserSubscription by issuing a HTTP **DELETE** request to **/v1/usersubscription/USERSUBSCRIPTION_ID**.

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

Notification
=============

Description
-----------

An user's notification consists of Comments and Votes posted by other users on the user's image. 

The front-end should first find our how many notifications are avaiable and display it to the user. If the user clicks on the notification button, then then an AJAX call should be made to retrieve all the notification object array. You can reset the counter with the reset API.

Get Notification count for a User
---------------------------------

You can get the number of notifications for a User by issuing a HTTP **GET** request to **/v1/notification/count/** with the following parameters

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "user",            "URI of the the user",                             "string",           "yes" 

Example code:

.. code-block:: js

    /v1/notification/count/?user=/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/

The following JSON object is returned:

.. csv-table::
    :widths: 20 70 10
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "count",             "Number of notifications available",                        "Integer"

Example code:

.. code-block:: js

    {
        "count": 20
    }

Reset Notification count for a User
-----------------------------------

You can get the number of notifications for a User by issuing a HTTP **GET** request to **/v1/notification/reset_count/** with the following parameters

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "user",            "URI of the the user",                             "string",           "yes" 

Example code:

.. code-block:: js

    /v1/notification/reset_count/?user=/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/

The following JSON object is returned:

.. csv-table::
    :widths: 20 70 10
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "count",             "Number of notifications available",                        "Integer"

Example code:

.. code-block:: js

    {
        "count": 0
    }

Get Notifications of a User
---------------------------

You can get a user's notification by issuing a HTTP **GET** request to **/v1/notification/** with the following parameters


.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "user",            "URI of the the user",                             "string",           "yes" 
    "offset",           "The index of the first object after the query has been ordered",      "integer", "no"
    "limit",            "The number of comments to be returned after all comments are ordered. Default = ""all comments""", "string", "no"

Example code:

.. code-block:: js

    /v1/notification/?user=/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/

The following JSON object is returned:

.. csv-table::
    :widths: 20 70 10
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "meta",              "Information regarding the query. ""limit"", ""next"", ""offset"", ""previous"", ""total_count""", "string"
    "object",            "Array of returned Image and Wordbox objects",              "Array"

Example code:

.. code-block:: js

    {
        "meta": {
            "limit": 2,
            "next": "/v1/notification/?user=%2Fv1%2Fuser%2F59ddf65d-e5e7-56a2-9f33-77362b8fc20e%2F&limit=20&offset=20",
            "offset": 1,
            "previous": null,
            "total_count": 69 
        },
        "objects": [{
            "obj_type": "comment",
            ...
        }, {
            "obj_type": "vote",
            ...
        }, {
            "obj_type": "vote",
            ...
        }, {
            "obj_type": "comment",
            ...
        }]
    }



CommunityMembership
===================

Description
-----------

Resource the represents the membership that a user has in a community. 

Get information about a CommunityMembership
-------------------------------------------

You can get the following information about a CommunityMembership by issuing a HTTP **GET** request to **/v1/communitymembership/COMMUNITYMEMBERSHIP_ID** with the following parameters:

.. csv-table::
    :widths: 10 60 10 20
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "",                 "",                                                 "",                 ""

The following is returned:

.. csv-table::
    :widths: 10 50 40
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "community",         "URI of the community object",                              "string"
    "member",            "URI of the user object",                                   "string" 
    "created_time",      "Time the communitymembership was created",                 "string, rfc-3339 standard"
    "obj_type",          "Type of resource",                                         "string"
    "last_visited",      "Date of the last time the user visited (reset_last_visted_date)","string, rfc-3339 standard"
    "created_time",      "The time the comment was created",                         "string, rfc-3339 standard"
    "updated_time",      "The time the comment was updated",                         "string, rfc-3339 standard"
    "new_posts",         "Number of image uploads since \'last visted\'",            "integer"
    "resource_uri",      "URI of the Friendship object",                             "string"

Example code:

.. code-block:: js

    {
        "community": "/v1/community/dec0c7df-1656-560f-80d8-380ee7ffe6bc/",
        "created_time": "2012-05-26T05:46:50",
        "member": "/v1/user/e88864da-41bc-54c7-8ce1-37212fab3245/",
        "obj_type": "communitymembership",
        "resource_uri": "/v1/communitymembership/f02a5052-0a9b-5705-9383-505df45926d1/"
        "created_time": "2012-05-28T18:40:30+00:00",
        "updated_time": "2012-05-28T18:40:30+00:00",
    }

Get the CommunityMemberships of a User 
--------------------------------------

You can get all the CommunityMemberships related to a user by issuing a HTTP **GET** request to **/v1/communitymembership/** with the following parameters:

.. csv-table::
    :widths: 10 60 10 20
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "member",           "URI of the user object",                           "string",           "no" 
    "offset",           "The index of the first object after the query has been ordered",      "integer", "no"
    "limit",            "The number of votes to be returned after all votes are ordered. Default = "all comments", "string", "no"

Results are given reverse chronologically be default (order_by=\"-created_time\")

Example code:

.. code-block:: js

    /v1/communitymembership/?member=/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/

The following JSON object is returned:

.. csv-table::
    :widths: 10 80 10
    :header-rows: 1

    "Field",            "Description",                                       "Type"
    "meta",             "Information regarding the query. ""limit"", ""next"", ""offset"", ""previous"", ""total_count""", "string"
    "objects",          "Array of objects",                                  "integer" 

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
            "obj_type": "communitymembership",
            "resource_uri": "/v1/communitymembership/358fe7aa-8db8-56bd-9de9-0effa8cd2678/",
            ...
        }, {
            "obj_type": "communitymembership",
            "resource_uri": "/v1/communitymembership/f02a5052-0a9b-5705-9383-505df45926d1/",
            ...
        }]
    }

Get the CommunityMemberships of a Community
-------------------------------------------

You can get all the CommunityMemberships related to Community by issuing a HTTP **GET** request to **/v1/communitymembership/** with the following parameters:

.. csv-table::
    :widths: 10 60 10 20
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "community",        "URI of the Community object",                      "string",           "no" 
    "offset",           "The index of the first object after the query has been ordered",      "integer", "no"
    "limit",            "The number of votes to be returned after all votes are ordered. Default = "all comments", "string", "no"

Example code:

.. code-block:: js

    /v1/communitymembership/?community=/v1/community/dec0c7df-1656-560f-80d8-380ee7ffe6bc/

The following JSON object is returned:

.. csv-table::
    :widths: 10 80 10
    :header-rows: 1

    "Field",            "Description",                                       "Type"
    "meta",             "Information regarding the query. ""limit"", ""next"", ""offset"", ""previous"", ""total_count""", "string"
    "objects",          "Array of objects",                                  "integer" 

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
            "obj_type": "communitymembership",
            "resource_uri": "/v1/communitymembership/358fe7aa-8db8-56bd-9de9-0effa8cd2678/",
            ...
        }, {
            "obj_type": "communitymembership",
            "resource_uri": "/v1/communitymembership/f02a5052-0a9b-5705-9383-505df45926d1/",
            ...
        }]
    }

Get CommunityMemberships if a User is part of a Community 
---------------------------------------------------------

This can be used to find out if a particular user is a member of a set of communities. For example, you might want to see if User 1 is a member of Community A, Community B, or Community C.

You can get all the communitymemberships where a user is a member of set of communities by issuing a HTTP **GET** request to **/v1/communitymembership/** with the following parameters:

.. csv-table::
    :widths: 10 60 10 20
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "member",           "URI of the User object",                          "string",           "yes" 
    "community",        "comma delimited list of URI of the Community objects","string",           "yes" 
    "limit",            "The number of votes to be returned after all votes are ordered. Default = "all comments", "string", "no"
    "offset",           "The index of the first object after the query has been ordered",      "integer", "no"
    "order_by",          "Currently, this is not an option. The default is "-created_time" where the '-' signifies reverse chronological order.",   "string", "no"

For example, if you want to see whether or not a user [USER] is a member of the following Communities [COMMUNITY1, COMMUNITY2, COMMUNITY3], you can issue a HTTP **GET** request to **/v1/communitymembership?member=USER_URI&community=COMMUNITY1_URI,COMMUNITY2_URI,COMMUNITY3_URI**. You can turn off pagination by adding "limit=0" to the **GET** request. This will give you all the results in one array.

The returned JSON object will contain an array of CommunityMembership objects. These objects represent Community Memberships objects that the User is related to (or communities the user is a member of). 

.. csv-table::
    :widths: 10 80 10
    :header-rows: 1

    "Field",            "Description",                                       "Type"
    "meta",             "Information regarding the query. ""limit"", ""next"", ""offset"", ""previous"", ""total_count""", "string"
    "objects",          "Array of objects",                                  "integer" 

Example code:

.. code-block:: js


    {
        "meta": {
            "limit": 2,
            "next": null,
            "offset": 0,
            "previous": null,
            "total_count": 2
        },
        "objects": [{
            "created_time": "2012-03-10T18:51:45",
            "obj_type": "vote",
            "user": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
            "parent": "/v1/comment/cf97b7f1-94b2-57da-84e2-67c111dbbfcf/",
            "resource_uri": "/v1/vote/cc22601b-7c12-5445-907d-853cb79ebfb4/"
        }, {
            "created_time": "2012-03-10T16:43:02",
            "obj_type": "vote",
            "user": "/v1/user/ef84d8b6-b790-5096-b10e-dc13037997af/",
            "parent": "/v1/comment/cf97b7f1-94b2-57da-84e2-67c111dbbfcf/",
            "resource_uri": "/v1/vote/0e02ea09-3151-5966-b98a-162b03b09d27/"
        }]
    }

Reset last visited date
-----------------------

You can get reset the last visited date for a CommunityMembership by issuing a HTTP **GET** request to **/v1/communitymembership/COMMUNITYMEMBERSHIP_ID/visited/** with the following parameters

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"

Example code:

.. code-block:: js

    /v1/communitymembership/687a1b6a-e5a4-5674-8032-4a388dd19ed0/visited/

An empty object is returned with a Status Code of 200.

Create a CommunityMembership
----------------------------

You can create a CommunityMembership by issuing a HTTP **POST** request to **/v1/communitymembership** with a JSON object containing the following Key/Value:

.. csv-table::
    :widths: 10 80 10
    :header-rows: 1

    "Key",              "Value",                                            "Type"
    "community",        "URI of the community object",                      "string" 
    "member",           "URI of the user object",                           "string" 

If the POST is successful, you will receive the following Response Header:

.. code-block:: js

    Status Code: 201
    Date: Sat, 10 Mar 2012 18:51:45 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8
    Location: http://www.derek.dev.dujour.im/v1/communitymembership/f02a5052-0a9b-5705-9383-505df45926d1/

You will get "Status Code: 201". Furthermore, the URI of the newly created resource will be under the "Location" field.

Delete a CommunityMembership
----------------------------

You can remove a CommunityMembership by issuing a HTTP **DELETE** request to **/v1/communitymembership/COMMUNITYMEMBERSHIP_ID**.
If the DELETE is successful, you will receive the following Response Header

.. code-block:: js

    Status Code: 204
    Date: Sat, 10 Mar 2012 19:24:35 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8

You will get "Status Code: 204".



