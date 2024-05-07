from django.shortcuts import render,redirect,get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse,Http404
from .models import CustomUser,Producto,Categoria,Derivacion,Diagnostico
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import PasswordResetForm,AuthenticationForm
from django.core.mail import send_mail
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas



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


class CarritoForm(forms.Form):
    productos = forms.ModelMultipleChoiceField(queryset=Producto.objects.all(), widget=forms.CheckboxSelectMultiple)
    
    PRECIO_FIJO_PRODUCTO = 2990

    def precio_total(self):
        
        cantidad_productos = len(self.cleaned_data['productos'])
        return self.PRECIO_FIJO_PRODUCTO * cantidad_productos


def carrito(request):
    productos = Producto.objects.all()  # Obtener todos los productos disponibles
    if request.method == 'POST':
        # Agregar producto al carrito
        producto_id = request.POST.get('producto_id')
        producto = Producto.objects.get(id=producto_id)
        # Podrías realizar validaciones adicionales aquí antes de agregar al carrito
        request.session.setdefault('carrito', []).append(producto.id)
        request.session.modified = True
        return redirect('carrito')  # Redirigir nuevamente a la página del carrito después de agregar
    else:
        form = CarritoForm()
    return render(request, 'examenes/carrito_test.html', {'productos': productos, 'form': form})


def calcular_precio_total_categorias(categorias_seleccionadas):
    precio_total = 0
    
    # Iterar sobre todas las categorías seleccionadas
    for categoria in categorias_seleccionadas:
        # Sumar el precio de cada categoría
        precio_total += categoria.precio
    
    return precio_total



def ver_carrito(request):
    carrito = request.session.get('carrito', [])
    print("IDs de productos en el carrito:", carrito)  # Imprimir los IDs de los productos
    ids_productos_validos = [id for id in carrito if isinstance(id, int)]
    productos_en_carrito = Producto.objects.filter(id__in=ids_productos_validos)
    nombres_productos = [producto.nombre for producto in productos_en_carrito]
    categorias_seleccionadas = set(producto.categoria for producto in productos_en_carrito)
    precio_total = calcular_precio_total_categorias(categorias_seleccionadas)
    return render(request, 'examenes/resumen_carritotest.html', {'categoria': Categoria, 'nombres_productos': nombres_productos, 'precio_total': precio_total})



def agregar_al_carrito(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        producto = get_object_or_404(Producto, id=producto_id)  # Verificar si el producto existe
        if 'carrito' not in request.session:
            request.session['carrito'] = []
        if producto.id not in request.session['carrito']:  # Evitar duplicados en el carrito
            request.session['carrito'].append(producto.id)
            request.session.modified = True
    return redirect('carrito') 


def eliminar_del_carrito(request, producto_id):
    # Obtener el carrito de compras del usuario desde la sesión
    carrito = request.session.get('carrito', [])
    
    # Verificar si el producto está en el carrito
    if producto_id in carrito:
        # Eliminar el producto del carrito
        carrito.remove(producto_id)
        
        # Actualizar el carrito en la sesión
        request.session['carrito'] = carrito

    return redirect('ver_carrito')

def pago_exitoso(request):
    # Obtener nombre de usuario de la sesión
    nombre_usuario = request.user.username if request.user.is_authenticated else "Usuario Anónimo"

    # Obtener productos seleccionados de la sesión
    productos_ids = request.session.get('carrito', [])
    productos_agregados = Producto.objects.filter(id__in=productos_ids)


    # Generar PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="pago_exitoso.pdf"'
    p = canvas.Canvas(response)
    p.drawString(100, 800, "Paciente " + nombre_usuario)
    p.drawString(100, 780,  productos_agregados[0].categoria.nombre + ": ")  # Accede al nombre de la categoría del primer producto
    y = 740
    for producto in productos_agregados:
        p.drawString(120, y, producto.nombre)
        y -= 20
    p.save()
    return response


def ver_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'examenes/ver_categoria.html', {'categorias': categorias})

def ver_productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)
    return render(request, 'examenes/ver_productos_por_categoria.html', {'categoria': categoria, 'productos': productos})



def ver_derivaciones(request):
    derivaciones = Derivacion.objects.all()
    return render(request, 'derivaciones/derivaciones.html', {'derivaciones': derivaciones})


def ver_diagnosticos(request):
    diagnosticos = Diagnostico.objects.all()  # Recupera todos los diagnósticos de la base de datos
    return render(request, 'derivaciones/diagnostico.html', {'diagnosticos': diagnosticos})