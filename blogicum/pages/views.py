from django.shortcuts import render


def about(request):
    return render(
        request,
        'pages/about.html',
        context={'title': 'О проекте'},
    )


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


def rules(request):
    return render(
        request,
        'pages/rules.html',
        context={'title': 'Наши правила'},
    )
