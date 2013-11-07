**********
Accounts
**********

Me resource 
============

Description
-----------

If you want to sign in, send a GET request to "/v1/me" (literally that path) with username, password and stay_signed_in flag. If you want to sign out, just send a DELETE request to "/v1/me". If you are already signed in and want to get information about the current user, send a GET request to "/v1/me" without any parameters.

Get information about the current user
---------------------------------------

You can get the information about the current user by issuing a HTTP **GET** request to **/v1/me** without ANY parameters:

The following is returned:

.. csv-table::
    :widths: 10 50 40
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "user",              "URI of the UserProfile object",                            "string"

Example code:

.. code-block:: js

    {
        "user": "/v1/user/3fc01072-8555-5509-9edc-061844f4a46a/"
    }

Note that if the user is not signed in, the backend will return a 401 Unauthorized error.

Sign in and get information about the current user
---------------------------------------------------

You can get the information about the current user by issuing a HTTP **GET** request to **/v1/me** with the following parameters

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "user",             "username or user's email",                         "string",           "yes" 
    "password",         "the password of the user",                         "string",           "yes"
    "stay_signed_in",   "should be True or False",                          "string",           "no"

The following is returned:

.. csv-table::
    :widths: 10 50 40
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "user",              "URI of the UserProfile object",                            "string"

Example code:

.. code-block:: js

    {
        "user": "/v1/user/3fc01072-8555-5509-9edc-061844f4a46a/"
    }

Note that if user doesn't exist, the backend will return 404 Not Found error.


the user is not signed in, the backend will return return 401 Unauthorized error.
If the password is wrong, the backend will return 401 Unauthorized error.
If the user is not activated, the backend will return 403 Forbidden error.
If everything is going correctly, show the url of user's resource with 200 status code.


Sign out
========
You can sign out by issuing a HTTP **DELETE** request to **/v1/me**.

If successful, it will return 204. If the user is not signed in, it will return 401.


UsernameResource
=================

Description
-------------
This api can help front-end to find the actual user object uri by using the username as input. If this username doesn't exist on the site, it will return 404 error status.
You can get the uri of a user by issuing a HTTP **GET** request to **/v1/username/[username]** where [username] is the username that front-end wants to look up.

Example code /v1/username/dbtsai:

.. code-block:: js

    {
        "user": "/v1/user/3fc01072-8555-5509-9edc-061844f4a46a/"
    }

EmailResource
=================

Description
-------------
This api can help front-end to find the actual user object uri by using the email as input. If this email doesn't exist on the site, it will return 404 error status.
You can get the uri of a user by issuing a HTTP **GET** request to **/v1/username/[email]** where [email] is the username that front-end wants to look up.

Example code /v1/email/dbtsai@dbtsai.org:

.. code-block:: js

    {
        "user": "/v1/user/3fc01072-8555-5509-9edc-061844f4a46a/"
    }

User
========

Description
-----------

User information


Get information about a User
-------------------------------

You can get the following information about a User by issuing a HTTP **GET** request to **/v1/user/USER_ID**. The following is returned:

.. csv-table::
    :widths: 10 60 30
    :header-rows: 1

    "Field",             "Description",                                              "Type"
    "first_name",        "First name of user",                                       "string"
    "middle_name",       "Middle name of user"",                                     "string"
    "last_name",         "Last name of user",                                        "string"
    "about_me",          "Information about the user",                               "string"
    "fashion_statement", "The user's fashion statement",                             "string"
    "gender",            "User's Gender",                                            "char"
    "email",             "User's email address (must be correct format)",            "string"
    "website",           "User's website address",                                   "string"
    "created_time",      "The time the comment was created",                         "string, rfc-3339 standard"
    "updated_time",      "The time the comment was updated",                         "string, rfc-3339 standard"
    "profile_image_standard", "Profile images of standard size",                     "array"
    "profile_image_thumbnail", "Profile images of thumbnail size",                   "array"
    "community",         "URI for the all the communities this user belongs to",     "string"
    "obj_type",          "the type of resource",                                     "string"
    "resource_uri"       "URI of the current object"                                 "string
    "total_images",      "Total number of images the user has uploaded",             "integer"
    "total_subscribers", "Total number of subscribers the user has",                 "integer"
    "total_wordboxes",   "Total number of wordboxes the user has uploaded",          "integer"
    "age",               "Age of the user -- COMING SOON",                           "integer"
    "location",          "Location of user -- COMING SOON",                          "string"

Example code:

.. code-block:: js

    {
        "about_me": "I believe that everyone is unique and beautiful.",
        "created_time": "2011-11-11T04:55:57",
        "email": "michael@dujour.im",
        "fashion_statement": "It just has to be comfortable and unique! If it adds a bit of rebelliousness, then perfect! \n",
        "first_name": "Michael",
        "gender": "M",
        "last_name": "Zhang",
        "middle_name": "",
        "community": "/v1/community/?member=/v1/user/59ddf65d-e5e7-56a2-9f33-77362b8fc20e/",
        "obj_type": "user",
        "profile_image_thumbnail": {
            "obj_type": "image",
            "versions": [
                {
                    "height": 750,
                    "resource_uri": "https://d956iao6yp65z.cloudfront.net/images/1322037522_c2ac-c03e2aed-d467-57ed-9091-7b8c28cb21f3_0500x0750.jpg",
                    "width": 500
                },
                {
                    "height": 375,
                    "resource_uri": "https://d956iao6yp65z.cloudfront.net/images/1322037522_c2ac-c03e2aed-d467-57ed-9091-7b8c28cb21f3_0500x0750.jpg",
                    "width": 250
                },
                {
                    "height": 187,
                    "resource_uri": "https://d956iao6yp65z.cloudfront.net/images/1322037522_c2ac-c03e2aed-d467-57ed-9091-7b8c28cb21f3_0500x0750.jpg",
                    "width": 125
                },
                {
                    "height": 93,
                    "resource_uri": "https://d956iao6yp65z.cloudfront.net/images/1322037522_c2ac-c03e2aed-d467-57ed-9091-7b8c28cb21f3_0500x0750.jpg",
                    "width": 62
                }
            ], ...
        },
        "profile_image_standard": {
            "obj_type": "image",
            "versions": [
                {
                    "height": 750,
                    "resource_uri": "https://d956iao6yp65z.cloudfront.net/images/1322037522_c2ac-c03e2aed-d467-57ed-9091-7b8c28cb21f3_0500x0750.jpg",
                    "width": 500
                },
                {
                    "height": 375,
                    "resource_uri": "https://d956iao6yp65z.cloudfront.net/images/1322037522_c2ac-c03e2aed-d467-57ed-9091-7b8c28cb21f3_0500x0750.jpg",
                    "width": 250
                },
                {
                    "height": 187,
                    "resource_uri": "https://d956iao6yp65z.cloudfront.net/images/1322037522_c2ac-c03e2aed-d467-57ed-9091-7b8c28cb21f3_0500x0750.jpg",
                    "width": 125
                },
                {
                    "height": 93,
                    "resource_uri": "https://d956iao6yp65z.cloudfront.net/images/1322037522_c2ac-c03e2aed-d467-57ed-9091-7b8c28cb21f3_0500x0750.jpg",
                    "width": 62
                }
            ], ...
        },
        "resource_uri": "/v1/user/e88864da-41bc-54c7-8ce1-37212fab3245/",
        "total_images": 99,
        "total_subscribers": 999,
        "total_wordboxes": 32,
        "username": "zikegcwk",
        "website": "www.facebook.com/michaelkezhang\n\nwww.wmphotostudio.com"
    }

Get all Users that belong to a Community 
----------------------------------------

You can get all the communitys related to user by issuing a HTTP **GET** request to **/v1/community/** with the following parameters


.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "community",        "URI of the community object",                      "string",           "yes" 
    "offset",           "The index of the first object after the query has been ordered",      "integer", "no"
    "limit",            "The number of comments to be returned after all comments are ordered. Default = "all comments", "string", "no"
    "order_by",         "Currently, this is not an option. The default is "-created_time" where the '-' signifies reverse chronological order.",   "string", "no"

Example code:

.. code-block:: js

    /v1/user/?community=/v1/community/dec0c7df-1656-560f-80d8-380ee7ffe6bc/

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
            "username": "derek",
            "obj_type": "user",
            ...
        }, {
            "username": "dbtsai",
            "obj_type": "user",
            ...
        }]
    }

Get all Images/Wordboxes (Media) for a User's Collection
--------------------------------------------------------

You can get all the images/wordboxes (media) of a User's Collection by issuing a HTTP **GET** request to **/v1/usercollection/** with the following parameters


.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "user",             "URI of the the user",                              "string",           "yes" 
    "offset",           "The index of the first object after the query has been ordered",      "integer", "no"
    "limit",            "The number of comments to be returned after all comments are ordered. Default = ""all comments""", "string", "no"

Example code:

.. code-block:: js

    http://www.dujour.im/v1/usercollection/?user=/v1/user/2091d4db-972b-5104-8718-8a2575c1504c/

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

This can also be used to find if a particular User collected certain Images or Wordboxes.  For example, if you want to see whether or not a user [USER] collected a set of images or wordboxes [IMAGE1, IMAGE2, WORDBOX1, WORDBOX2], you can issue a HTTP **GET** request to **/v1/usercollection/?user=USER_URI&media=IMAGE1_URI,IMAGE2_URI,WORDBOX1_URI,WORDBOX2_URI**. A list of objects (from the input list) that the User has collected will be returned. You can turn off pagination by adding "limit=0" to the **GET** request. This will give you all the results in one array.

Get all Subscriptions (User) belonging to a user
------------------------------------------------

You can get all the subscriptions (other users that someone subscribes to) belonging to a user by issuing a HTTP **GET** request to **/v1/user/** with the following parameters


.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Parameter",        "Description",                                      "Type",             "Required"
    "subscriber",       "URI of the user",                                  "string",           "yes" 
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
            "username": "derek",
            "obj_type": "user",
            "resource_uri": "/v1/user/c7d0c99c-6aaf-59d7-b4fc-2093b4b9d4d8",
            ...
        }, {
            "username": "dbtsai",
            "obj_type": "user",
            "resource_uri": "/v1/user/6e6db817-18b7-50d2-b25c-1b8272331a7a",
            ...
        }]
    }

Create a User
----------------
This api can be used to create a new user. You can sign up an account by issuing a HTTP **POST** request to **/v1/user/** with application/json. Please use UsernameResource and EmailResource to check if they are available first!!!

Example code:

.. code-block:: js

	{
		"username":"DBTsai20133",
		"email":"dbtsai+04@dbtsai.org",
		"password":"dbdczk",
		"first_name":"David",
		"last_name": "Tsai"
	}

Error handing:

.. code-block:: js

	461           # The username doesn't match r'@([A-Za-z0-9_]+)'
	462           # The username already exists
	463           # This email is not valid
	464           # The email already exists

Update User information 
------------------------

You can update a User's information by issuing a HTTP **PATCH** request to **/v1/user/USER_ID/** with a JSON object containing the following Keys/Values:

.. csv-table::
    :widths: 20 60 10 10
    :header-rows: 1

    "Key",               "Value",                                           "Type",         "Required"
    "first_name",        "First name of user",                              "string",       "no"
    "middle_name",       "Middle name of user"",                            "string",       "no"
    "last_name",         "Last name of user",                               "string",       "no"
    "about_me",          "Information about the user",                      "string",       "no"
    "fashion_statement", "The user's fashion statement",                    "string",       "no"
    "gender",            "User's Gender",                                   "char",         "no"
    "email",             "User's email address (must be correct format)",   "string",       "no"
    "website",           "User's website address",                          "string",       "no"
    "age",               "Age of the user -- COMING SOON",                  "integer",      "no"
    "location",          "Location of user -- COMING SOON",                 "string",       "no"
    "profile_image_standard", "Image URI",                                  "string",       "no"
    "profile_image_thumbnail", "Image URI",                                 "string",       "no"

If the PATCH is successful, you will receive the following Response Header:

.. code-block:: js

    Status Code: 204
    Date: Sat, 10 Mar 2012 19:24:35 GMT
    Connection: keep-alive
    Content-Length: 0
    Server: nginx/1.0.5
    Vary: Cookie
    Content-Type: text/html; charset=utf-8

You will get "Status Code: 204" if the PATCH request is successful.


Add Images to a User's Collection
---------------------------------

You can add Images to a User's Collection by issuing a HTTP **POST** request to **/v1/user/USER_ID/add_to_collection/** with a JSON object containing the following Keys/Values:

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

If the Images are successfully added to the User's Collection, you will receive the following Response Header:

.. code-block:: js

    Status Code: 201
    Date: Sun, 06 May 2012 06:43:02 GMT
    Transfer-Encoding: chunked
    Connection: keep-alive
    Server: nginx/1.0.5
    Content-Type: text/html; charset=utf-8
    Location: http://www.dujour.im/v1/user/dec0c7df-1656-560f-80d8-380ee7ffe6bc/add/

You will get "Status Code: 201" if the POST request is successful.

Remove Images from a User's Collection 
--------------------------------------

You can remove Images from a User's Collection by issuing a HTTP **POST** request to **/v1/user/USER_ID/remove_from_collection/** uri with a JSON object containing the following Keys/Values:

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

If the Images are successfully removed to the User's Collection, you will receive the following Response Header:

.. code-block:: js

    Status Code: 201
    Date: Sun, 06 May 2012 06:43:02 GMT
    Transfer-Encoding: chunked
    Connection: keep-alive
    Server: nginx/1.0.5
    Content-Type: text/html; charset=utf-8
    Location: http://www.dujour.im/v1/user/dec0c7df-1656-560f-80d8-380ee7ffe6bc/add/

You will get "Status Code: 201" if the POST request is successful.

Add WordBoxes to a User's Collection 
------------------------------------

Same as above for Images. Just use 'wordbox' instead of 'image'.

Remove WordBoxes from a User's Collection
-----------------------------------------

Same as above for Images. Just use 'wordbox' instead of 'image'.
