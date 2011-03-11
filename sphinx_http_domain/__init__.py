# -*- coding: utf-8 -*-
"""
    sphinx.domains.http
    ~~~~~~~~~~~~~~~~~~~

    The HTTP domain.

    :copyright: Copyright 2011, David Zentgraf.
    :license: BSD, see LICENSE for details
"""

from itertools import izip

from sphinx.locale import l_
from sphinx.domains import Domain, ObjType

from sphinx_http_domain.directives import HTTPMethod, HTTPResponse
from sphinx_http_domain.nodes import (desc_http_method, desc_http_url,
                                      desc_http_path, desc_http_patharg,
                                      desc_http_query, desc_http_queryparam,
                                      desc_http_fragment, desc_http_response)


class HTTPDomain(Domain):
    """HTTP language domain."""
    name = 'http'
    label = 'HTTP'
    object_types = {
        'method': ObjType(l_('method'), 'method'),
        'response': ObjType(l_('response'), 'response'),
    }
    directives = {
        'method': HTTPMethod,
        'response': HTTPResponse,
    }
    roles = {
        # 'method': HTTPXRefRole(),
        # 'response': HTTPXRefRole(),
    }


def setup(app):
    app.add_domain(HTTPDomain)
    desc_http_method.contribute_to_app(app)
    desc_http_url.contribute_to_app(app)
    desc_http_path.contribute_to_app(app)
    desc_http_patharg.contribute_to_app(app)
    desc_http_query.contribute_to_app(app)
    desc_http_queryparam.contribute_to_app(app)
    desc_http_fragment.contribute_to_app(app)
    desc_http_response.contribute_to_app(app)
