# -*- coding: utf-8 -*-
"""
    Fields for the HTTP domain.
"""

from docutils import nodes

from sphinx.util.docfields import GroupedField, TypedField


class ResponseField(TypedField):
    """
    Like a TypedField, but with automatic descriptions.

    Just like a TypedField, you can use a ResponseField with or without
    a type::

        :param 200: description of response
        :type 200: SomeObject

        -- or --

        :param SomeObject 200: description of response

    In addition, ResponseField will provide a default description of
    the status code, if you provide none::

        :param 404:

        -- is equivalent to --

        :param 404: Not Found
    """
    # List of HTTP Status Codes, derived from:
    # http://en.wikipedia.org/wiki/List_of_HTTP_status_codes
    status_codes = {
        # 1xx Informational
        '100': 'Continue',
        '101': 'Switching Protocols',
        '102': 'Processing',
        '122': 'Request-URI too long',
        # 2xx Success
        '200': 'OK',
        '201': 'Created',
        '202': 'Accepted',
        '203': 'Non-Authoritative Information',
        '204': 'No Content',
        '205': 'Reset Content',
        '206': 'Partial Content',
        '207': 'Multi-Status',
        '226': 'IM Used',
        # 3xx Redirection
        '300': 'Multiple Choices',
        '301': 'Moved Permanently',
        '302': 'Found',
        '303': 'See Other',
        '304': 'Not Modified',
        '305': 'Use Proxy',
        '306': 'Switch Proxy',
        '307': 'Temporary Redirect',
        # 4xx Client Error
        '400': 'Bad Request',
        '401': 'Unauthorized',
        '402': 'Payment Requrired',
        '403': 'Forbidden',
        '404': 'Not Found',
        '405': 'Method Not Allowed',
        '406': 'Not Acceptable',
        '407': 'Proxy Authentication Requried',
        '408': 'Request Timeout',
        '409': 'Conflict',
        '410': 'Gone',
        '411': 'Length Required',
        '412': 'Precondition Failed',
        '413': 'Request Entity Too Large',
        '414': 'Request-URI Too Long',
        '415': 'Unsupported Media Type',
        '416': 'Requested Range Not Satisfiable',
        '417': 'Expectation Failed',
        '418': "I'm a teapot",
        '422': 'Unprocessable Entity',
        '423': 'Locked',
        '424': 'Failed Dependency',
        '425': 'Unordered Collection',
        '426': 'Upgrade Required',
        '444': 'No Response',
        '449': 'Retry With',
        '450': 'Block by Windows Parental Controls',
        '499': 'Client Closed Request',
        # 5xx Server Error
        '500': 'Interal Server Error',
        '501': 'Not Implemented',
        '502': 'Bad Gateway',
        '503': 'Service Unavailable',
        '504': 'Gateway Timeout',
        '505': 'HTTP Version Not Supported',
        '506': 'Variant Also Negotiates',
        '507': 'Insufficient Storage',
        '509': 'Bandwith Limit Exceeded',
        '510': 'Not Extended',
    }

    def default_content(self, fieldarg):
        """
        Given a fieldarg, returns the status code description in list form.

        The default status codes are provided in self.status_codes.
        """
        try:
            return [nodes.Text(self.status_codes[fieldarg])]
        except KeyError:
            return []

    def make_entry(self, fieldarg, content):
        # Wrap Field.make_entry, but intercept empty content and replace
        # it with default content.
        if not content:
            content = self.default_content(fieldarg)
        return super(TypedField, self).make_entry(fieldarg, content)


class NoArgGroupedField(GroupedField):
    def __init__(self, *args, **kwargs):
        super(NoArgGroupedField, self).__init__(*args, **kwargs)
        self.has_arg = False

    def make_field(self, types, domain, items):
        if len(items) == 1 and self.can_collapse:
            super(NoArgGroupedField, self).make_field(types, domain, items)
        fieldname = nodes.field_name('', self.label)
        listnode = self.list_type()
        for fieldarg, content in items:
            par = nodes.paragraph()
            par += content
            listnode += nodes.list_item('', par)
        fieldbody = nodes.field_body('', listnode)
        return nodes.field('', fieldname, fieldbody)
