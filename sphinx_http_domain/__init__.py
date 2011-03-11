# -*- coding: utf-8 -*-
"""
    sphinx.domains.http
    ~~~~~~~~~~~~~~~~~~~

    The HTTP domain.

    :copyright: Copyright 2011, David Zentgraf.
    :license: BSD, see LICENSE for details
"""

import re

from docutils import nodes

from sphinx import addnodes
from sphinx.locale import l_
from sphinx.domains import Domain, ObjType
from sphinx.directives import ObjectDescription


class HTTPMethod(ObjectDescription):
    """
    Description of a general HTTP method.
    """
    # RE for HTTP method signatures
    sig_re = re.compile(
        r'^'
        r'(GET|POST|PUT|DELETE)?\s?'    # verb
        r'(\S+)'                        # url
        r'(.*)'                         # query
        r'$'
    )

    def handle_signature(self, sig, signode):
        """
        Transform an HTTP method signature into RST nodes.
        Returns (method name, classname if any).
        """
        m = sig_re.match(sig)
        if m is None:
            raise ValueError

        verb, url, query = m.groups()
        if verb is None:
            verb = 'GET'

        signode += addnodes.desc_addname(verb, verb)
        signode += addnodes.desc_name(url, url)

        if query:
            params = query.strip().split()
            for param in params:
                signode += addnodes.desc_optional(param, param)

        return url


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
