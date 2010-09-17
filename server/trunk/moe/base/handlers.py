# -*- coding: utf-8 -*-
import logging

from tipfy import (HTTPException, RequestHandler, Response, Tipfy, abort,
    get_config, import_string, url_for)
from tipfy.ext import i18n
from tipfy.ext import jinja2
from tipfy.ext import session
from tipfy.ext import auth

from moe.base.models import Area


class AreaRequestHandler(RequestHandler, session.AllSessionMixins,
    auth.AppEngineAuthMixin, jinja2.Jinja2Mixin,):
    """Base for all handlers."""

    middleware = [session.SessionMiddleware, i18n.I18nMiddleware]

    def __init__(self, app, request):
        self.app = app
        self.request = request

        # Alias.
        self.current_user = self.auth_current_user

        area_name = self.get_area_name()
        if area_name not in ('docs', 'www'):
            # TODO instead of 404, redirect to a page to create the area,
            # if the are doesn't exist.
            # For now, only 404 is allowed.
            abort(404)

        self.area = Area.get_by_key_name(area_name)
        if self.area is None:
            self.area = Area.get_or_insert(key_name=area_name, name=area_name)

        # Get sitename from config or use host minus port as default
        # sitename.
        sitename = self.request.host.rsplit(':', 1)[0]

        # Add some common stuff to context.
        self.context = self.request.context = {
            'area':           self.area,
            'current_url':    self.request.url,
            'sitename':       get_config('moe', 'sitename', sitename),
            'analytics_code': get_config('moe', 'analytics_code', None),
            'dev':            get_config('tipfy', 'dev'),
            'apps_installed': get_config('tipfy', 'apps_installed'),
        }

    def render_response(self, filename, **values):
        # System messages.
        self.request.context['messages'] = self.messages

        self.request.context.update({
            'auth_session': self.auth_session,
            'current_user': self.auth_current_user,
            'login_url':    self.auth_login_url(),
            'logout_url':   self.auth_logout_url('/'),
        })

        return super(AreaRequestHandler, self).render_response(filename,
            **values)

    def set_form_error(self, body=None, title=None):
        """Adds a form error message.

        :param body:
            Message contents.
        :param title:
            Optional message title.
        :return:
            ``None``.
        """
        if body is None:
            body = i18n._('A problem occurred. Please correct the errors '
                'listed in the form.')

        if title is None:
            title = i18n._('Error')

        self.set_message('error', body, title=title, life=None)

    def get_area_name(self):
        if self.request.rule_args:
            name = self.request.rule_args.get('area_name', 'www')
        else:
            # For when no rule is set.
            #host = request.host.split(':', 1)[0]
            #domain = get_config('tipfy', 'server_name', '').split(':', 1)[0]
            #name = host[:-len(domain) - 1]
            name = 'www'

        return name

    def head(self, **kwargs):
        """Accept HEAD requests."""
        return Response('')


class ExceptionHandler(AreaRequestHandler):
    def get(self, exception=None, handler=None):
        # Always log exceptions.
        logging.exception(exception)

        # Get the exception code and description, if it is an HTTPException,
        # or assume 500.
        code = getattr(exception, 'code', 500)
        message = getattr(exception, 'description', None)

        if self.app.dev and code not in (404,):
            # Raise the exception in dev except for NotFound.
            raise

        if code in (403, 404):
            # Render a special template for these codes.
            template = 'base/error_%d.html' % code
        else:
            # Render a generic 500 template.
            template = 'base/error_500.html'

        # Set breadcrumbs to follow rest of the site.
        self.request.context['breadcrumbs'] = [
            (url_for('home/index', area_name=self.area.name),
                i18n._('Home'))
        ]

        # Render the template using the exception message, if any, and set
        # the status code.
        response = self.render_response(template, message=message)
        response.status_code = code
        return response


class ExceptionMiddleware(object):
    def handle_exception(self, e, handler=None):
        return ExceptionHandler(Tipfy.app, Tipfy.request).dispatch('get',
            exception=e)
