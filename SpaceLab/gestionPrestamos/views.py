from django.http import HttpResponse
import datetime
from django.template import Template, Context
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

#def index(request):
#    doc_externo=open("/home/astrolabio/Django/inventario/gestionPrestamos/templates/index.html")
#    plt=Template(doc_externo.read())
#    doc_externo.close()
#    ctx=Context()
#    documento=plt.render(ctx)
#     return HttpResponse(documento)

#def index(request):
#    return render(request, 'index.html')

@login_required(login_url="index.html")
def logedin(request):
    return render(request, 'logedin.html')

def exit(request):
    logout(request)
    return redirect('index')

def custom_login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('logedin')  # Redirige a la página 'logedin'
    
    return render(request, 'login.html', {'form': form})