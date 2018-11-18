from django.views.generic import TemplateView


class Index(TemplateView):
    '''Welcome page.'''
    template_name = 'frontend/index.html'
