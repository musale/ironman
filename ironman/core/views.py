'''Core views.'''
from django.views.generic import FormView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from ironman.core import forms


class UserSignup(FormView):
    '''Create a new normal user.'''
    form_class = forms.UserSignup
    template_name = 'registration/signup.html'

    def get_success_url(self):
        '''URL to redirect to after a successful sign up.'''
        return reverse('user_dashboard')


@method_decorator(login_required, name='dispatch')
class UserDashboard(TemplateView):
    '''Logged in user dashboard.'''
    template_name = 'frontend/dashboard.html'


class Index(TemplateView):
    '''Welcome page.'''
    template_name = 'frontend/index.html'

    def get_template_names(self):
        '''Get the dashboard html if logged in, index if not.'''
        template_name = super(Index, self).get_template_names()
        if self.request.user.is_authenticated:
            template_name = ['frontend/dashboard.html']
        return template_name
