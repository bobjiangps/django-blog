from django.shortcuts import render


def tool_main_page(request):
    return render(request, 'tool/main.html')
