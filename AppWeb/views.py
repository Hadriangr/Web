from django.shortcuts import render,redirect,get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse, HttpResponseRedirect
from .models import CustomUser,Categoria,Derivacion,Item,Carrito,ItemCarrito,Compra,CompraItem
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from django.utils.html import strip_tags
from django.utils import timezone
from reportlab.lib.pagesizes import A5
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, PageBreak, PageTemplate,Frame, Paragraph, Spacer
from reportlab.lib.units import cm
from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.conf import settings
import os
from reportlab.lib import colors
from django.core.files.storage import default_storage
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders




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


def validate_email(value):
    if not value.endswith('@example.com'):
        raise ValidationError('Invalid email address')

def user_logout(request):
    logout(request)
    return redirect('index')

#Cambio de clave y envío de correo




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

def registro_done(request):
    return render(request,'registration/registro_done.html')

# def register(request):
#     if request.method == 'POST':
#         user_form = CustomUserCreationForm(request.POST)
#         if user_form.is_valid():
#             user = user_form.save(commit=False)
#             user.username = user_form.cleaned_data.get('email')  # Usar el correo electrónico como nombre de usuario
#             user.save()
#             messages.success(request, '¡Registro exitoso! Por favor, inicia sesión con tu nueva cuenta.')  # Mensaje de éxito
#             return redirect('registro-exitoso')  # Redireccionar al usuario a la página de inicio de sesión
#     else:
#         user_form = CustomUserCreationForm()
#     return render(request, 'registration/registro.html', {'user_form': user_form})


def registro_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Aquí podrías redirigir al usuario a una página de éxito o hacer cualquier otra acción deseada
            return redirect('registro-exitoso')  # Reemplaza 'pagina_de_exito' con el nombre de la URL de tu página de éxito
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})

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
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

def add_header_footer(canvas, doc, nombre, apellido, rut, direccion, comuna, edad, fecha_actual):
    width, height = A5

    # Header
    logo_path = finders.find('assets/img/logo.jpeg')
    if logo_path:
        canvas.drawImage(logo_path, 40, height - 3 * cm, width=3 * cm, height=3 * cm)
    else:
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
    y = height - 4 * cm  # Ajustar esta posición inicial para crear más espacio entre el logo y el texto del usuario
    for line in text:
        canvas.drawString(40, y, line)
        y -= 12

    #y_for_sale_number = height - 4 * cm
    #canvas.drawRightString(width - 40, y_for_sale_number, f"Número: {numero_venta}")

    # Añadir imagen de la firma y ajustar posición
    firma_path = finders.find('assets/img/firma.jpeg')
    if firma_path:
        y_firma = 2 * cm + 18  # Ajustar esta posición para que esté 2 cm por encima del número de página y más cerca del texto
        canvas.drawImage(firma_path, 40, y_firma, width=5 * cm, height=2 * cm)  # Ajustar tamaño si es necesario
        y_texto_firma = y_firma - 12  # Ajustar la posición del texto más cerca de la firma
    else:
        y_texto_firma = y  # Si no hay firma, usar la posición actual

    # Texto plano debajo de la firma
    canvas.setFont('Helvetica', 10)
    texto_firma_1 = "Dra. Marcia Guajardo Rivera"
    texto_firma_2 = "Rut. 15.140.627-0"
    canvas.drawString(40, y_texto_firma, texto_firma_1)
    canvas.drawString(40, y_texto_firma - 12, texto_firma_2)  # Mover el segundo texto una línea abajo

    # Footer - Número de página y fecha
    page_num = canvas.getPageNumber()
    canvas.drawRightString(width - 40, cm, f"Página {page_num}")
    canvas.drawString(40, cm, f"Fecha: {fecha_actual}")

@login_required(login_url='/login')
@transaction.atomic
def generar_pdf_productos(request):
    try:
        logger.info("Iniciando la generación del PDF de productos.")
        productos_carrito = request.session.get('productos_carrito', None)

        if not productos_carrito:
            logger.warning("No se encontraron productos en el carrito.")
            return render(request, 'vacio.html')

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="productos.pdf"'

        buffer = BytesIO()

        # Obtener datos del usuario
        user = request.user
        nombre = user.nombre
        apellido = user.apellido
        rut = user.rut
        direccion = user.direccion
        comuna = user.comuna
        fecha_nacimiento = user.fecha_nacimiento
        edad = datetime.now().year - fecha_nacimiento.year
        fecha_actual = datetime.now().strftime("%d/%m/%Y")

        doc = SimpleDocTemplate(buffer, pagesize=A5)

        # Crear un marco para las páginas dejando espacio para el header (5 cm) y footer (5 cm)
        frame = Frame(doc.leftMargin, doc.bottomMargin + 5 * cm, doc.width, doc.height - 10 * cm, id='normal')

        # Crear el PageTemplate con encabezado y pie de página
        template = PageTemplate(id='test', frames=frame, onPage=lambda canvas, doc: add_header_footer(canvas, doc, nombre, apellido, rut, direccion, comuna, edad, fecha_actual))
        doc.addPageTemplates([template])

        elements = []

        # Estilos
        styles = getSampleStyleSheet()
        normal_style = styles['BodyText']
        bold_category_style = ParagraphStyle(name='BoldCategory', parent=normal_style, fontName='Helvetica-Bold')

        # Productos del carrito
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("<b>Orden de Examenes</b>", bold_category_style))

        for producto in productos_carrito:
            elements.append(Paragraph(producto['producto__nombre'], normal_style))
            if len(elements) > 30:  # Asegura que haya suficiente espacio en cada página
                elements.append(PageBreak())
                break

        logger.info("Construyendo el documento PDF de productos.")
        # Construir el documento
        doc.build(elements)

        response.write(buffer.getvalue())
        buffer.close()

        # Clear session data to avoid reuse of old data
        del request.session['productos_carrito']

        logger.info("PDF de productos generado exitosamente.")
        return response
    except Exception as e:
        logger.error("Error generando PDF de productos: %s", e)
        return render(request, 'vacio.html')


@login_required(login_url='/login')
def generar_pdf_derivaciones(request):
    try:
        logger.info("Iniciando la generación del PDF de derivaciones.")
        derivaciones_carrito = request.session.get('derivaciones_carrito', None)

        if not derivaciones_carrito:
            logger.warning("No se encontraron derivaciones en el carrito.")
            return render(request, 'vacio.html')

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="derivaciones.pdf"'

        buffer = BytesIO()

        # Obtener datos del usuario
        user = request.user
        nombre = user.nombre
        apellido = user.apellido
        rut = user.rut
        direccion = user.direccion
        comuna = user.comuna
        fecha_nacimiento = user.fecha_nacimiento
        edad = datetime.now().year - fecha_nacimiento.year
        fecha_actual = datetime.now().strftime("%d/%m/%Y")

        doc = SimpleDocTemplate(buffer, pagesize=A5)

        # Crear un marco para las páginas dejando espacio para el header (5 cm) y footer (5 cm)
        frame = Frame(doc.leftMargin, doc.bottomMargin + 5 * cm, doc.width, doc.height - 10 * cm, id='normal')

        # Crear el PageTemplate con encabezado y pie de página
        template = PageTemplate(id='test', frames=frame, onPage=lambda canvas, doc: add_header_footer(canvas, doc, nombre, apellido, rut, direccion, comuna, edad, fecha_actual))
        doc.addPageTemplates([template])

        elements = []

        # Estilos
        styles = getSampleStyleSheet()
        normal_style = styles['BodyText']
        bold_category_style = ParagraphStyle(name='BoldCategory', parent=normal_style, fontName='Helvetica-Bold')

        # Derivaciones del carrito
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("<b>INTERCONSULTA</b>", bold_category_style))

        for derivacion in derivaciones_carrito:
            elements.append(Paragraph(derivacion['producto__nombre'], normal_style))
            if len(elements) > 30:  # Asegura que haya suficiente espacio en cada página
                elements.append(PageBreak())
                break

        logger.info("Construyendo el documento PDF de derivaciones.")
        # Construir el documento
        doc.build(elements)

        response.write(buffer.getvalue())
        buffer.close()

        # Clear session data to avoid reuse of old data
        del request.session['derivaciones_carrito']

        logger.info("PDF de derivaciones generado exitosamente.")
        return response
    except Exception as e:
        logger.error("Error generando PDF de derivaciones: %s", e)
        return render(request, 'vacio.html')


#--------------------------------------------------------------------------------------------------------------------------------------




@login_required(login_url='/login')
@transaction.atomic
def pago_exitoso(request):
    user = request.user
    carrito, created = Carrito.objects.get_or_create(usuario=user)

    # Supongamos que el pago fue exitoso
    pago_exitoso = True  # Aquí debería ir la lógica real del pago

    if pago_exitoso:
        # Crear la compra
        compra = Compra(usuario=user)
        compra.save()

        costo_total = 0
        categorias_incluidas = set()
        derivaciones_incluidas = set()

        productos_carrito = []
        derivaciones_carrito = []

        # Añadir items del carrito a la compra y calcular el costo
        for item_carrito in carrito.itemcarrito_set.all():
            producto = item_carrito.item
            cantidad = 1  # Asumiendo que cada item en el carrito representa una unidad. Ajusta si es necesario.

            # Verificar si la categoría del producto ya está incluida
            if producto.categoria and producto.categoria.id not in categorias_incluidas:
                costo_total += producto.categoria.precio
                categorias_incluidas.add(producto.categoria.id)

            # Verificar si la derivación del producto ya está incluida
            if producto.derivacion and producto.derivacion.id not in derivaciones_incluidas:
                costo_total += producto.derivacion.precio
                derivaciones_incluidas.add(producto.derivacion.id)

            # Crear un CompraItem
            CompraItem.objects.create(
                compra=compra,
                producto=producto,
                cantidad=cantidad,
                costo=producto.categoria.precio if producto.categoria else producto.derivacion.precio
            )

            # Añadir el producto a la lista para la sesión
            productos_carrito.append({
                'producto__nombre': producto.nombre,
                'producto__categoria__nombre': producto.categoria.nombre if producto.categoria else '',
                'producto__derivacion__nombre': producto.derivacion.nombre if producto.derivacion else '',
            })

            # Si hay derivaciones, añadir a la lista de derivaciones para la sesión
            if producto.derivacion:
                derivaciones_carrito.append({
                    'producto__nombre': producto.nombre,
                    'producto__derivacion__nombre': producto.derivacion.nombre,
                })

        # Actualizar el costo total de la compra
        compra.costo_total = costo_total
        compra.save()

        # Guardar los productos del carrito en la sesión
        request.session['productos_carrito'] = productos_carrito
        request.session['derivaciones_carrito'] = derivaciones_carrito

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



def nosotros(request):
    return render(request,'nosotros.html')


def terminos_condiciones_view(request):
    terminos_file_path = os.path.join(settings.MEDIA_ROOT, 'terminos_condiciones.pdf')
    return render(request, 'terminos_condiciones.html', {'terminos_file_path': terminos_file_path})