from django.shortcuts import render,redirect,get_object_or_404
from .forms import LoginForm, CustomUserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Examen,CustomUser
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.contrib import messages



class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')  # Redirigir al inicio de sesión después del registro
    template_name = 'registration/signup.html'







# Create your views here.
def index(request):
    return render(request, 'index.html')




def examenes_hombre(request):
    cuadros = [
        {'titulo': 'Cuadro 1', 'contenido': 'Contenido del cuadro 1', 'ruta': 'Hcuadro_1'},
        {'titulo': 'Cuadro 2', 'contenido': 'Contenido del cuadro 2', 'ruta': 'Hcuadro_2'},
        {'titulo': 'Cuadro 3', 'contenido': 'Contenido del cuadro 3', 'ruta': 'Hcuadro_3'},
        {'titulo': 'Cuadro 4', 'contenido': 'Contenido del cuadro 4', 'ruta': 'Hcuadro_4'},
    ]
    return render(request, 'examenes_hombre.html', {'cuadros': cuadros})


def user_login(request):
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username = cd['username'], 
                                password = cd['password']) #None
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Usuario autenticado')
                else:
                    return HttpResponse('El usuario no esta activo')
            else:
                return HttpResponse('La información no es correcta')
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html',{'form':form})











def user_logout(request):
    logout(request)
    return redirect('index')







def lista_examenes(request):
    examenes = Examen.objects.all()
    return render(request, 'examenes/lista_examenes.html', {'examenes': examenes})






def mostrar_subcategorias(request, examen_id):
    examen = get_object_or_404(Examen, id=examen_id)
    subcategorias = examen.subcategorias.all()
    return render(request, 'examenes/mostrar_subcategorias.html', {'examen': examen, 'subcategorias': subcategorias})









from django.core.mail import send_mail

def custom_password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Enviar correo electrónico de restablecimiento de contraseña
            send_mail(
                'Solicitud de restablecimiento de contraseña',
                'Por favor sigue este enlace para restablecer tu contraseña.',
                'your_email@gmail.com',  # Reemplaza con tu dirección de correo electrónico
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña.')
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, 'registration/password_reset_form.html', {'form': form})







def custom_password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')

def custom_password_reset_confirm(request):
    return render(request, 'registration/password_reset_confirm.html')

def custom_password_reset_complete(request):
    return render(request, 'registration/password_reset_complete.html')
