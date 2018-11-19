'''Generate activation tokens for registered users.'''
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    '''Activation token creator.'''

    def _make_hash_value(self, user, timestamp):
        '''Make base 64 hash.'''
        return (six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.profile.email_confirmed))


TOKEN_GENERATOR = AccountActivationTokenGenerator()
