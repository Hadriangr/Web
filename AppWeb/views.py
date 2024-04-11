from django.shortcuts import render
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')


def examenes_mujer(request):
    # Recuperar las recetas médicas de la categoría "Examenes"
    examenes = RecetaMedica.objects.filter(categoria='Examenes')
    
    # Crear una lista de diccionarios con los datos necesarios para cada cuadro
    cuadros = []
    for examen in examenes:
        cuadro = {
            'titulo': examen.nombre,
            'contenido': examen.descripcion,
            'ruta': f'detalle_receta/{examen.id}',  # URL para ver los detalles de la receta
        }
        cuadros.append(cuadro)
    
    return render(request, 'examenes_mujer.html', {'cuadros': cuadros})

def render_cuadro(request, titulo, contenido, template_name):
    return render(request, template_name, {'titulo': titulo, 'contenido': contenido})

def Mcuadro_1(request):
    return render_cuadro(request, 'Cuadro 1', 'Contenido del cuadro 1', 'Mcuadro_1.html')


def Mcuadro_2(request):
    return render_cuadro(request, 'Cuadro 2', 'Contenido del cuadro 2', 'Mcuadro_2.html')


def Mcuadro_3(request):
    return render_cuadro(request, 'Cuadro 3', 'Contenido del cuadro 3', 'Mcuadro_3.html')


def Mcuadro_4(request):
    return render_cuadro(request, 'Cuadro 4', 'Contenido del cuadro 4', 'Mcuadro_4.html')


def Hcuadro_1(request):
    return render_cuadro(request, 'Cuadro 1', 'Contenido del cuadro 1', 'Hcuadro_1.html')


def Hcuadro_2(request):
    return render_cuadro(request, 'Cuadro 2', 'Contenido del cuadro 2', 'Hcuadro_2.html')


def Hcuadro_3(request):
    return render_cuadro(request, 'Cuadro 3', 'Contenido del cuadro 3', 'Hcuadro_3.html')


def Hcuadro_4(request):
    return render_cuadro(request, 'Cuadro 4', 'Contenido del cuadro 4', 'Hcuadro_4.html')



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
    
    return render(request, 'login.html',{'form':form})


@login_required
def dashboard(request):
    return render(request,
                  'dashboard.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            return render(request,
                          'registro_done.html',
                          {'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request,
                      'registro.html',
                      {'user_form':user_form})