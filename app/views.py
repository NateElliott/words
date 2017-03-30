from django.views import View
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings

from .models import User, Files
from .helper import generator, filehandler

import os, string, json


class LoginView(View):
    template_name = 'core/login.html'

    def get(self, request):
        return render(request,self.template_name)

    def post(self, request):

        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])

        if user and user.is_active:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class IndexView(View):
    template_name = 'index.html'

    @method_decorator(login_required)
    def get(self, request):

        return render(request, self.template_name,{'data':'hello world'})


class FileNewView(View):
    template_name = 'editor.html'
    def get(self, request):
        default_file = os.path.join(settings.BASE_DIR,'storage','default.md')
        return render(request, self.template_name,{'filedata':filehandler.getfile(default_file)})

    def post(self, request):

        name = request.POST.get('filename')
        code = request.POST.get('code')
        store = generator.id_generator(size=16)

        return HttpResponse('<b>{}-{}</b><br><pre><code>{}</code></pre>'.format(name,store,code))
