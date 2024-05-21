from django.shortcuts import render,redirect,get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse, HttpResponseRedirect
from .models import CustomUser,Categoria,Derivacion,Item,Carrito,ItemCarrito,CompraHistorica
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import PasswordResetForm,AuthenticationForm
from django.core.mail import send_mail
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from django.utils.html import strip_tags
from django.core.mail import EmailMessage,send_mail
from django.utils import timezone
from reportlab.lib.pagesizes import A5
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, PageBreak,BaseDocTemplate, PageTemplate,Frame, Paragraph, Spacer, Table
from reportlab.lib.units import cm
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet




class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')  # Redirigir al inicio de sesión después del registro
    template_name = 'registration/signup.html'

# Create your views here.
def index(request):
    return render(request, 'index.html')





def user_login(request):
    next_url = request.GET.get('next', '')  # Obtener la URL de redirección si existe

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username_or_email = cd.get('username')  # Este campo aún se llama 'username' en tu formulario de inicio de sesión
            password = cd['password']
            user = authenticate(request, username=username_or_email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    next_url = request.POST.get('next', reverse('home'))  # Redirigir a la página inicial o a la URL de redirección
                    return HttpResponseRedirect(next_url)
                else:
                    return HttpResponse('El usuario no está activo')
            else:
                return HttpResponse('La información de inicio de sesión no es correcta')
    else:
        form = AuthenticationForm(request)

    return render(request, 'registration/login.html', {'form': form, 'next': next_url})




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


def calcular_precio_derivaciones(items_carrito, derivaciones):
    derivaciones_procesadas = set()
    precio_total_derivaciones = 0
    items_por_derivacion = {}
    
    for derivacion in derivaciones:
        if derivacion in derivaciones_procesadas:
            continue
        
        items_derivacion = items_carrito.filter(derivacion=derivacion)
        items_por_derivacion[derivacion] = items_derivacion
        
        precio_total_derivacion = derivacion.precio
        precio_total_derivaciones += precio_total_derivacion
        
        derivaciones_procesadas.add(derivacion)
    
    return precio_total_derivaciones, items_por_derivacion


def calcular_precio_categorias(items_carrito, categorias):
    categorias_procesadas = set()
    precio_total_categorias = 0
    items_por_categoria = {}
    
    for categoria in categorias:
        if categoria in categorias_procesadas:
            continue
        
        items_categoria = items_carrito.filter(categoria=categoria)
        items_por_categoria[categoria] = items_categoria
        
        precio_total_categoria = categoria.precio
        precio_total_categorias += precio_total_categoria
        
        categorias_procesadas.add(categoria)
    
    return precio_total_categorias, items_por_categoria


def calcular_precio_total_e_items_carrito(usuario):
    items_carrito = Item.objects.filter(itemcarrito__carrito__usuario=usuario) 
    categorias = Categoria.objects.filter(item__in=items_carrito).distinct()
    derivaciones = Derivacion.objects.filter(item__in=items_carrito).distinct()
    
    precio_total_categorias, items_por_categoria = calcular_precio_categorias(items_carrito, categorias)
    precio_total_derivaciones, items_por_derivacion = calcular_precio_derivaciones(items_carrito, derivaciones)
    
    precio_total = precio_total_categorias + precio_total_derivaciones
    
    return {
        'items_por_categoria': items_por_categoria,
        'items_por_derivacion': items_por_derivacion,
        'precio_total_categorias': precio_total_categorias,
        'precio_total_derivaciones': precio_total_derivaciones,
        'precio_total': precio_total,
            }


@login_required(login_url='/login')
def resumen_carrito(request):
    data = calcular_precio_total_e_items_carrito(request.user)
    return render(request, 'examenes/resumen_carritotest.html', data)


#Cambio de clave y envío de correo
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

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

#----------------------------------------------------------------------------------------------------------------------------------------------------------




# Cuenta y editarla 
#----------------------------------------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='/login')
def mi_cuenta(request):
    usuario = request.user
    #compras = Compra.objects.filter(usuario=usuario)
    return render(request, 'cuenta/mi_cuenta.html', {'usuario': usuario})


@login_required(login_url='/login')
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


@login_required(login_url='/login')
def ver_compras_usuario(request):
    # Obtener todas las compras históricas del usuario actual
    compras_usuario = CompraHistorica.objects.filter(usuario=request.user)
    
    return render(request, 'cuenta/historico.html', {'compras_usuario': compras_usuario})

#----------------------------------------------------------------------------------------------------------------------------------------------------------




@login_required(login_url='/login')
def agregar_al_carrito(request):
    if request.method == 'POST':
        elemento_id = request.POST.get('elemento_id')
        tipo = request.POST.get('tipo')
        
        # Obtener el elemento (Producto o Diagnostico) según el tipo y el ID
        elemento = get_object_or_404(Item, id=elemento_id)
        
        # Verificar si el usuario está autenticado
        if request.user.is_authenticated:
            # Obtener el carrito del usuario o crear uno nuevo si no existe
            carrito_usuario, _ = Carrito.objects.get_or_create(usuario=request.user)

            # Verificar si el elemento ya está en el carrito del usuario
            ya_en_carrito = ItemCarrito.objects.filter(carrito=carrito_usuario, item=elemento).exists()

            # Marcar el producto como ya agregado para usar en la plantilla
            elemento.ya_en_carrito = ya_en_carrito

            if not ya_en_carrito:
                # Si el elemento no está en el carrito, agregarlo
                ItemCarrito.objects.create(carrito=carrito_usuario, item=elemento)
                messages.success(request, 'El elemento se ha añadido al carrito.')
            else:
                messages.warning(request, 'El elemento ya está en el carrito.')
        else:
            # Añadir un mensaje de alerta y redirigir a la página de inicio de sesión con el parámetro `next`
            messages.error(request, 'Necesitas estar logeado para agregar productos al carrito.')
            login_url = reverse('login')
            current_url = request.build_absolute_uri()
            redirect_url = f"{login_url}?next={current_url}"
            return redirect(redirect_url)

    # Redireccionar a la página de la categoría del producto agregado
    return redirect(reverse('ver_productos_por_categoria', args=[elemento.categoria.id]))



@login_required(login_url='/login')
def agregar_al_carrito_derivaciones(request):
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
        if ItemCarrito.objects.filter(carrito=carrito_usuario, item=elemento).exists():
            # Si el elemento ya está en el carrito, no es necesario mostrar ningún mensaje
            pass
        else:
            # Agregar el elemento al carrito del usuario
            ItemCarrito.objects.create(carrito=carrito_usuario, item=elemento)
            # No se muestran mensajes

    # Redireccionar a la página de la categoría del producto agregado
    return redirect(reverse('ver_diagnosticos', args=[elemento.derivacion.id]))



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


#--------------------------------------------------------------------------------------------------------------------------------------------
#Generación de PDFS 

from reportlab.lib.styles import ParagraphStyle


@login_required(login_url='/login')
def generar_pdf_productos(request):
    productos_carrito = request.session.get('productos_carrito', None)
    
    if not productos_carrito:
        return HttpResponse("No se encontraron productos en el carrito.")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="productos.pdf"'

    buffer = BytesIO()

    # Obtener datos del usuario
    nombre = request.user.nombre
    apellido = request.user.apellido
    rut = request.user.rut
    direccion = request.user.direccion
    comuna = request.user.comuna
    fecha_nacimiento = request.user.fecha_nacimiento
    edad = datetime.now().year - fecha_nacimiento.year
    fecha_actual = datetime.now().strftime("%d/%m/%Y")

    doc = SimpleDocTemplate(buffer, pagesize=A5)

    # Crear un marco para las páginas
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 2 * cm, id='normal')

    # Crear el PageTemplate con encabezado y pie de página
    template = PageTemplate(id='test', frames=frame, onPage=lambda canvas, doc: add_header_footer(canvas, doc, nombre, apellido, rut, direccion, comuna, edad, fecha_actual))
    doc.addPageTemplates([template])

    elements = []

    # Estilos
    styles = getSampleStyleSheet()
    header_style = styles['Heading1']
    normal_style = styles['BodyText']
    
    # Nuevo estilo para la categoría en negrita
    bold_category_style = ParagraphStyle(name='BoldCategory', parent=normal_style)
    bold_category_style.fontName = 'Helvetica-Bold'  # Cambia la fuente a negrita

    # Organizar los productos por categoría
    productos_por_categoria = {}
    for producto in productos_carrito:
        categoria = producto['item__categoria__nombre']
        if categoria not in productos_por_categoria:
            productos_por_categoria[categoria] = []
        productos_por_categoria[categoria].append(producto['item__nombre'])


    elements.append(Spacer(1, 7))

    for categoria, productos in productos_por_categoria.items():
        elements.append(Paragraph(f"<b>{categoria}</b>", bold_category_style))  # Categoría en negrita
        for producto in productos:
            elements.append(Paragraph(producto, normal_style))
            # Verificar si hay espacio suficiente para más productos en esta página
            if buffer.tell() > A5[1] * 0.7:  # 70% del alto de la página A5
                elements.append(PageBreak())  # Agregar un salto de página
                break

    # Construir el documento
    doc.build(elements)

    response.write(buffer.getvalue())
    buffer.close()

    return response

def add_header_footer(canvas, doc, nombre, apellido, rut, direccion, comuna, edad, fecha_actual):
    width, height = A5

    # Header
    canvas.setFont('Helvetica-Bold', 12)
    canvas.drawString(40, height - cm, "Nuuk Medical")

    # Datos del usuario
    canvas.setFont('Helvetica', 10)
    text = [
        f"Sr.(a) {nombre} {apellido}",
        f"Edad: {edad} años",
        f"Domicilio: {direccion}",
        f"Ciudad: {comuna}",
        f"RUT: {rut}"
    ]
    y = height - 2 * cm
    for line in text:
        canvas.drawString(40, y, line)
        y -= 12  # Adjust line spacing as needed

    # Footer - Page Number and Date
    page_num = canvas.getPageNumber()
    canvas.drawRightString(width - 40, cm, f"Página {page_num}")
    canvas.drawString(40, cm, f"Fecha: {fecha_actual}")


@login_required(login_url='/login')
def generar_pdf_derivaciones(request):
    derivaciones_carrito = request.session.get('derivaciones_carrito', None)
    
    if not derivaciones_carrito:
        return HttpResponse("No se encontraron derivaciones en el carrito.")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="derivaciones.pdf"'

    buffer = BytesIO()

    # Obtener datos del usuario
    nombre = request.user.nombre
    apellido = request.user.apellido
    rut = request.user.rut
    direccion = request.user.direccion
    comuna = request.user.comuna
    fecha_nacimiento = request.user.fecha_nacimiento
    edad = datetime.now().year - fecha_nacimiento.year
    fecha_actual = datetime.now().strftime("%d/%m/%Y")

    doc = SimpleDocTemplate(buffer, pagesize=A5)

    # Crear un marco para las páginas
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 2 * cm, id='normal')

    # Crear el PageTemplate
    template = PageTemplate(id='test', frames=frame, onPage=lambda canvas, doc: add_header_footer(canvas, doc, nombre, apellido, rut, direccion, comuna, edad, fecha_actual))
    doc.addPageTemplates([template])

    elements = []

    # Estilos
    styles = getSampleStyleSheet()
    normal_style = styles['BodyText']
    
    # Nuevo estilo para la derivación en negrita
    bold_derivation_style = ParagraphStyle(name='BoldDerivation', parent=normal_style)
    bold_derivation_style.fontName = 'Helvetica-Bold'  # Cambia la fuente a negrita

    # Derivaciones del carrito
    elements.append(Paragraph("Se solicita evaluación por especialidad:", normal_style))
    elements.append(Spacer(1, 7))

    # Organizar las derivaciones por nombre de derivación
    derivaciones_por_nombre = {}
    for derivacion in derivaciones_carrito:
        nombre_derivacion = derivacion['item__derivacion__nombre']
        if nombre_derivacion not in derivaciones_por_nombre:
            derivaciones_por_nombre[nombre_derivacion] = []
        derivaciones_por_nombre[nombre_derivacion].append(derivacion['item__nombre'])

    for nombre_derivacion, items in derivaciones_por_nombre.items():
        elements.append(Paragraph(f"<b>Derivación: {nombre_derivacion}</b>", bold_derivation_style))  # Derivación en negrita
        for item in items:
            elements.append(Paragraph(item, normal_style))
            elements.append(Spacer(1, 7))

    # Construir el documento
    doc.build(elements)

    response.write(buffer.getvalue())
    buffer.close()

    return response

def add_header_footer(canvas, doc, nombre, apellido, rut, direccion, comuna, edad, fecha_actual):
    width, height = A5

    # Header
    canvas.setFont('Helvetica-Bold', 12)
    canvas.drawString(40, height - cm, "Nuuk Medical")

    # Datos del usuario
    canvas.setFont('Helvetica', 10)
    text = [
        f"Sr.(a) {nombre} {apellido}",
        f"Edad: {edad} años",
        f"Domicilio: {direccion}",
        f"Ciudad: {comuna}",
        f"RUT: {rut}"
    ]
    y = height - 2 * cm
    for line in text:
        canvas.drawString(40, y, line)
        y -= 12  # Adjust line spacing as needed

    # Footer - Page Number and Date
    page_num = canvas.getPageNumber()
    canvas.drawRightString(width - 40, cm, f"Página {page_num}")
    canvas.drawString(40, cm, f"Fecha: {fecha_actual}")
#--------------------------------------------------------------------------------------------------------------------------------------

def send_email(subject, message, from_email, recipient_list, attachment_file):
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=recipient_list
    )

    email.attach(attachment_file.name, attachment_file.read(), 'application/pdf')

    email.send()



@login_required(login_url='/login')
def pago_exitoso(request):
    user = request.user
    carrito, created = Carrito.objects.get_or_create(usuario=user)

    # Supongamos que el pago fue exitoso
    pago_exitoso = True  # Aquí debería ir la lógica real del pago

    if pago_exitoso:
        # Guardar los productos del carrito en la sesión
        productos_carrito = list(carrito.itemcarrito_set.filter(item__categoria__isnull=False).values('item__nombre', 'item__categoria__nombre'))
        request.session['productos_carrito'] = productos_carrito
        
        # Guardar las derivaciones del carrito en la sesión
        derivaciones_carrito = list(carrito.itemcarrito_set.filter(item__derivacion__isnull=False).values('item__nombre', 'item__derivacion__nombre'))
        request.session['derivaciones_carrito'] = derivaciones_carrito

        # Registrar la compra en CompraHistorica
        for item_carrito in carrito.itemcarrito_set.all():
            CompraHistorica.objects.create(
                usuario=user,
                producto=item_carrito.item,
                fecha_compra=timezone.now(),
                costo=0  # Asumiendo que tu modelo Item tiene un campo precio
            )

        # Limpiar el carrito después de registrar la compra
        carrito.limpiar_carrito()

        return render(request, 'examenes/pago_exitoso.html')  # Redirige a una página de confirmación de compra
    else:
        messages.error(request, "Hubo un problema con el pago. Por favor, inténtelo de nuevo.")
        return redirect('examenes/resumen_carrito')


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



def enviar_correo_con_adjuntos(usuario, asunto, cuerpo, pdf_productos, pdf_derivaciones):
    # Obtener el correo electrónico del usuario
    destinatario = usuario.email
    
    # Renderizar el cuerpo del correo electrónico como texto plano
    cuerpo_plano = strip_tags(cuerpo)
    
    
    # Crear el objeto EmailMessage
    email = EmailMessage(
        subject=asunto,
        body=cuerpo_plano,
        from_email='Nuuk_medical@options.cl',  # Cambia esto por tu dirección de correo electrónico
        to=[destinatario],
    )
    
    email.attach('productos.pdf', pdf_productos, 'application/pdf')
    email.attach('derivaciones.pdf', pdf_derivaciones, 'application/pdf')
    
    # Enviar el correo electrónico
    email.send(fail_silently=False)