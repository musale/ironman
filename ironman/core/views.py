'''Core views.'''
import logging
from django.views.generic import FormView, TemplateView
from django.views import View
from django.core import mail
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.conf import settings
from ironman.core import forms
from ironman.core.tokens import TOKEN_GENERATOR

LOG = logging.getLogger(__name__)


class ThankYou(TemplateView):
    '''Thank you page.'''
    template_name = 'frontend/thank_you.html'


class UserSignup(FormView):
    '''Create a new normal user.'''
    form_class = forms.UserSignup
    template_name = 'registration/signup.html'

    def get_success_url(self):
        '''URL to redirect to after a successful sign up.'''
        return reverse('thank_you')

    def form_valid(self, form):
        """If the form is valid, send email & redirect to the supplied URL."""
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        subject = 'Confirm your email address to learn with us'

        body = render_to_string('registration/acc_activate_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'),
            'token': TOKEN_GENERATOR.make_token(user),
        })

        message = (
            "Your data has been saved! Check your email for a "
            "confirmation email and be able to login.")
        messages.success(self.request, message)

        from_email = settings.DEFAULT_FROM_EMAIL
        mailer = mail.EmailMessage(
            subject=subject, body=body, from_email=from_email, to=[user.email])
        mailer.send()
        LOG.debug(body)

        return HttpResponseRedirect(self.get_success_url())


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


class ActivateAccountView(View):
    '''Activate a registered user.'''

    def get(self, request, uidb64, token):
        '''Handle GET requests.'''
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and TOKEN_GENERATOR.check_token(user, token):
            user.profile.email_confirmed = True
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('user_dashboard')
        return render(request, 'registration/acc_token_invalid.html')
