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


        return render(request, self.template_name)


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
        wloc = request.POST.get('loc')
        whash = hashlib.sha1(wdata.encode('utf-8')).hexdigest()[:6]

        try:
            file = Files.objects.get(name=wfile)
            if whash != file.chash:
                file.content = wdata
                file.chash = whash
                file.loc = wloc
                file.save()

        except:
            file = Files(name=wfile,
                         store=generator.id_generator(8),
                         content=wdata,
                         chash=whash,
                         loc = wloc,
                         owner=request.user,
                         public=False)
            file.save()


        response_text = {}
        response_text["hash"] = file.chash
        response_text["store"] = file.store
        response_text["loc"] = file.loc
        response_text["dtg"] = file.updated

        return JsonResponse(response_text)



class FileEditView(View):

    template_name = 'editor.html'
    def get(self, request, *args, **kwargs):
        store = self.kwargs['store']

        file = Files.objects.filter(store=store)[0]

        return render(request, self.template_name, {'file':file})



class ListAllView(View):

    def get(self, request):

        user_files = Files.objects.filter(owner=request.user).order_by('-updated')
        fop = []

        for f in user_files:
            fop.append({
                "pid":f.store,
                "data":{
                    "name":f.name,
                    "hash":f.chash,
                    "created": f.created,
                    "updated":f.updated,
                    "public": f.public
                }
            })

        return JsonResponse(fop, safe=False)