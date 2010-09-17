from google.appengine.api import users

from tipfy import RequestHandler, cached_property, redirect
from tipfy.ext.i18n import _, lazy_gettext

from tipfy.ext.auth import login_required

from tipfy.ext.wtforms import Form, fields, validators

from moe.base.handlers import AreaRequestHandler


class SignupForm(Form):
    """Base signup form."""
    nickname = fields.TextField(lazy_gettext('Nickname'))


class SignupHandler(AreaRequestHandler):
    @login_required
    def get(self, **kwargs):
        redirect_url = self.redirect_path()

        if self.auth_current_user:
            # User is already registered, so don't display the signup form.
            return redirect(redirect_url)

        return self.render_response('users/signup.html', form=self.form)

    @login_required
    def post(self, **kwargs):
        redirect_url = self.redirect_path()

        if self.auth_current_user:
            # User is already registered, so don't process the signup form.
            return redirect(redirect_url)

        if self.form.validate():
            auth_id = 'gae|%s' % self.auth_session.user_id()
            user = self.auth_create_user(self.form.nickname.data, auth_id,
                email=self.auth_session.email())
            if user:
                self.set_message('success', 'You are now registered. '
                    'Welcome!', flash=True, life=5)
                return redirect(redirect_url)
            else:
                self.set_message('error', 'This nickname is already '
                    'registered.', life=None)
                return self.get(**kwargs)

        self.set_message('error', 'A problem occurred. Please correct the '
            'errors listed in the form.', life=None)
        return self.get(**kwargs)

    @cached_property
    def form(self):
        return SignupForm(self.request)

    def redirect_path(self, default='/'):
        url = self.request.args.get('continue', '/')

        if not url.startswith('/'):
            url = default

        return url
