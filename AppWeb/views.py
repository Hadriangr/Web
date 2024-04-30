from django.shortcuts import render,redirect,get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse,Http404
from .models import CustomUser,Paquete,ElementoCarrito
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import PasswordResetForm,AuthenticationForm
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Sum




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
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Aquí utilizamos el campo de email en lugar del campo de username
            username_or_email = cd.get('username')  # Aquí mantenemos 'username' para la compatibilidad
            password = cd['password']
            user = authenticate(request, username=username_or_email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Usuario autenticado')
                else:
                    return HttpResponse('El usuario no está activo')
            else:
                return HttpResponse('La información de inicio de sesión no es correcta')
    else:
        form = AuthenticationForm(request)
    
    return render(request, 'registration/login.html', {'form': form})



def user_logout(request):
    logout(request)
    return redirect('index')



def lista_examenes(request):
    examenes = Paquete.objects.all()
    return render(request, 'examenes/lista_examenes.html', {'examenes': examenes})



# def mostrar_subcategorias(request, examen_id):
#     examen = get_object_or_404(PaqueteExamen, id=examen_id)
#     subcategorias = SubcategoriaExamen.objects.filter(examen=examen)

#     # Calcular la reseña general excluyendo los mensajes predeterminados
#     reseña_general = set()  # Utilizar un conjunto para asegurar la unicidad de los mensajes
#     for subcategoria in subcategorias:
#         if subcategoria.mensaje_para_reseña != 'Mensaje predeterminado':
#             reseña_general.add(subcategoria.mensaje_para_reseña)

#     return render(request, 'examenes/mostrar_subcategorias.html', {
#         'examen': examen,
#         'subcategorias': subcategorias,
#         'reseña_general': '\n'.join(reseña_general),  # Convertir el conjunto en una cadena separada por saltos de línea
#     })




#Cambio de clave y envío de correo




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



# # Carrito de compras 

# def agregar_al_carrito(request):
#     if request.method == 'POST':
#         subcategorias_ids = request.POST.getlist('subcategorias')
#         subcategorias = SubcategoriaExamen.objects.filter(id__in=subcategorias_ids)
#         for subcategoria in subcategorias:
#             # Agregar la subcategoría al carrito
#             request.session['carrito'].append(subcategoria.id)
#         # Redirigir a la página del carrito
#         return redirect('ver_carrito')
#     else:
#         # Si la solicitud no es POST, lanzar un error 404
#         raise Http404("Método de solicitud no permitido")




# def ver_carrito(request):
#     carrito = request.session.get('carrito', [])
#     subcategorias_carrito = SubcategoriaExamen.objects.filter(id__in=carrito)
    
#     # Calcular el monto total sumando los precios de los exámenes en el carrito
#     monto_total = subcategorias_carrito.aggregate(total=Sum('examen__precio'))['total'] or 0
    
#     return render(request, 'examenes/ver_carrito.html', {'subcategorias_carrito': subcategorias_carrito, 'monto_total': monto_total})





# def eliminar_del_carrito(request, subcategoria_id):
#     carrito = request.session.get('carrito', [])
#     try:
#         carrito.remove(subcategoria_id)
#         request.session['carrito'] = carrito
#     except ValueError:
#         pass  # Manejar el caso cuando el producto no está en el carrito
#     return redirect('ver_carrito')


def mostrar_paquetes(request):
    paquetes = Paquete.objects.all()
    return render(request, 'examenes/mostrar_paquetes.html', {'paquetes': paquetes})

def agregar_al_carrito(request, paquete_id):
    paquete = Paquete.objects.get(pk=paquete_id)
    if request.method == 'POST':
        cantidad = int(request.POST['cantidad'])
        elemento, creado = ElementoCarrito.objects.get_or_create(paquete=paquete)
        elemento.cantidad += cantidad
        elemento.save()
    return redirect('ver_carrito')

def quitar_del_carrito(request, elemento_id):
    elemento = ElementoCarrito.objects.get(pk=elemento_id)
    elemento.delete()
    return redirect('ver_carrito')

def ver_carrito(request):
    elementos_carrito = ElementoCarrito.objects.all()
    total = sum(elemento.paquete.costo_fijo * elemento.cantidad for elemento in elementos_carrito)
    return render(request, 'examenes/ver_carrito.html', {'elementos_carrito': elementos_carrito, 'total': total})