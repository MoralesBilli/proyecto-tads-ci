from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from datetime import datetime
import os
from Modelos.Modelos import Alumnos, Inscripciones, Calificaciones
from Extensiones import db
import textwrap

def generar_reporte_tutoria(no_control):
    # --- 1. Obtener datos del alumno ---
    alumno = db.session.query(Alumnos).filter_by(no_control=no_control).first()
    if not alumno:
        raise ValueError("No se encontró al alumno con el número de control proporcionado.")

    # --- 2. Obtener información académica ---
    inscripciones = db.session.query(Inscripciones).filter_by(no_control_alumno=no_control).all()
    total_materias_inscritas = len(inscripciones)

    calificaciones_query = db.session.query(Calificaciones).join(Inscripciones).filter(Inscripciones.no_control_alumno == no_control)
    calificaciones_lista = [c.calificacion for c in calificaciones_query.all()]
    
    promedio_general = sum(calificaciones_lista) / len(calificaciones_lista) if calificaciones_lista else 0

    # --- 3. Preparar datos para el PDF ---
    now = datetime.now()
    meses_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    nombre_completo = f"{alumno.nombre} {alumno.apellido_paterno} {alumno.apellido_materno or ''}".strip()
    numero_de_oficio = f"TUT/{now.year}/{alumno.no_control}"
    fecha_actual = now.strftime("%d/%m/%Y")
    dia_texto = str(now.day)
    mes_texto = meses_es[now.month - 1]
    año_texto = str(now.year)
    
    factores_de_riesgo = [factor.nombre for factor in alumno.factores_de_riesgo]
    lista_factores_str = "\n".join(f"- {factor}" for factor in factores_de_riesgo) if factores_de_riesgo else "Ninguno identificado."

    # --- 4. Generar el PDF ---
    output_folder = 'reportes_generados'
    os.makedirs(output_folder, exist_ok=True)
    file_path = os.path.join(output_folder, f"Reporte_{no_control}.pdf")
    
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # --- Encabezado ---
    header_image_path = os.path.join(os.path.dirname(__file__), 'images', 'encabezado.png')
    header_height = 1.5 * inch # Altura deseada para el encabezado

    try:
        # Dibuja la imagen de encabezado que abarca todo el ancho
        c.drawImage(header_image_path, 0, height - header_height, width=width, height=header_height, preserveAspectRatio=False)
    except Exception as e:
        c.drawString(inch, height - 0.8 * inch, f"[Error al cargar encabezado.png: {e}]")
        header_height = 0.5 * inch # Reduce el espacio si la imagen no carga

    # --- Información del Oficio ---
    c.setFont("Helvetica", 10)
    text_x = width - 3.5 * inch
    current_y = height - header_height - 0.5 * inch # Ajusta la posición Y inicial del texto
    c.drawString(text_x, current_y, f"Oficina: Departamento de Servicios Escolares")
    current_y -= 15
    c.drawString(text_x, current_y, f"No. de Oficio: {numero_de_oficio}")
    current_y -= 15
    c.drawString(text_x, current_y, "Asunto: Reporte de Seguimiento Académico")
    current_y -= 15
    c.drawString(text_x, current_y, f"Fecha: {fecha_actual}")

    # --- Cuerpo del Reporte ---
    c.setFont("Helvetica-Bold", 11)
    current_y -= 35
    c.drawString(inch, current_y, "C. JEFE(A) DEL DEPARTAMENTO DE TUTORÍAS")
    current_y -= 15
    c.drawString(inch, current_y, "P R E S E N T E.")

    c.setFont("Helvetica", 11)
    current_y -= 35
    text_obj = c.beginText(inch, current_y)
    text_obj.setLeading(14) # Espacio entre líneas

    line1 = f"El (La) que suscribe, Jefe(a) de Servicios Escolares, por medio del presente informa la situación académica del (la) C. Alumno(a): {nombre_completo} con número de control {alumno.no_control}, inscrito(a) en el {alumno.semestre}o. SEMESTRE del programa educativo de {alumno.carrera.nombre} en modalidad {alumno.carrera.modalidad}."
    
    wrapped_line1 = "\n".join(textwrap.wrap(line1, width=90))
    text_obj.textLines(wrapped_line1)
    text_obj.textLine("")

    text_obj.textLine("Según los registros que obran en el archivo de control escolar, se han identificado los siguientes factores de riesgo asociados al alumno(a) para su oportuno seguimiento:")
    
    c.drawText(text_obj)
    current_y = text_obj.getY()

    # --- Lista de Factores de Riesgo ---
    c.setFont("Helvetica", 10)
    current_y -= 20 # Espacio antes de la lista de factores
    factors_text_obj = c.beginText(1.2 * inch, current_y)
    factors_text_obj.setLeading(12)
    factors_text_obj.textLines(lista_factores_str)
    c.drawText(factors_text_obj)
    current_y = factors_text_obj.getY()

    # --- Información Académica Adicional ---
    current_y -= 30
    c.setFont("Helvetica-Bold", 11)
    c.drawString(inch, current_y, "Información Académica Relevante:")
    c.setFont("Helvetica", 11)
    current_y -= 20
    c.drawString(inch, current_y, f"Promedio General Acumulado: {promedio_general:.2f}")
    current_y -= 15
    c.drawString(inch, current_y, f"Estado Actual: {alumno.estado.replace('_', ' ')}")
    current_y -= 15
    c.drawString(inch, current_y, f"Materias Cursando: {total_materias_inscritas}")

    # --- Cierre ---
    current_y -= 40
    cierre_text = f"Se extiende el presente reporte en la ciudad de Tijuana, B.C., a los {dia_texto} DÍAS DEL MES DE {mes_texto.upper()} DE {año_texto}, para los fines que al departamento de tutorías convengan."
    
    text_obj_cierre = c.beginText(inch, current_y)
    text_obj_cierre.setLeading(14)
    wrapped_cierre = "\n".join(textwrap.wrap(cierre_text, width=90))
    text_obj_cierre.textLines(wrapped_cierre)
    c.drawText(text_obj_cierre)
    current_y = text_obj_cierre.getY()

    # --- Firma ---
    current_y -= 80
    c.drawCentredString(width / 2.0, current_y, "ATENTAMENTE")
    current_y -= 15
    c.drawCentredString(width / 2.0, current_y, '"Excelencia en Educación Tecnológica"')
    current_y -= 15
    c.drawCentredString(width / 2.0, current_y, '"Por una Juventud Integrada al Desarrollo de México"')
    
    current_y -= 50
    c.drawCentredString(width / 2.0, current_y, "_________________________________________")
    c.setFont("Helvetica-Bold", 10)
    current_y -= 15
    c.drawCentredString(width / 2.0, current_y, "FIRMANTE_ESCOLARES") # Reemplazar si es dinámico
    c.setFont("Helvetica", 10)
    current_y -= 15
    c.drawCentredString(width / 2.0, current_y, "JEFA DEL DEPARTAMENTO DE SERVICIOS ESCOLARES")

    c.save()
    return file_path