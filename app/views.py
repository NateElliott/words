from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from django.conf import settings

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

import urllib.request

from .models import User, Paper
from .helper import generator

import os

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

        if request.FILES.get('data-file'):
            source = request.FILES.get('data-file')
            file = source.name
            data = request.FILES['data-file'].read()

        store = generator.id_generator(size=8)

        user_path = os.path.join(settings.BASE_DIR, 'storage', request.user.username)
        if not os.path.exists(user_path):
            os.mkdir(user_path)

        mdpath = os.path.join(user_path, store)
        if not os.path.exists(mdpath):
            os.mkdir(mdpath)

        f = open(os.path.join(mdpath,file),'wb')
        f.write(data)

        Paper(name=file,
              size=len(data),
              store=store,
              status='private',
              owner=request.user,
              origin=source).save()

        f.close()

        return redirect('/')








class FileViewView(View):
    template_name = 'view.html'

    def get(self, request, store, file):

        try:
            op = Paper.objects.filter(store=store)[0]
            self.mdpath = os.path.join(settings.BASE_DIR,'storage',op.owner.username,op.store,file)
            if os.path.exists(self.mdpath):

                if op.status == 'public':
                    return render(request, self.template_name, {'data':self.openfile()})
                elif op.status == 'private' and op.owner.username == request.user.username:
                    return render(request, self.template_name, {'data': self.openfile()})

        except:
            return HttpResponse(status=404)


    def openfile(self):

        with open(self.mdpath,'rb') as f:
            fdata = f.read().decode('utf-8', 'ignore')
        f.close()

        return fdata







class FileNewView(View):
    template_name = 'new.html'

    def get(self, request):

        return render(request, self.template_name)

