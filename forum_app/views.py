from django.shortcuts import render


# Create your views here.

def OpenMainWeb(request):
    return render(request, 'forum_app/main.html')
