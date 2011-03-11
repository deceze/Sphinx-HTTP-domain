# -*- coding: utf-8 -*-
"""
    Nodes for the HTTP domain.
"""

from docutils import nodes

from sphinx.util.texescape import tex_escape_map


class HttpNode(nodes.Part, nodes.Inline, nodes.TextElement):
    """Generic HTTP node."""
    _writers = ['text', 'html', 'latex', 'man']

    def set_first(self):
        try:
            self.children[0].first = True
        except IndexError:
            pass

    @classmethod
    def contribute_to_app(cls, app):
        kwargs = {}
        for writer in cls._writers:
            visit = getattr(cls, 'visit_' + writer, None)
            depart = getattr(cls, 'depart_' + writer, None)
            if visit and depart:
                kwargs[writer] = (visit, depart)
        app.add_node(cls, **kwargs)

    @staticmethod
    def visit_text(self, node):
        pass

    @staticmethod
    def depart_text(self, node):
        pass

    @staticmethod
    def visit_latex(self, node):
        pass

    @staticmethod
    def depart_latex(self, node):
        pass

    @staticmethod
    def visit_man(self, node):
        pass

    @staticmethod
    def depart_man(self, node):
        pass


class desc_http_method(HttpNode):
    """HTTP method node."""
    def astext(self):
        return nodes.TextElement.astext(self) + ' '

    @staticmethod
    def depart_text(self, node):
        self.add_text(' ')

    @staticmethod
    def visit_html(self, node):
        self.body.append(self.starttag(node, 'tt', '',
                                       CLASS='descclassname deschttpmethod'))

    @staticmethod
    def depart_html(self, node):
        self.body.append(' </tt>')

    @staticmethod
    def visit_latex(self, node):
        self.body.append(r'\code{')
        self.literal_whitespace += 1

    @staticmethod
    def depart_latex(self, node):
        self.body.append(r'}~')
        self.literal_whitespace -= 1

    @staticmethod
    def depart_man(self, node):
        self.body.append(r'\~')


class desc_http_url(HttpNode):
    """HTTP URL node."""
    @staticmethod
    def visit_html(self, node):
        self.body.append(self.starttag(node, 'tt', '',
                                       CLASS='descname deschttpurl'))

    @staticmethod
    def depart_html(self, node):
        self.body.append('</tt>')

    @staticmethod
    def visit_latex(self, node):
        self.body.append(r'\bfcode{')
        self.literal_whitespace += 1

    @staticmethod
    def depart_latex(self, node):
        self.body.append(r'}')
        self.literal_whitespace -= 1


class desc_http_path(HttpNode):
    """HTTP path node. Contained in the URL node."""
    @staticmethod
    def visit_html(self, node):
        self.body.append(self.starttag(node, 'span', '',
                                       CLASS='deschttppath'))

    @staticmethod
    def depart_html(self, node):
        self.body.append('</span>')


class desc_http_patharg(HttpNode):
    """
    HTTP path argument node. Contained in the path node.

    This node is created when {argument} is found inside the path.
    """
    wrapper = (u'{', u'}')

    def astext(self, node):
        return (self.wrapper[0] +
                nodes.TextElement.astext(node) +
                self.wrapper[1])

    @staticmethod
    def visit_text(self, node):
        self.add_text(node.wrapper[0])

    @staticmethod
    def depart_text(self, node):
        self.add_text(node.wrapper[1])

    @staticmethod
    def visit_html(self, node):
        self.body.append(
            self.starttag(node, 'em', '', CLASS='deschttppatharg') +
            self.encode(node.wrapper[0]) +
            self.starttag(node, 'span', '', CLASS='deschttppatharg')
        )

    @staticmethod
    def depart_html(self, node):
        self.body.append('</span>' +
                         self.encode(node.wrapper[1]) +
                         '</em>')

    @staticmethod
    def visit_latex(self, node):
        self.body.append(r'\emph{' +
                         node.wrapper[0].translate(tex_escape_map))

    @staticmethod
    def depart_latex(self, node):
        self.body.append(node.wrapper[1].translate(tex_escape_map) +
                         '}')

    @staticmethod
    def visit_man(self, node):
        self.body.append(self.defs['emphasis'][0])
        self.body.append(self.deunicode(node.wrapper[0]))

    @staticmethod
    def depart_man(self, node):
        self.body.append(self.deunicode(node.wrapper[1]))
        self.body.append(self.defs['emphasis'][1])


class desc_http_query(HttpNode):
    """HTTP query string node. Contained in the URL node."""
    prefix = u'?'

    def astext(self):
        return self.prefix + nodes.TextElement.astext(self)

    @staticmethod
    def visit_text(self, node):
        self.add_text(node.prefix)
        node.set_first()

    @staticmethod
    def visit_html(self, node):
        self.body.append(
            self.starttag(node, 'span', '', CLASS='deschttpquery') +
            self.encode(node.prefix)
        )
        node.set_first()

    @staticmethod
    def depart_html(self, node):
        self.body.append('</span>')

    @staticmethod
    def visit_latex(self, node):
        self.body.append(node.prefix.translate(tex_escape_map))
        node.set_first()

    @staticmethod
    def visit_man(self, node):
        self.body.append(self.deunicode(node.prefix))
        node.set_first()


class desc_http_queryparam(HttpNode):
    """
    HTTP query string parameter node. Contained in the query string node.

    This node is created for each parameter inside a query string.
    """
    child_text_separator = u'&'
    first = False

    @staticmethod
    def visit_text(self, node):
        if not node.first:
            self.add_text(node.child_text_separator)

    @staticmethod
    def visit_html(self, node):
        if not node.first:
            self.body.append(self.encode(node.child_text_separator))
        self.body.append(self.starttag(node, 'em', '',
                                       CLASS='deschttpqueryparam'))

    @staticmethod
    def depart_html(self, node):
        self.body.append('</em>')

    @staticmethod
    def visit_latex(self, node):
        if not node.first:
            self.body.append(
                node.child_text_separator.translate(tex_escape_map)
            )
        self.body.append('\emph{')

    @staticmethod
    def depart_latex(self, node):
        self.body.append('}')

    @staticmethod
    def visit_man(self, node):
        if not node.first:
            self.body.append(self.deunicode(node.child_text_separator))
        self.body.append(self.defs['emphasis'][0])

    @staticmethod
    def depart_man(self, node):
        self.body.append(self.defs['emphasis'][1])


class desc_http_fragment(HttpNode):
    """HTTP fragment node. Contained in the URL node."""
    prefix = u'#'

    def astext(self):
        return self.prefix + nodes.TextElement.astext(self)

    @staticmethod
    def visit_text(self, node):
        self.add_text(node.prefix)

    @staticmethod
    def visit_html(self, node):
        self.body.append(self.encode(node.prefix) +
                         self.starttag(node, 'em', '',
                                       CLASS='deschttpfragment'))

    @staticmethod
    def depart_html(self, node):
        self.body.append('</em>')

    @staticmethod
    def visit_latex(self, node):
        self.body.append(node.prefix.translate(tex_escape_map) +
                         r'\emph{')

    @staticmethod
    def depart_latex(self, node):
        self.body.append('}')

    @staticmethod
    def visit_man(self, node):
        self.body.append(self.deunicode(node.prefix))
        self.body.append(self.defs['emphasis'][0])

    @staticmethod
    def depart_man(self, node):
        self.body.append(self.defs['emphasis'][1])


class desc_http_response(HttpNode):
    """HTTP response node."""

    @staticmethod
    def visit_html(self, node):
        self.body.append(self.starttag(node, 'strong', '',
                                       CLASS='deschttpresponse'))

    @staticmethod
    def depart_html(self, node):
        self.body.append('</strong>')

    @staticmethod
    def visit_latex(self, node):
        self.body.append(r'\textbf{')

    @staticmethod
    def depart_latex(self, node):
        self.body.append('}')

    @staticmethod
    def visit_man(self, node):
        self.body.append(self.defs['strong'][0])

    @staticmethod
    def depart_man(self, node):
        self.body.append(self.defs['strong'][1])
