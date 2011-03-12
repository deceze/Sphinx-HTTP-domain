# -*- coding: utf-8 -*-
"""
    sphinx.domains.http
    ~~~~~~~~~~~~~~~~~~~

    The HTTP domain.

    :copyright: Copyright 2011, David Zentgraf.
    :license: BSD, see LICENSE for details
"""

from itertools import izip

from docutils.nodes import literal, Text

from sphinx.locale import l_
from sphinx.domains import Domain, ObjType
from sphinx.roles import XRefRole
from sphinx.util.nodes import make_refnode

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
        'method': XRefRole(),
        'response': XRefRole(),
    }
    initial_data = {
        'method': {},    # name -> docname, sig, title, method
        'response': {},  # name -> docname, sig, title
    }

    def clear_doc(self, docname):
        """Remove traces of a document from self.data."""
        for typ in self.initial_data:
            for name, entry in self.data[typ].items():
                if entry[0] == docname:
                    del self.data[typ][name]

    def find_xref(self, env, typ, target):
        """Returns a self.data entry for *target*, according to *typ*."""
        try:
            return self.data[typ][target]
        except KeyError:
            return None

    def resolve_xref(self, env, fromdocname, builder,
                     typ, target, node, contnode):
        """
        Resolve the ``pending_xref`` *node* with the given *typ* and *target*.

        Returns a new reference node, to replace the xref node.

        If no resolution can be found, returns None.
        """
        match = self.find_xref(env, typ, target)
        if match:
            docname = match[0]
            sig = match[1]
            title = match[2]
            # Coerce contnode into the right nodetype
            nodetype = type(contnode)
            if issubclass(nodetype, literal):
                nodetype = self.directives[typ].nodetype
            # Override contnode with title, unless it has been manually
            # overridden in the text.
            if contnode.astext() == target:
                contnode = nodetype(title, title)
            else:
                child = contnode.children[0]
                contnode = nodetype(child, child)
            # Return the new reference node
            return make_refnode(builder, fromdocname, docname,
                                typ + '-' + target, contnode, sig)

    def get_objects(self):
        """
        Return an iterable of "object descriptions", which are tuples with
        five items:

        * `name`     -- fully qualified name
        * `dispname` -- name to display when searching/linking
        * `type`     -- object type, a key in ``self.object_types``
        * `docname`  -- the document where it is to be found
        * `anchor`   -- the anchor name for the object
        * `priority` -- how "important" the object is (determines placement
          in search results)

          - 1: default priority (placed before full-text matches)
          - 0: object is important (placed before default-priority objects)
          - 2: object is unimportant (placed after full-text matches)
          - -1: object should not show up in search at all
        """
        # Method descriptions
        for typ in self.initial_data:
            for name, entry in self.data[typ].iteritems():
                docname = entry[0]
                yield(name, name, typ, docname, typ + '-' + name, 0)


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
