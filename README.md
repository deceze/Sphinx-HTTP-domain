# Sphinx HTTP Domain

## Description

Sphinx plugin to add an HTTP domain, allowing the documentation of
RESTful HTTP methods.

You can document simple methods, wrap any arguments in the path
with curly-braces:

    .. http:method:: GET /api/foo/bar/{id}/{slug}

       :arg id: An id
       :arg slug: A slug

       Retrieve list of foobars matching given id.

Query string parameters are also supported:

    .. http:method:: GET /api/foo/bar/?id

       :param id: An id

       Search for a list of foobars matching given id.
       
*This is very rudimentary and experimental code at the moment.*

## Installation

Run `pip install sphinx-http-domain`.

Then, add `sphinx_http_domain` to your conf.py:

    extensions = ['sphinx_http_domain']

## Development

- Version: pre-Alpha
- Homepage: https://github.com/deceze/Sphinx-HTTP-domain

For contributions, please fork this project on GitHub!

### Author

David Zentgraf (https://github.com/deceze)

### Contributors

- Simon Law (https://github.com/sfllaw)
