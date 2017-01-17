from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from django.conf import settings

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

import urllib.request

from .models import User, Paper
from .helper import generator, filehandler

import os, string

from django.conf import settings



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

        list = Paper.objects.all().order_by('-datetime')
        return render(request, self.template_name,{'data':list})









class AddUrlView(View):

    def post(self, request):

        if request.POST.get('data-url'):
            source = request.POST.get('data-url')
            file = source.split('/')[-1]
            data = urllib.request.urlopen(request.POST['data-url']).read()

        elif request.FILES.get('data-file'):
            source = request.FILES.get('data-file')
            file = source.name
            data = request.FILES['data-file'].read()

        elif request.POST.get('body'):
            source = request.user.username

            if request.POST.get('title'):
                file = request.POST.get('title')
            else:
                file = '{}.md'.format(generator.id_generator(size=8))

            data = request.POST.get('body').encode('utf-8', 'ignore')



        store = generator.id_generator(size=8)

        user_path = os.path.join(settings.BASE_DIR, 'storage', request.user.username)
        if not os.path.exists(user_path):
            os.mkdir(user_path)

        mdpath = os.path.join(user_path, store)
        if not os.path.exists(mdpath):
            os.mkdir(mdpath)

        f = open(os.path.join(mdpath, file), 'wb')
        f.write(data)

        Paper(name=file,
              size=len(data),
              store=store,
              is_public=False,
              owner=request.user,
              origin=source).save()

        f.close()

        return redirect('/')








class FileViewView(View):
    template_name = 'view.html'
    def get(self, request, store, file):
        try:
            op = Paper.objects.filter(store=store)[0]
            mdpath = os.path.join(settings.BASE_DIR,'storage',op.owner.username,op.store,file)
            if os.path.exists(mdpath):
                if op.is_public or op.owner.username == request.user.username:
                    return render(request, self.template_name, {'data':filehandler.getfile(mdpath)})

        except:
            return HttpResponse(status=404)








class FileNewView(View):
    template_name = 'editor.html'
    def get(self, request):
        default_file = os.path.join(settings.BASE_DIR,'storage','default.md')
        return render(request, self.template_name,{'filedata':filehandler.getfile(default_file)})


    def post(self, request):
        return HttpResponse('<pre>{}</pre>'.format(request.POST.get('code')))



class FileEditView(View):
    template_name = 'new.html'
    def get(self, request, store, file):
        try:
            op = Paper.objects.filter(store=store)[0]
            mdpath = os.path.join(settings.BASE_DIR,'storage',op.owner.username,op.store,file)
            if os.path.exists(mdpath):
                if op.is_public or op.owner.username == request.user.username:
                    return render(request, self.template_name, {'filedata':filehandler.getfile(mdpath),
                                                                'file_obj':op})
        except:
            return HttpResponse(status=404)