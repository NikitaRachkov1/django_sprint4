from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = 'pages/about.html'
    extra_context = {'title': 'О проекте'}


class RulesView(TemplateView):
    template_name = 'pages/rules.html'
    extra_context = {'title': 'Наши правила'}


def forbidden(request, exception):
    return render(
        request,
        'pages/403csrf.html',
        status=403,
    )


def internal_server_error(request):
    return render(
        request,
        'pages/500.html',
        status=500,
    )


def page_not_found(request, exception):
    return render(
        request,
        'pages/404.html',
        status=404,
    )
