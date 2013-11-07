*********
Actions
*********

.. _actions-vote:

Votes
======

Description
-----------

You can vote on any media objects.

Get information about a vote
-------------------------------

You can get the following information about a vote by issuing a HTTP **GET** request to **/v1/vote/VOTE_ID**. The following is returned:

.. csv-table::
    :widths: 10 60 30
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "owner",             "URI for the user that created the vote",                   "string"
    "parent",            "URI of object the vote refers to",                         "string"
    "created_time",      "Tme the comment was created",                              "string, rfc-3339 standard"
    "obj_type",          "Type of resource",                                         "string"
    "resource_uri"       "URI of the current object"                                 "string

Example code:

.. code-block:: js

    {
        "created_time": "2012-03-10T16:43:02",
        "obj_type": "vote",
        "owner": "/v1/user/ef84d8b6-b790-5096-b10e-dc13037997af/",
        "parent": "/v1/comment/cf97b7f1-94b2-57da-84e2-67c111dbbfcf/",
        "resource_uri": "/v1/vote/0e02ea09-3151-5966-b98a-162b03b09d27/"
    }

Get votes related to an object
------------------------------

You can get all the votes related to a media object by issuing a HTTP **GET** request to **/v1/vote/** with the following parameters:

.. csv-table::
    :widths: 10 60 10 20
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "parent",           "URI of the parent object",                         "string",           "no" 
    "offset",           "The index of the first object after the query has been ordered",      "integer", "no"
    "limit",            "The number of votes to be returned after all votes are ordered. Default = ""all comments""", "string", "no"
    "order_by",         "Currently, this is not an option. The default is "-created_time" where the '-' signifies reverse chronological order.",   "string", "no"

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
            "limit": 2,
            "next": null,
            "offset": 0,
            "previous": null,
            "total_count": 2
        },
        "objects": [{
            "created_time": "2012-03-10T18:51:45",
            "obj_type": "vote",
            "owner": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
            "parent": "/v1/comment/cf97b7f1-94b2-57da-84e2-67c111dbbfcf/",
            "resource_uri": "/v1/vote/cc22601b-7c12-5445-907d-853cb79ebfb4/"
        }, {
            "created_time": "2012-03-10T16:43:02",
            "obj_type": "vote",
            "owner": "/v1/user/ef84d8b6-b790-5096-b10e-dc13037997af/",
            "parent": "/v1/comment/cf97b7f1-94b2-57da-84e2-67c111dbbfcf/",
            "resource_uri": "/v1/vote/0e02ea09-3151-5966-b98a-162b03b09d27/"
        }]
    }

Get votes related to an object and owner
----------------------------------------

This can be used to find out if a particular owner voted on an object or a set of objects.

You can get all the votes related to a media object by issuing a HTTP **GET** request to **/v1/vote/** with the following parameters:

.. csv-table::
    :widths: 10 60 10 20
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "owner",            "URI of the user object",                          "string",           "yes" 
    "parent",           "comma delimited list of URI of the parent objects","string",           "yes" 
    "limit",            "The number of votes to be returned after all votes are ordered. Default = ""all comments""", "string", "no"
    "offset",           "The index of the first object after the query has been ordered",      "integer", "no"
    "order_by",          "Currently, this is not an option. The default is "-created_time" where the '-' signifies reverse chronological order.",   "string", "no"

For example, if you want to see whether or not a user [OWNER] voted on a set of images [IMAGE1, IMAGE2, IMAGE3], you can issue a HTTP **GET** request to **/v1/vote/?owner=USER_URI&parent=IMAGE1_URI,IMAGE2_URI,IMAGE3_URI**. You can turn off pagination by adding "limit=0" to the **GET** request. This will give you all the results in one array.

The returned JSON object will contain an array of vote objects. These objects represent parent objects that the user has voted "up" on. Parent objects that were not voted on or were un-voted will not appear. The following JSON object is returned:

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
            "owner": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
            "parent": "/v1/comment/cf97b7f1-94b2-57da-84e2-67c111dbbfcf/",
            "resource_uri": "/v1/vote/cc22601b-7c12-5445-907d-853cb79ebfb4/"
        }, {
            "created_time": "2012-03-10T16:43:02",
            "obj_type": "vote",
            "owner": "/v1/user/ef84d8b6-b790-5096-b10e-dc13037997af/",
            "parent": "/v1/comment/cf97b7f1-94b2-57da-84e2-67c111dbbfcf/",
            "resource_uri": "/v1/vote/0e02ea09-3151-5966-b98a-162b03b09d27/"
        }]
    }

Create a vote
-------------

You can vote on an object by issuing a HTTP **POST** request to **/v1/vote/** with a JSON object containing the following Key/Value:

.. csv-table::
    :widths: 10 80 10
    :header-rows: 1

    "Key",              "Value",                                       "Type"
    "parent",           "URI of the parent object",                    "string"

If the POST is successful, you will receive the following Response Header:

.. code-block:: js

    Status Code: 201
    Date: Sat, 10 Mar 2012 18:51:45 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8
    Location: http://www.dujour.im/v1/vote/0e02ea09-3151-5966-b98a-162b03b09d27/

You will get "Status Code: 201". Furthermore, the URI of the newly created resource will be under the "Location" field.

Delete a vote
-------------

You can un-vote on a media object by issuing a HTTP **DELETE** request to **/v1/vote/VOTE_ID**.
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

.. _actions-comment:

Comments
========

Description
-----------

You can comment on any media object

Get information about a comment
-------------------------------

You can get the following information about a comment by issuing a HTTP **GET** request to **/v1/comment/COMMENT_ID**. The following is returned:

.. csv-table::
    :widths: 10 60 30
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "message",           "The comment text",                                         "string"
    "owner",             "URI for the user that created the comment",                "string"
    "parent",            "URI of object the comment refers to",                      "string"
    "created_time",      "The time the comment was created",                         "string, rfc-3339 standard"
    "total_votes",       "The number of times this comment was voted on",            "integer"
    "resource_uri",      "URI of the current object"                                 "string"
    "username",          "Username of the owner",                                    "string"
    "name",              "Full name of the owner",                                   "string"

Example code:

.. code-block:: js

    {
        "created_time": "2012-07-07T02:50:55+00:00",
        "message": "I really like it",
        "name": "D.B. Tsai",
        "owner": "/v1/user/bda6243d-d76d-52e3-b872-20b2eba84257/",
        "parent": "/v1/image/55c2be2a-c93f-550c-b232-c015e8edd976/",
        "resource_uri": "/v1/comment/b01c4821-496f-5de2-9f36-86f5548ea61b/",
        "total_votes": 46,
        "username": "DBTsai"
    }

Get comments related to an object
---------------------------------

You can get all the comments related to a parent object by issuing a HTTP **GET** request to **/v1/comment/** with the following parameters


.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "parent",           "URI of the parent object",                         "string",           "yes" 
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
            "limit": 2,
            "next": "/v1/comment/?limit=2&parent=%2Fv1%2Fimage%2Fb62fb9b4-9c13-50c3-8c85-2c87e96553b3%2F&offset=3&order_by=-created_time",
            "offset": 1,
            "previous": null,
            "total_count": 25
        },
        "objects": [{
            "created_time": "2012-02-19T18:52:50",
            "message": "my first comment",
            "name": "Derek Chang",
            "username": "derek",
            "owner": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
            "parent": "/v1/image/b62fb9b4-9c13-50c3-8c85-2c87e96553b3/",
            "resource_uri": "/v1/comment/d4b9929d-16c8-5f6e-bf06-16c50b88cd5c/",
            "total_votes": 0
        }, {
            "created_time": "2012-02-19T18:52:28",
            "message": "my second comment",
            "name": "Michael Zhang",
            "username": "zikegcwk",
            "owner": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
            "parent": "/v1/image/b62fb9b4-9c13-50c3-8c85-2c87e96553b3/",
            "resource_uri": "/v1/comment/5d9b6cae-4664-55b2-8683-52c4c3f901b8/",
            "total_votes": 0
        }]
    }

**NOTE** If the parent object is a User, then this is equivalent to reading comments on a User's wall

Create a comment
----------------

You can post a comment by issuing a HTTP **POST** request to the **/v1/comment/** uri with a JSON object containing the following Key/Value:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "parent",           "URI of the parent object",                     "string",       "yes"
    "owner",            "URI of the user object",               "string",       "yes"
    "message",          "comment message",                              "string",       "yes"

If the POST is successful, you will receive the following Response Header:

.. code-block:: js

    Status Code: 201
    Date: Sat, 10 Mar 2012 18:51:45 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8
    Location: http://www.dujour.im/v1/comment/5d9b6cae-4664-55b2-8683-52c4c3f901b8/

You will get "Status Code: 201". 

**NOTE** If the parent object is a User, then this is equivalent to writing a comment on a User's wall

Update a comment
----------------

You can update a comment by issuing a HTTP **PATCH** request to **/v1/comment/COMMENT_ID/** uri with a JSON object containing the following Keys/Values:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "parent",           "URI of the parent object",                     "string",       "yes"
    "message",          "comment message",                              "string",       "yes"

If the PUT is successful, you will receive the following Response Header:

.. code-block:: js

    Status Code: 202
    Date: Sat, 10 Mar 2012 19:24:35 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8

You will get "Status Code: 202" if the PATCH request is successful.


Delete a comment
----------------

You can delete a comment by issuing a HTTP **DELETE** request to **/v1/comment/COMMENT_ID**.

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




.. _actions-newsfeed:

Newsfeed
========

Description
-----------

An owner's newsfeed consists of Images and Wordboxes posted by other users he/she subscribes to


Get Newsfeed of a User
---------------------------------

You can get a user's newsfeed by issuing a HTTP **GET** request to **/v1/newsfeed/** with the following parameters


.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "owner",            "URI of the the user",                             "string",           "yes" 
    "offset",           "The index of the first object after the query has been ordered",      "integer", "no"
    "limit",            "The number of comments to be returned after all comments are ordered. Default = ""all comments""", "string", "no"

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
            "next": "/v1/comment/?limit=2&parent=%2Fv1%2Fimage%2Fb62fb9b4-9c13-50c3-8c85-2c87e96553b3%2F&offset=3&order_by=-created_time",
            "offset": 1,
            "previous": null,
            "total_count": 25
        },
        "objects": [{
            "obj_type": "image",
            ...
        }, {
            "obj_type": "wordbox",
            ...
        }, {
            "obj_type": "wordbox",
            ...
        }, {
            "obj_type": "image",
            ...
        }]
    }
