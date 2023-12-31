from django.shortcuts import render
from django.views.generic.base import TemplateView
# Create your views here.


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = 'صفحه اصلی'
        return context


def site_header_component(request):
    context = {
        'link': 'آموزش جنگو'
    }
    return render(request, 'shared/site_header_component.html', context)


def site_footer_component(request):
    return render(request, 'shared/site_footer_component.html', {})