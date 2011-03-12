Sphinx HTTP Domain
==================

Description
-----------

Sphinx plugin to add an HTTP domain, allowing the documentation of
RESTful HTTP methods.

*This is very rudimentary and experimental code at the moment.*

HTTP methods
------------

You can document simple methods, wrap any arguments in the path
with curly-braces::

    .. http:method:: GET /api/foo/bar/{id}/{slug}

       :arg id: An id
       :arg slug: A slug

       Retrieve list of foobars matching given id.

Query string parameters are also supported, both mandatory and
optional::

    .. http:method:: GET /api/foo/bar/?id&slug

       :param id: An id
       :optparam slug: A slug

       Search for a list of foobars matching given id.

As well, you can provide types for parameters and arguments::

    .. http:method:: GET /api/foo/bar/{id}/?slug
       
       :arg integer id: An id
       :optparam string slug: A slug

       Search for a list of foobars matching given id.

Fragments are also supported::

    .. http:method:: GET /#!/username

       :fragment username: A username

       Renders a user's profile page.

Plus, you can document the responses with their response codes::

    .. http:method:: POST /api/foo/bar/

       :param string slug: A slug
       :response 201: A foobar was created successfully.
       :response 400:

       Create a foobar.

To refer to an HTTP method, use ``:http:method:``::

    .. http:method:: GET /api/
       :label-name: get-root
       :title: API root

    The :http:method:`get-root` contains all of the API.


HTTP responses
--------------

Documenting responses is also simple::

   .. http:response:: Foobar object

      A foobar object looks like this::

      .. source-code:: js
         {
            'slug': SLUG
         }
   
      :data string SLUG: A slug
      :format: JSON

To refer to an HTTP response, use ``:http:response:``::

   .. http:response:: Foobar object

   A :http:response:`foobar-object` is returned when you foo the bar.


Installation
------------

Run ``pip install sphinx-http-domain``.

Then, add ``sphinx_http_domain`` to your conf.py::

    extensions = ['sphinx_http_domain']


Development
-----------

- Version: pre-Alpha
- Homepage: https://github.com/deceze/Sphinx-HTTP-domain

For contributions, please fork this project on GitHub!


Author
``````

David Zentgraf (https://github.com/deceze)


Contributors
````````````

- Simon Law (https://github.com/sfllaw)
