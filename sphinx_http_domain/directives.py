# -*- coding: utf-8 -*-
"""
    sphinx.domains.http
    ~~~~~~~~~~~~~~~~~~~

    Directives for the HTTP domain.
"""

import re
from urlparse import urlsplit, parse_qsl

from docutils.nodes import literal, strong, Text
from docutils.parsers.rst import directives

from sphinx.locale import l_, _
from sphinx.directives import ObjectDescription
from sphinx.util.docfields import TypedField

from sphinx_http_domain.docfields import NoArgGroupedField, ResponseField
from sphinx_http_domain.nodes import (desc_http_method, desc_http_url,
                                      desc_http_path, desc_http_patharg,
                                      desc_http_query, desc_http_queryparam,
                                      desc_http_fragment, desc_http_response)
from sphinx_http_domain.utils import slugify, slugify_url


class HTTPDescription(ObjectDescription):
    def get_anchor(self, name, sig):
        """
        Returns anchor for cross-reference IDs.

        *name* is whatever :meth:`handle_signature()` returned.
        """
        return self.typ + '-' + self.get_id(name, sig)

    def get_entry(self, name, sig):
        """
        Returns entry to add for cross-reference IDs.

        *name* is whatever :meth:`handle_signature()` returned.
        """
        return name

    def get_id(self, name, sig):
        """
        Returns cross-reference ID.

        *name* is whatever :meth:`handle_signature()` returned.
        """
        return name

    def add_target_and_index(self, name, sig, signode):
        """
        Add cross-reference IDs and entries to self.indexnode, if applicable.

        *name* is whatever :meth:`handle_signature()` returned.
        """
        anchor = self.get_anchor(name, sig)
        id = self.get_id(name, sig)
        self.add_target(anchor=anchor, entry=self.get_entry(name, sig),
                        id=id, sig=sig, signode=signode)
        self.add_index(anchor=anchor, name=name, sig=sig)

    def add_target(self, anchor, id, entry, sig, signode):
        """Add cross-references to self.env.domaindata, if applicable."""
        if anchor not in self.state.document.ids:
            signode['names'].append(anchor)
            signode['ids'].append(anchor)
            signode['first'] = (not self.names)
            self.state.document.note_explicit_target(signode)
            data = self.env.domaindata['http'][self.typ]
            if id in data:
                otherdocname = data[id][0]
                self.env.warn(
                    self.env.docname,
                    'duplicate method description of %s, ' % sig +
                    'other instance in ' +
                    self.env.doc2path(otherdocname) +
                    ', use :noindex: for one of them',
                    self.lineno
                )
            data[id] = entry

    def add_index(self, anchor, name, sig):
        """
        Add index entries to self.indexnode, if applicable.

        *name* is whatever :meth:`handle_signature()` returned.
        """
        raise NotImplemented


class HTTPMethod(HTTPDescription):
    """
    Description of a general HTTP method.
    """
    typ = 'method'
    nodetype = literal

    option_spec = {
        'noindex': directives.flag,
        'title': directives.unchanged,
        'label-name': directives.unchanged,
    }
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
        return desc_http_method(method, method.upper())

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
        # Name and title
        name = self.options.get('label-name',
                                slugify_url(method.lower() + '-' + url))
        title = self.options.get('title', sig)
        return (method.upper(), url, name, title)

    def get_entry(self, name, sig):
        """
        Returns entry to add for cross-reference IDs.

        *name* is whatever :meth:`handle_signature()` returned.
        """
        method, _, _, title = name
        return (self.env.docname, sig, title, method)

    def get_id(self, name, sig):
        """
        Returns cross-reference ID.

        *name* is whatever :meth:`handle_signature()` returned.
        """
        return name[2]

    def add_index(self, anchor, name, sig):
        """
        Add index entries to self.indexnode, if applicable.

        *name* is whatever :meth:`handle_signature()` returned.
        """
        method, url, id, title = name
        if title != sig:
            self.indexnode['entries'].append(('single',
                                              _("%s (HTTP method)") % title,
                                              anchor, anchor))
        self.indexnode['entries'].append(
            ('single',
             _("%(method)s (HTTP method); %(url)s") % {'method': method,
                                                       'url': url},
             anchor, anchor)
        )


class HTTPResponse(HTTPDescription):
    """
    Description of a general HTTP response.
    """
    typ = 'response'
    nodetype = strong

    option_spec = {
        'noindex': directives.flag,
    }
    doc_field_types = [
        TypedField('data', label=l_('Data'),
                   names=('data',),
                   typenames=('datatype', 'type'),
                   typerolename='response',
                   can_collapse=True),
        NoArgGroupedField('contenttype', label=l_('Content Types'),
                          names=('contenttype', 'mimetype', 'format'),
                          can_collapse=True),
    ]

    def handle_signature(self, sig, signode):
        """
        Transform an HTTP response into RST nodes.
        Returns the reference name.
        """
        name = slugify(sig)
        signode += desc_http_response(name, sig)
        return name

    def get_entry(self, name, sig):
        return (self.env.docname, sig, sig)

    def add_index(self, anchor, name, sig):
        """
        Add index entries to self.indexnode, if applicable.

        *name* is whatever :meth:`handle_signature()` returned.
        """
        self.indexnode['entries'].append(('single',
                                          _("%s (HTTP response)") % sig,
                                          anchor, anchor))
        self.indexnode['entries'].append(('single',
                                          _("HTTP response; %s") % sig,
                                          anchor, anchor))
