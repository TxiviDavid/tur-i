from django.shortcuts import render
from django.views.generic import View


class IntroView(View):
    def get(self, request):
        context = {}
        return render(request, 'intro/index.html', context)
