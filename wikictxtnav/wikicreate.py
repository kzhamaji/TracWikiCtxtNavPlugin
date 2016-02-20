# encoding: utf-8
# Created by Noah Kantrowitz
# Copyright (c) 2008 Noah Kantrowitz. All rights reserved.
import urllib

from trac.core import *
from trac.web.main import IRequestHandler
from trac.web.chrome import ITemplateProvider, add_ctxtnav
from trac.web.api import IRequestFilter
from genshi.core import Markup

from trac.wiki import WikiSystem

class WikiCreateModule(Component):
    """An evil module that adds a rename button to the wiki UI."""
 
    implements(IRequestHandler, ITemplateProvider, IRequestFilter)
    
    PAGE_TEMPLATES_PREFIX = 'PageTemplates/'
    DEFAULT_PAGE_TEMPLATE = 'DefaultPage'
    
    # IRequestHandler methods
    def match_request (self, req):
        return req.path_info == '/wikicreate'

    def process_request (self, req):
        req.perm.require('WIKI_CREATE')

        if req.method == 'POST':
            new_page = urllib.unquote_plus(req.args.get('new_page',''))
            template = req.args.get('template', '')
        
            if not new_page:
                raise TracError, "Please provide a new page name"

            # check existence
            if WikiSystem(self.env).has_page(new_page):
                raise TracError, "Page exists"

            # redirect
            req.redirect(req.href.wiki(new_page, action='edit', template=template))

        # add templates
        prefix = self.PAGE_TEMPLATES_PREFIX
        templates = [template[len(prefix):] for template in
                     WikiSystem(self.env).get_pages(prefix) if
                     'WIKI_VIEW' in req.perm('wiki', template)]
        data = {
            'templates': templates,
            'default_template': self.DEFAULT_PAGE_TEMPLATE, 
            }
        return 'wikicreate.html', data, None


    # ITemplateProvider methods
    def get_templates_dirs(self):
        from pkg_resources import resource_filename
        return [resource_filename(__name__,'templates')]

    def get_htdocs_dirs(self):
        return []

    # IRequestFilter methods
    def pre_process_request(self, req, handler):
        return handler

    def post_process_request(self, req, template, data, content_type):
        if (req.path_info.startswith('/wiki') or req.path_info == '/') and \
                data and 'page' in data:
            page = data['page']
            perm = req.perm(page.resource)
            if 'WIKI_CREATE' in perm or 'WIKI_ADMIN' in perm:
                href = req.href('wikicreate') 
                add_ctxtnav(req, 'Create', href)
        return template, data, content_type
