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
from sphinx.util.docfields import TypedField

from sphinx_http_domain.docfields import ResponseField
from sphinx_http_domain.nodes import (desc_http_method, desc_http_url,
                                      desc_http_path, desc_http_patharg,
                                      desc_http_query, desc_http_queryparam,
                                      desc_http_fragment)


class HTTPMethod(ObjectDescription):
    """
    Description of a general HTTP method.
    """
    doc_field_types = [
        TypedField('argument', label=l_('Path arguments'),
                   names=('arg', 'argument', 'patharg'),
                   typenames=('argtype', 'pathargtype'),
                   can_collapse=True),
        TypedField('parameter', label=l_('Query params'),
                   names=('param', 'parameter', 'queryparam'),
                   typenames=('paramtype', 'queryparamtype'),
                   typerolename='response',
                   can_collapse=True),
        TypedField('optional_parameter', label=l_('Opt. params'),
                   names=('optparam', 'optional', 'optionalparameter'),
                   typenames=('optparamtype',),
                   can_collapse=True),
        TypedField('fragment', label=l_('Fragments'),
                   names=('frag', 'fragment'),
                   typenames=('fragtype',),
                   can_collapse=True),
        ResponseField('response', label=l_('Responses'),
                      names=('resp', 'responds', 'response'),
                      typerolename='response',
                      can_collapse=True)
    ]

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

    def node_from_method(self, method):
        """Returns a ``desc_http_method`` Node from a ``method`` string."""
        if method is None:
            method = 'GET'
        method = method.upper()
        return desc_http_method(method, method)

    def node_from_url(self, url):
        """Returns a ``desc_http_url`` Node from a ``url`` string."""
        if url is None:
            raise ValueError
        # Split URL into path, query, and fragment
        path, query, fragment = self.split_url(url)
        urlnode = desc_http_url()
        urlnode += self.node_from_path(path)
        node = self.node_from_query(query)
        if node:
            urlnode += node
        node = self.node_from_fragment(fragment)
        if node:
            urlnode += node
        return urlnode

    def node_from_path(self, path):
        """Returns a ``desc_http_path`` Node from a ``path`` string."""
        if path:
            pathnode = desc_http_path(path)
            path_segments = self.path_re.findall(path)[:-1]
            for text, arg in path_segments:
                pathnode += Text(text)
                if arg:
                    arg = arg[1:-1]     # Strip off { and }
                    pathnode += desc_http_patharg(arg, arg)
            return pathnode
        else:
            raise ValueError

    def node_from_query(self, query):
        """Returns a ``desc_http_query`` Node from a ``query`` string."""
        if query:
            querynode = desc_http_query(query)
            query_params = query.split('&')
            for p in query_params:
                querynode += desc_http_queryparam(p, p)
            return querynode

    def node_from_fragment(self, fragment):
        """Returns a ``desc_http_fragment`` Node from a ``fragment`` string."""
        if fragment:
            return desc_http_fragment(fragment, fragment)

    def split_url(self, url):
        """
        Splits a ``url`` string into its components.
        Returns (path, query string, fragment).
        """
        _, _, path, query, fragment = urlsplit(url)
        return (path, query, fragment)

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
        signode += self.node_from_method(method)
        signode += self.node_from_url(url)
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
