# -*- coding: utf-8 -*-
"""
    sphinx.domains.http
    ~~~~~~~~~~~~~~~~~~~

    The HTTP domain.

    :copyright: Copyright 2011, David Zentgraf.
    :license: BSD, see LICENSE for details
"""

from itertools import izip
import re
from urlparse import urlsplit, parse_qsl

from docutils.nodes import Text

from sphinx.locale import l_
from sphinx.domains import Domain, ObjType
from sphinx.directives import ObjectDescription

from sphinx_http_domain.nodes import (desc_http_method, desc_http_url,
                                      desc_http_path, desc_http_patharg,
                                      desc_http_query, desc_http_queryparam,
                                      desc_http_fragment)


class HTTPMethod(ObjectDescription):
    """
    Description of a general HTTP method.
    """
    # RE for HTTP method signatures
    sig_re = re.compile(
        (
            r'^'
            r'(?:(GET|POST|PUT|DELETE)\s+)?'  # HTTP method
            r'(.+)'                           # URL
            r'\s*$'
        ),
        re.IGNORECASE
    )

    # Note, path_re.findall() will produce an extra ('', '') tuple
    # at the end of its matches. You should strip it off, or you will
    path_re = re.compile(
        (
            r'([^{]*)'                  # Plain text
            r'(\{[^}]*\})?'             # {arg} in matched braces
        ),
        re.VERBOSE
    )

    def handle_method(self, method, signode):
        if method is None:
            method = 'GET'
        method = method.upper()
        signode += desc_http_method(method, method)

    def handle_url(self, url, signode):
        if url is None:
            raise ValueError
        # Split URL into path, query, and fragment
        _, _, path, query, fragment = urlsplit(url)
        urlnode = desc_http_url()
        # Create nodes for the path
        if path:
            pathnode = desc_http_path(path)
            path_segments = self.path_re.findall(path)[:-1]
            for text, arg in path_segments:
                pathnode += Text(text)
                if arg:
                    arg = arg[1:-1]     # Strip off { and }
                    pathnode += desc_http_patharg(arg, arg)
            urlnode += pathnode
        else:
            raise ValueError
        # Create nodes for the query string
        if query:
            querynode = desc_http_query(query)
            query_params = query.split('&')
            for p in query_params:
                querynode += desc_http_queryparam(p, p)
            urlnode += querynode
        # Create a node for the fragment
        if fragment:
            urlnode += desc_http_fragment(fragment, fragment)
        # Add urlnode to signode
        signode += urlnode

    def handle_signature(self, sig, signode):
        """
        Transform an HTTP method signature into RST nodes.
        Returns (method name, full URL).
        """
        # Match the signature to extract the method and URL
        m = self.sig_re.match(sig)
        if m is None:
            raise ValueError
        method, url = m.groups()
        # Append nodes to signode for method and url
        self.handle_method(method, signode)
        self.handle_url(url, signode)
        return (method, url)


class HTTPDomain(Domain):
    """HTTP language domain."""
    name = 'http'
    label = 'HTTP'
    object_types = {
        'method': ObjType(l_('method'), 'method')
    }
    directives = {
        'method': HTTPMethod
    }
    roles = {
        # 'method': RESTXRefRole(),
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
