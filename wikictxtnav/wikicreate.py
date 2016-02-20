# encoding: utf-8
# Created by Noah Kantrowitz
# Copyright (c) 2008 Noah Kantrowitz. All rights reserved.
import urllib

from trac.core import *
from trac.web.main import IRequestHandler
from trac.web.chrome import ITemplateProvider, add_ctxtnav
from trac.web.api import IRequestFilter
from genshi.core import Markup

from trac.wiki import WikiSystem, validate_page_name

from trac.util.translation import _, add_domain

class WikiCreateModule(Component):

    implements(IRequestHandler, ITemplateProvider, IRequestFilter)

    PAGE_TEMPLATES_PREFIX = 'PageTemplates/'
    DEFAULT_PAGE_TEMPLATE = 'DefaultPage'

    def __init__ (self):
        import pkg_resources
        try:
            locale_dir = pkg_resources.resource_filename(__name__, 'locale')
        except KeyError:
            pass
        else:
            add_domain('wikictxtnav', self.env.path, locale_dir)

    # IRequestHandler methods
    def match_request (self, req):
        return req.path_info == '/wikicreate'

    def process_request (self, req):
        req.perm.require('WIKI_CREATE')

        if req.method == 'POST':
            pagename = urllib.unquote_plus(req.args.get('new_page',''))
            template = req.args.get('template', '')

            if not validate_page_name(pagename):
                raise TracError(_("Invalid Wiki page name '%(name)s'",
                                name=pagename))

            # check existence
            if WikiSystem(self.env).has_page(pagename):
                raise TracError, _("The page %(name)s already exists.", name=pagename)

            # redirect
            req.redirect(req.href.wiki(pagename, action='edit', template=template))

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
                add_ctxtnav(req, _('Create'), href)
        return template, data, content_type
