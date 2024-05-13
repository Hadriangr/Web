from django.shortcuts import render,redirect,get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from .models import CustomUser,Categoria,Derivacion,Item,Carrito,ItemCarrito
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import PasswordResetForm,AuthenticationForm
from django.core.mail import send_mail
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from django.template.loader import get_template



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
            username_or_email = cd.get('username')  # Este campo aún se llama 'username' en tu formulario de inicio de sesión
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
    productos = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), widget=forms.CheckboxSelectMultiple)
    
    PRECIO_FIJO_PRODUCTO = 2990

    def precio_total(self):
        
        cantidad_productos = len(self.cleaned_data['productos'])
        return self.PRECIO_FIJO_PRODUCTO * cantidad_productos


def carrito(request):
    # Obtener todos los elementos en el carrito del usuario
    if request.user.is_authenticated:
        carrito_usuario, _ = Carrito.objects.get_or_create(usuario=request.user)
        elementos_en_carrito = ItemCarrito.objects.filter(carrito=carrito_usuario)
    else:
        # Manejo de usuarios anónimos, si es necesario
        elementos_en_carrito = []

    return render(request, 'examenes/carrito_test.html', {'elementos_en_carrito': elementos_en_carrito})


def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.username = user_form.cleaned_data.get('email')  # Usar el correo electrónico como nombre de usuario
            user.save()
            messages.success(request, '¡Registro exitoso! Por favor, inicia sesión con tu nueva cuenta.')  # Mensaje de éxito
            return redirect('login')  # Redireccionar al usuario a la página de inicio de sesión
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'registration/registro.html', {'user_form': user_form})

def calcular_precio_total_categorias(categorias_seleccionadas):
    precio_total = 0
    
    # Iterar sobre todas las categorías seleccionadas
    for categoria in categorias_seleccionadas:
        # Sumar el precio de cada categoría
        precio_total += categoria.precio
    
    return precio_total




def calcular_precio_total(derivaciones_seleccionadas):
    precio_total = 0
    
    # Sumar el precio de todas las derivaciones seleccionadas
    for derivacion in derivaciones_seleccionadas:
        precio_total += derivacion.precio
    
    return precio_total

from django.db.models import Sum

def resumen_carrito(request):
    # Obtener todos los items en el carrito del usuario actual 
    items_carrito = Item.objects.filter(itemcarrito__carrito__usuario=request.user) 
    
    # Obtener todas las categorías únicas en el carrito
    categorias = Categoria.objects.filter(item__in=items_carrito).distinct()
    
    # Crear un diccionario para almacenar los items agrupados por categoría
    items_por_categoria = {}
    precio_total_categorias = 0
    
    # Iterar sobre cada categoría y obtener los items asociados
    for categoria in categorias:
        items_categoria = items_carrito.filter(categoria=categoria)
        items_por_categoria[categoria] = items_categoria
        precio_total_categorias += items_categoria.aggregate(Sum('categoria__precio'))['categoria__precio__sum'] or 0
    
    # Obtener todas las derivaciones únicas en el carrito
    derivaciones = Derivacion.objects.filter(item__in=items_carrito).distinct()
    
    # Crear un conjunto para mantener un registro de las derivaciones procesadas
    derivaciones_procesadas = set()
    precio_total_derivaciones = 0
    
    # Crear un diccionario para almacenar los ítems agrupados por derivación
    items_por_derivacion = {}
    
    # Iterar sobre cada derivación y obtener el precio de cada una
    for derivacion in derivaciones:
        # Verificar si ya se ha procesado esta derivación
        if derivacion in derivaciones_procesadas:
            continue
        
        # Obtener los ítems asociados a esta derivación
        items_derivacion = items_carrito.filter(derivacion=derivacion)
        
        # Agregar los ítems de la derivación al diccionario
        items_por_derivacion[derivacion] = items_derivacion
        
        # Calcular el precio total de la derivación (solo una vez)
        precio_total_derivacion = derivacion.precio
        
        # Agregar el precio total de la derivación al precio total general
        precio_total_derivaciones += precio_total_derivacion
        
        # Agregar la derivación al conjunto de derivaciones procesadas
        derivaciones_procesadas.add(derivacion)
    
    # Calcular el precio total del carrito
    precio_total = precio_total_categorias + precio_total_derivaciones
    
    return render(request, 'examenes/resumen_carritotest.html', {
        'items_por_categoria': items_por_categoria,
        'items_por_derivacion': items_por_derivacion,
        'precio_total_categorias': precio_total_categorias,
        'precio_total_derivaciones': precio_total_derivaciones,
        'precio_total': precio_total,
    })






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




# Cuenta y editarla 

@login_required
def mi_cuenta(request):
    usuario = request.user
    #compras = Compra.objects.filter(usuario=usuario)
    return render(request, 'cuenta/mi_cuenta.html', {'usuario': usuario})


@login_required
def editar_perfil(request):
    usuario = request.user
    if request.method == 'POST':
        usuario.direccion = request.POST.get('direccion')
        usuario.comuna = request.POST.get('comuna')
        usuario.region = request.POST.get('region')
        usuario.telefono_contacto = request.POST.get('telefono')
        usuario.email = request.POST.get('correo')
        usuario.save()
        return redirect('mi_cuenta')
    return render(request, 'cuenta/editar_perfil.html', {'usuario': usuario})


def agregar_al_carrito(request):
    if request.method == 'POST':
        elemento_id = request.POST.get('elemento_id')
        tipo = request.POST.get('tipo')
        
        # Obtener el elemento (Producto o Diagnostico) según el tipo y el ID
        elemento = get_object_or_404(Item, id=elemento_id)
        
        # Obtener el carrito del usuario o crear uno nuevo si no existe
        if request.user.is_authenticated:
            carrito_usuario, _ = Carrito.objects.get_or_create(usuario=request.user)
        else:
            # Manejo de usuarios anónimos, si es necesario
            pass

        # Verificar si el elemento ya está en el carrito del usuario
        if not ItemCarrito.objects.filter(carrito=carrito_usuario, item=elemento).exists():
            # Agregar el elemento al carrito del usuario
            ItemCarrito.objects.create(carrito=carrito_usuario, item=elemento)
            request.session.modified = True
    
    return redirect('resumen_carrito')



def eliminar_producto(request, item_id):
    # Obtener el item del carrito
    item_carrito = get_object_or_404(ItemCarrito, item_id=item_id, carrito__usuario=request.user)

    # Eliminar el item del carrito
    item_carrito.delete()

    # Mostrar un mensaje de éxito
    messages.success(request, "El item se ha eliminado correctamente del carrito.")

    # Redireccionar a la página del resumen del carrito
    return redirect('resumen_carrito')


def eliminar_derivacion(request, item_id):
    # Obtener la derivacion del carrito
    derivacion_carrito = get_object_or_404(ItemCarrito, item_id=item_id, carrito__usuario=request.user)

    # Eliminar la derivacion del carrito
    derivacion_carrito.delete()

    # Mostrar un mensaje de éxito
    messages.success(request, "La derivacion se ha eliminado correctamente del carrito.")

    # Redireccionar a la página del resumen del carrito
    return redirect('resumen_carrito')



@login_required
def generar_pdf_productos(request):
    carrito_usuario = request.user.carrito_set.first()
    
    if carrito_usuario:
        # Organizar los productos por categoría
        categorias = Categoria.objects.all()
        productos_por_categoria = {}
        for categoria in categorias:
            productos_por_categoria[categoria] = ItemCarrito.objects.filter(item__categoria=categoria, carrito=carrito_usuario)
        
        # Generar PDF con los productos organizados por categoría
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="productos.pdf"'
        p = canvas.Canvas(response)
        y = 800

        if carrito_usuario:
            nombre = carrito_usuario.usuario.nombre
            apellido = carrito_usuario.usuario.apellido
            rut = carrito_usuario.usuario.rut  # Asumiendo que el rut está almacenado en el campo username

        # Agregar información del usuario al PDF
        p.drawString(100, y, f'Nombre: {nombre}')
        y -= 20
        p.drawString(100, y, f'Apellido: {apellido}')
        y -= 20
        p.drawString(100, y, f'RUT: {rut}')
        y -= 20

        for categoria, items in productos_por_categoria.items():
            if items:
                p.drawString(100, y, f' {categoria.nombre}')
                y -= 20
                for item_carrito in items:
                    p.drawString(120, y, item_carrito.item.nombre)  
                    y -= 20
        p.save()
        return response

    else:
        return HttpResponse("No se encontró el carrito del usuario")



@login_required
def generar_pdf_derivaciones(request):
    carrito_usuario = request.user.carrito_set.first()
    
    if carrito_usuario:
        # Organizar las derivaciones por categoría
        derivaciones = Derivacion.objects.all()
        derivaciones_por_categoria = {}
        for derivacion in derivaciones:
            derivaciones_por_categoria[derivacion] = ItemCarrito.objects.filter(item__derivacion=derivacion, carrito=carrito_usuario)
        
        # Generar PDF con las derivaciones organizadas por categoría
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="derivaciones.pdf"'
        p = canvas.Canvas(response)
        y = 800

        if carrito_usuario:
            nombre = carrito_usuario.usuario.nombre
            apellido = carrito_usuario.usuario.apellido
            rut = carrito_usuario.usuario.rut  # Asumiendo que el rut está almacenado en el campo username

        # Agregar información del usuario al PDF
        p.drawString(100, y, f'Nombre: {nombre}')
        y -= 20
        p.drawString(100, y, f'Apellido: {apellido}')
        y -= 20
        p.drawString(100, y, f'RUT: {rut}')
        y -= 20
        for derivacion, items in derivaciones_por_categoria.items():
            if items:
                p.drawString(100, y, f'Derivación: {derivacion.nombre}')
                y -= 20
                for item_carrito in items:
                    p.drawString(120, y, item_carrito.item.nombre)  
                    y -= 20
        p.save()
        return response

    else:
        return HttpResponse("No se encontró el carrito del usuario")



@login_required
def pago_exitoso(request):
    return render(request, 'examenes/pago_exitoso.html')





def ver_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'examenes/ver_categoria.html', {'categorias': categorias})

def ver_productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Item.objects.filter(categoria=categoria)
    return render(request, 'examenes/ver_productos_por_categoria.html', {'categoria': categoria, 'productos': productos})



def ver_derivaciones(request):
    derivaciones = Derivacion.objects.all()
    return render(request, 'derivaciones/derivaciones.html', {'derivaciones': derivaciones})


def ver_diagnosticos(request, derivacion_id):
    derivacion = get_object_or_404(Derivacion, id=derivacion_id)
    diagnosticos = Item.objects.filter(derivacion=derivacion)
    return render(request, 'derivaciones/diagnostico.html', {'derivacion': derivacion, 'diagnosticos': diagnosticos})
