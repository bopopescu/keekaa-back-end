********
Brands
********

Brand
=====

Description
------------

Brands are created by a user. They are assocaited with items

Get information about a Brand
-----------------------------

You can get the following information about a brand by issuing a HTTP **GET** request to **/v1/brand/BRAND_ID**. The following is returned:

.. csv-table::
    :widths: 10 60 30
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "owner",             "URI for the user that created the Brand",                  "string"
    "name",              "The name of the brand",                                    "string"
    "description",       "A description of the brand",                               "string"
    "address",           "The address for the brand",                                "string"
    "url_name",          "The URL of the brand website",                             "string"
    "item",              "URI of items belonging to this brand",                     "string"
    "comment",           "URI of all the comments regarding this brand",             "string"
    "created_time",      "The time the comment was created",                         "string, rfc-3339 standard"
    "updated_time",      "The time the comment was updated",                         "string, rfc-3339 standard"
    "total_votes",       "The number of times this brand was voted on",              "integer"
    "total_comments",    "The number of comments this brand has",                    "integer"
    "total_favorites",   "The number of times this brand was favorited",             "integer"
    "total_items",       "The number of items belonging to this brand",              "integer"
    "resource_uri",      "URI of the current object"                                 "string"

Example code:

.. code-block:: js

    {
        "address": "USA",
        "comment": "/v1/comment/?parent=/v1/brand/335e280d-a3cf-5311-b6e7-e89e91cfeb79/",
        "created_time": "2012-02-19T21:06:02",
        "description": "Fashion and quality at the best price",
        "item": [],
        "name": "H&M",
        "owner": "/v1/user/e88864da-41bc-54c7-8ce1-37212fab3245/",
        "resource_uri": "/v1/brand/335e280d-a3cf-5311-b6e7-e89e91cfeb79/",
        "total_comments":475 
        "total_favorites": 112,
        "total_items": 49,
        "total_votes": 500,
        "updated_time": "2012-02-19T21:06:02",
        "url_name": "www.HM.com"
    }

Get all Brands belonging to a user
----------------------------------

You can get all the brands related to a user by issuing a HTTP **GET** request to **/v1/brand/** with the following parameters


.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "owner",            "URI of the user object",                          "string",           "yes" 
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
            "total_count": 2000
        },
        "objects": [{
            "address": "USA[",
            "comment": "/v1/comment/?parent=/v1/brand/3ed72137-a76f-5d4f-9e77-1a595ff525db/",
            "created_time": "2012-01-15 09:36:15",
            "description": "Another brand",
            "item": "/v1/item/?brand=/v1/brand/3ed72137-a76f-5d4f-9e77-1a595ff525db/",
            "name": "Sand",
            "owner": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
            "resource_uri": "/v1/brand/3ed72137-a76f-5d4f-9e77-1a595ff525db/",
            "total_comments": 1,
            "total_favorites": 2,
            "total_items": 4,
            "total_votes": 3,
            "updated_time": "2012-01-15T09:36:15",
            "url_name": "www.somebrand.com"
        }, {
            "address": "USA",
            "comment": "/v1/comment/?parent=/v1/brand/335e280d-a3cf-5311-b6e7-e89e91cfeb79/",
            "created_time": "2012-02-19T21:06:02",
            "description": "Fashion and quality at the best price",
            "item": [],
            "name": "H&M",
            "owner": "/v1/user/e88864da-41bc-54c7-8ce1-37212fab3245/",
            "resource_uri": "/v1/brand/335e280d-a3cf-5311-b6e7-e89e91cfeb79/",
            "total_comments":475 
            "total_favorites": 112,
            "total_items": 49,
            "total_votes": 500,
            "updated_time": "2012-02-19T21:06:02",
            "url_name": "www.HM.com"
        }]
    }

Create a Brand
--------------

You can create a brand by issuing a HTTP **POST** request to **/v1/brand/** with a JSON object containing the following Key/Value:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "owner",            "URI for the user that created the comment",    "string",       "yes"
    "name",             "The name of the brand",                        "string",       "yes"
    "description",      "A description of the brand",                   "string",       "no"
    "address",          "The address for the brand",                    "string",       "no"
    "url_name",         "The URL of the brand website",                 "string",       "no"

If the POST is successful, you will receive the following Response Header:

.. code-block:: js

    Status Code: 201
    Date: Sat, 10 Mar 2012 18:51:45 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8
    Location: http://www.dujour.im/v1/brand/335e280d-a3cf-5311-b6e7-e89e91cfeb79/

You will get "Status Code: 201". A JSON object representing the created object will be returned.

Update a Brand
--------------

You can update a brand by issuing a HTTP **PUT** request to **/v1/brand/BRAND_ID/** with a JSON object containing the following Keys/Values:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "owner",            "URI for the user that created the comment",    "string",       "no"
    "name",             "The name of the brand",                        "string",       "no"
    "description",      "A description of the brand",                   "string",       "no"
    "address",          "The address for the brand",                    "string",       "no"
    "url_name",         "The URL of the brand website",                 "string",       "no"

You will get "Status Code: 201". A JSON object representing the updated object will be returned.

.. code-block:: js

    Status Code: 204
    Date: Sat, 10 Mar 2012 19:24:35 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8

You will get "Status Code: 204" if the PUT request is successful.

The easiest way to update is to **PUT** the entire brand (with id BRAND_ID) JSON object to **/v1/brand/BRAND_ID/** and update the required fields (listed above). All the other fields will be ignored.

Delete a Brand
---------------


You can delete a brand by issuing a HTTP **DELETE** request to **/v1/brand/BRAND_ID**.

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

Item
====

Description
------------

Items are created by users but also belong to a Brand.

Get information about an Item
-----------------------------

You can get the following information about an item by issuing a HTTP **GET** request to **/v1/item/ITEM_ID**. The following is returned:

.. csv-table::
    :widths: 10 60 30
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "owner",             "URI for the user that created the comment",                "string"
    "name",              "The name of the item",                                     "string"
    "description",       "A description of the item",                                "string"
    "size",              "The size of the item",                                     "string"
    "price",             "The price of the item",                                    "string"
    "color",             "The color of the item",                                    "string"
    "url",               "The URL of the of where this item is found",               "string"
    "brand_name",        "The name of the associated brand",                             "string"
    "brand",             "URI of brand associated with this item",                   "string"
    "comment",           "URI of all the comments regarding this item",              "string"
    "created_time",      "The time the comment was created",                         "string, rfc-3339 standard"
    "updated_time",      "The time the comment was updated",                         "string, rfc-3339 standard"
    "total_votes",       "The number of times this item was voted on",               "integer"
    "total_comments",    "The number of comments this item has",                     "integer"
    "total_favorites",   "The number of times this comment was favorited",           "integer"
    "resource_uri",      "URI of the current object"                                 "string"

Example code:

.. code-block:: js

    {
        "brand": "/v1/brand/ad2e636a-b6b4-5e1d-9342-57695e740916/",
        "brand_name": "H&M",
        "color": "black",
        "comment": "/v1/comment/?parent=/v1/item/8bddae8f-3ad0-5518-82cf-b2caaa1335cd/",
        "created_time": "2012-03-18 07:53:44",
        "description": "colorful",
        "name": "V-neck T"
        "owner": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
        "price": "29.99",
        "resource_uri": "/v1/item/8bddae8f-3ad0-5518-82cf-b2caaa1335cd/",
        "size": "M",
        "total_comments": 20,
        "total_favorites": 50,
        "total_votes": 30,
        "updated_time": "2012-03-18T07:56:07",
        "url": "www.hm.com"
    }

Get all Items belonging to a User
----------------------------------

You can get all the items related to a user by issuing a HTTP **GET** request to **/v1/item/** with the following parameters


.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "owner",            "URI of the user object",                          "string",           "yes" 
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
            "brand": "/v1/brand/ad2e636a-b6b4-5e1d-9342-57695e740916/",
            "brand_name": "H&M",
            "color": "black",
            "comment": "/v1/comment/?parent=/v1/item/8bddae8f-3ad0-5518-82cf-b2caaa1335cd/",
            "created_time": "2012-03-18 07:53:44",
            "description": "colorful",
            "name": "V-neck T"
            "owner": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
            "price": "29.99",
            "resource_uri": "/v1/item/8bddae8f-3ad0-5518-82cf-b2caaa1335cd/",
            "size": "M",
            "total_comments": 20,
            "total_favorites": 50,
            "total_votes": 30,
            "updated_time": "2012-03-18T07:56:07",
            "url": "www.hm.com"
        }, {
            "brand": "/v1/brand/8d4340a2-85cd-5423-935d-e4c9b581a83d/",
            "brand_name": "Wilson",
            "color": "brown",
            "comment": "/v1/comment/?parent=/v1/item/4daf6af9-b8eb-5587-b18d-ae02f490fdfd/",
            "created_time": "2012-03-09 09:31:55",
            "description": "a real genuine football",
            "name": "football",
            "owner": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
            "price": "49.99",
            "resource_uri": "/v1/item/4daf6af9-b8eb-5587-b18d-ae02f490fdfd/",
            "size": "NA",
            "total_comments": 300,
            "total_favorites": 125,
            "total_votes": 433,
            "updated_time": "2012-03-18T07:44:35",
            "url": "www.football.com"
        }]
    }

Get all Items belonging to a User
----------------------------------

You can get all the items related to a brand by issuing a HTTP **GET** request to **/v1/item/** with the following parameters


.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "brand",            "URI of the brand object",                          "string",           "yes" 
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

Sample code similar to the previous example above.

Create an Item
--------------

You can create an item by issuing a HTTP **POST** request to **/v1/item/** with a JSON object containing the following Key/Value:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "owner",            "URI for the user that created the item",       "string",       "yes"
    "name",             "The name of the item",                         "string",       "yes"
    "description",      "A description of the item",                    "string",       "no"
    "brand_name",       "The name of the associated brand",             "string",       "no"
    "url",              "The URL of the item website",                  "string",       "no"
    "price",            "The price of the item",                        "string",       "no"
    "size",             "The size of the item",                         "string",       "no"
    "color",            "The color of the item",                        "string",       "no"

If the POST is successful, you will receive the following Response Header:

.. code-block:: js

    Status Code: 201
    Date: Sat, 10 Mar 2012 18:51:45 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8
    Location: http://www.dujour.im/v1/item/1384853c-9252-5a32-8cb6-f9b66e97e7c7/

You will get "Status Code: 201". A JSON object representing the created object will be returned.

Update an Item
--------------

You can update an item by issuing a HTTP **PUT** request to **/v1/item/ITEM_ID/** with a JSON object containing the following Keys/Values:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "owner",            "URI for the user that created the comment",    "string",       "no"
    "name",             "The name of the item",                         "string",       "no"
    "description",      "A description of the item",                    "string",       "no"
    "brand_name",       "The name of the associated brand",             "string",       "no"
    "url",              "The URL of the item website",                  "string",       "no"
    "price",            "The price of the item",                        "string",       "no"
    "size",             "The size of the item",                         "string",       "no"
    "color",            "The color of the item",                        "string",       "no"

You will get "Status Code: 201". A JSON object representing the updated object will be returned.

.. code-block:: js

    Status Code: 204
    Date: Sat, 10 Mar 2012 19:24:35 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8

You will get "Status Code: 204" if the PUT request is successful.

The easiest way to update is to **PUT** the entire item (with id ITEM_ID) JSON object to **/v1/item/ITEM_ID/** and update the required fields (listed above). All the other fields will be ignored.

Delete an Item
---------------

You can delete a item by issuing a HTTP **DELETE** request to **/v1/item/ITEM_ID**.

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

ItemTag
=======

Description
------------

ItemTags represent items that are found in a particular image.

Get information about an ItemTag
--------------------------------

You can get the following information about an itemtag by issuing a HTTP **GET** request to **/v1/itemtag/ITEMTAG_ID**. The following is returned:

.. csv-table::
    :widths: 10 60 30
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "owner",             "URI for the user that created the itemtag",                "string"
    "image",             "URI for the image",                                        "string"
    "item",              "URI for the item",                                         "string"
    "num",               "The number of the itemtag",                                "string"
    "x",                 "The x position of the itemtag",                            "string"
    "y",                 "The y position of the itemtag",                            "string"
    "created_time",      "The time the comment was created",                         "string, rfc-3339 standard"
    "updated_time",      "The time the comment was updated",                         "string, rfc-3339 standard"
    "resource_uri",      "URI of the current object"                                 "string"

Example code:

.. code-block:: js

    {
        "created_time": "2012-03-18 18:19:05",
        "image": "/v1/image/35d5a336-bc39-584a-aa3e-f3e92880a1f6/",
        "item": "/v1/item/fb91ea8e-29c5-564f-a799-faefef006701/",
        "num": 1,
        "owner": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
        "resource_uri": "/v1/itemtag/954d18dc-d4c7-56ee-b2f7-9061659fabb0/",
        "updated_time": "2012-03-18T18:19:05",
        "x": 0.456,
        "y": 0.987
    }

Get all ItemTags belonging to an Image 
--------------------------------------

You can get all the items related to an image by issuing a HTTP **GET** request to **/v1/itemtag/** with the following parameters


.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "image",            "URI of the image object",                          "string",           "yes" 
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
            "created_time": "2012-03-18 18:51:49",
            "image": "/v1/image/35d5a336-bc39-584a-aa3e-f3e92880a1f6/",
            "item": "/v1/item/ca1320b3-e355-54e8-8d10-0e770b0ceb24/",
            "num": 2,
            "owner": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
            "resource_uri": "/v1/itemtag/10724fa8-9a67-5a07-b6fb-a500ad5241c3/",
            "updated_time": "2012-03-18T18:51:49",
            "x": 0.456,
            "y": 0.987
        }, {
            "created_time": "2012-03-18 18:19:05",
            "image": "/v1/image/35d5a336-bc39-584a-aa3e-f3e92880a1f6/",
            "item": "/v1/item/fb91ea8e-29c5-564f-a799-faefef006701/",
            "num": 2,
            "owner": "/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
            "resource_uri": "/v1/itemtag/954d18dc-d4c7-56ee-b2f7-9061659fabb0/",
            "updated_time": "2012-03-18T18:48:47",
            "x": 0.456,
            "y": 0.987
        }]
    }


Create an ItemTag
------------------

You can create an itemtag by issuing a HTTP **POST** request to **/v1/itemtag/** with a JSON object containing the following Key/Value:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "owner",             "URI for the user that created the itemtag (must be logged in)",   "string",       "yes"
    "image",             "URI for the image",                           "string",       "yes"
    "item",              "URI for the item",                            "string",       "yes"
    "num",               "The number of the itemtag",                   "string",       "yes"
    "x",                 "The x position of the itemtag",               "string",       "yes"
    "y",                 "The y position of the itemtag",               "string",       "yes"

If the POST is successful, you will receive the following Response Header:

.. code-block:: js

    Status Code: 201
    Date: Sat, 10 Mar 2012 18:51:45 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8
    Location: http://www.dujour.im/v1/itemtag/10724fa8-9a67-5a07-b6fb-a500ad5241c3/

You will get "Status Code: 201". A JSON object representing the created object will be returned.

Update an ItemTag
------------------

You can update an itemtag by issuing a HTTP **PUT** request to **/v1/itemtag/ITEMTAG_ID/** with a JSON object containing the following Keys/Values:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",              "Value",                                        "Type",         "Required"
    "image",             "URI for the image",                           "string",       "no"
    "item",              "URI for the item",                            "string",       "no"
    "num",               "The number of the itemtag",                   "string",       "no"
    "x",                 "The x position of the itemtag",               "string",       "no"
    "y",                 "The y position of the itemtag",               "string",       "no"

If the PUT is successful, you will receive the following Response Header:

.. code-block:: js

    Status Code: 204
    Date: Sat, 10 Mar 2012 19:24:35 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8

You will get "Status Code: 201". A JSON object representing the updated object will be returned.

The easiest way to update is to **PUT** the entire itemtag (with id ITEMTAG_ID) JSON object to **/v1/itemtag/ITEMTAG_ID/** and update the required fields (listed above). All the other fields will be ignored.

Delete an ItemTag
------------------

You can delete a itemtag by issuing a HTTP **DELETE** request to **/v1/itemtag/ITEMTAG_ID**.

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

