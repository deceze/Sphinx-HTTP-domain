# -*- coding: utf-8 -*-
"""
    The HTTP domain.
"""

import re

from docutils import nodes

from sphinx import addnodes
from sphinx.locale import l_, _
from sphinx.domains import Domain, ObjType
from sphinx.directives import ObjectDescription


http_method_sig_re = re.compile(r'^(GET|POST|PUT|DELETE)?\s?(\S+)(.*)$')


class HTTPMethod(ObjectDescription):
    def handle_signature(self, sig, signode):
        m = http_method_sig_re.match(sig)
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
        'method':    ObjType(l_('method'),    'method')
    }
    directives = {
        'method':       HTTPMethod
    }
    roles = {
        # 'method':  RESTXRefRole(),
    }


def setup(app):
    app.add_domain(HTTPDomain)
