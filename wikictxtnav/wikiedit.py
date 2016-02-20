# encoding: utf-8
# Created by Noah Kantrowitz
# Copyright (c) 2008 Noah Kantrowitz. All rights reserved.
import urllib

from trac.core import *
from trac.web.chrome import add_ctxtnav
from trac.web.api import IRequestFilter

from trac.util.translation import _

class WikiEditModule(Component):

    implements(IRequestFilter)

    # IRequestFilter methods
    def pre_process_request(self, req, handler):
        return handler

    def post_process_request(self, req, template, data, content_type):

        if req.path_info.startswith('/wiki') or req.path_info == '/':
            action = req.args.get('action', 'view')

            if action == 'view' and data and 'page' in data:
                page = data['page']
                if 'WIKI_MODIFY' in req.perm:
                    href = req.href.wiki(page.name, action='edit')
                    add_ctxtnav(req, _('Edit'), href)
        return template, data, content_type
