# Sphinx HTTP Domain

## Description

Sphinx plugin to add an HTTP domain, allowing the documentation of
RESTful HTTP methods.

    .. http:method:: GET /api/foo/bar/:id/:slug

       :param id: An id
       :param slug: A slug

       Retrieve list of foobars matching given id.
       
*This is very rudimentary and experimental code at the moment.*

## Installation

Run pip install sphinx-http-domain.

Then, add `sphinx_http_domain` to your conf.py:

    extensions = ['sphinx_http_domain']
