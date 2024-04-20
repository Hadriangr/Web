from django.shortcuts import render,redirect,get_object_or_404
from .forms import LoginForm, CustomUserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Examen,CustomUser
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView




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


@login_required
def dashboard(request):
    return render(request,
                  'registration/dashboard.html')








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









# PasswordResetView: Vista para solicitar el restablecimiento de contraseña
class password_reset(PasswordResetView):
    template_name = 'registration/password_reset_form.html'  # Plantilla para el formulario de restablecimiento de contraseña
    email_template_name = 'registration/password_reset_email.html'  # Plantilla para el correo electrónico de restablecimiento de contraseña
    success_url = reverse_lazy('password_reset_done')  # URL a la que se redirige después de enviar el correo electrónico de restablecimiento de contraseña

# PasswordResetDoneView: Vista para la confirmación del envío del correo electrónico de restablecimiento de contraseña
class password_reset_done(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'  # Plantilla para la confirmación del envío del correo electrónico

# PasswordResetConfirmView: Vista para confirmar el restablecimiento de contraseña mediante el enlace enviado por correo electrónico
class password_reset_confirm(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'  # Plantilla para el formulario de confirmación de restablecimiento de contraseña
    success_url = reverse_lazy('password_reset_complete')  # URL a la que se redirige después de restablecer la contraseña con éxito

# PasswordResetCompleteView: Vista para confirmar que la contraseña se ha restablecido correctamente
class password_reset_completed(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'  # Plantilla para la confirmación del restablecimiento de contraseña

