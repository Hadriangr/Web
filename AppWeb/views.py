from django.shortcuts import render,redirect,get_object_or_404
from .forms import LoginForm, CustomUserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import Examen

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
    
    return render(request, 'registration/login.html',{'form':form})


@login_required
def dashboard(request):
    return render(request,
                  'registration/dashboard.html')



def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            return redirect('registro_done')
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'registro.html', {'user_form': user_form})





def user_logout(request):
    logout(request)
    return redirect('index')




def registro_done(request):
    return render(request, 'registro_done.html')





def lista_examenes(request):
    examenes = Examen.objects.all()
    return render(request, 'examenes/lista_examenes.html', {'examenes': examenes})






def mostrar_subcategorias(request, examen_id):
    examen = get_object_or_404(Examen, id=examen_id)
    subcategorias = examen.subcategorias.all()
    return render(request, 'examenes/mostrar_subcategorias.html', {'examen': examen, 'subcategorias': subcategorias})
