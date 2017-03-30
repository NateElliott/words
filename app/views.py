from django.views import View
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Files
from .helper import generator, filehandler

import os, string, hashlib


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



class FileSaveView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(FileSaveView, self).dispatch(request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request):

        wdata = request.POST.get('code')
        wfile = request.POST.get('filename')
        whash = hashlib.sha1(wdata.encode('utf-8')).hexdigest()[:6]

        try:
            file = Files.objects.get(name=wfile)
            if whash != file.chash:
                file.content = wdata
                file.chash = whash
                file.save()

        except:
            file = Files(name=wfile,
                         store=generator.id_generator(8),
                         content=wdata,
                         chash=whash,
                         owner=request.user,
                         public=False)
            file.save()


        response_text = {}
        response_text["hash"] = file.chash
        response_text["store"] = file.store
        response_text["dtg"] = file.updated

        return JsonResponse(response_text)











