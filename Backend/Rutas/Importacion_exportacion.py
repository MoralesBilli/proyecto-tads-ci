from Extensiones import db
from flask import Blueprint, jsonify,request
from Funciones.ImportarExcel import importar_grupos,importar_calificaciones, importar_docentes
from Modelos.Modelos import Grupos, Carreras,Materias
import os
from Funciones.Registrar_moviminto import registrar_audi
from flask import send_file
from Funciones.ExportarConstancia import generar_reporte_tutoria
from flask import send_file
from Funciones.ExportarConstancia import generar_reporte_tutoria

Import_export_bp = Blueprint('Import_export',__name__)

#folder para guardar el archivo de manera temporal


@Import_export_bp.route('/api/importar/grupos',methods=['POST'])
def importar_Excel_grupos():
    try:
        UPLOAD_FOLDER = 'grupos'
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        carreras =  Carreras.query.all()
        grupos = Grupos.query.all()

        carreras_nombres = [carrera.nombre for carrera in carreras]
        grupos_nombres = [grupo.grupo for grupo in grupos]

        #validaciones 
        if 'archivo' not in request.files:
            return jsonify({'error': 'No fue enviaddo un archivo'}),400
        
        archivo = request.files['archivo']

        if archivo.filename == '':
            return jsonify({'error': 'El nombre del archivo está vacío'}),400
        
        if not archivo.filename.endswith(('.xls','.xlsx')):
            return jsonify({'error':'Formato de archivo no válido'}),400
        

        ruta = os.path.join(UPLOAD_FOLDER, archivo.filename)
        archivo.save(ruta)

        procesamiento = importar_grupos(ruta,carreras_nombres,grupos_nombres)
       
        print(procesamiento)
        os.remove(ruta)

        if procesamiento.startswith("No se pudo importar") or "Error" in procesamiento:
            return jsonify({'error': procesamiento}), 400
        
        registrar_audi('Alumnos','Importar grupo',212420)

        return jsonify({'message': 'Archivo procesado correctamente', 'resultado': procesamiento}),200
    except Exception  as e:
        return jsonify({'error': f'Error al importar el archivo {str(e)}'}),400


@Import_export_bp.route('/api/importar/calificaciones',methods=['POST'])
def importar_Excel_Calificaciones():
    try:
        UPLOAD_FOLDER = 'calificacion'
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        grupos = Grupos.query.all()
        materias = Materias.query.all()
        materias_nombres = [materia.nombre for materia in materias]
        grupos_nombres = [grupo.grupo for grupo in grupos]
        #validaciones 
        if 'archivo' not in request.files:
            return jsonify({'error': 'No fue enviaddo un archivo'}),400
        
        archivo = request.files['archivo']

        if archivo.filename == '':
            return jsonify({'error': 'El nombre del archivo está vacío'}),400
        
        if not archivo.filename.endswith(('.xls','.xlsx')):
            return jsonify({'error':'Formato de archivo no válido'}),400
        

        ruta = os.path.join(UPLOAD_FOLDER, archivo.filename)
        archivo.save(ruta)

        procesamiento =  importar_calificaciones(ruta,grupos_nombres,materias_nombres)
       

        os.remove(ruta)

        if procesamiento.startswith("No se pudo importar") or "Error" in procesamiento:
            return jsonify({'error': procesamiento}), 400
        
        registrar_audi('Alumnos','Importar grupo',212420)

        return jsonify({'mensaje':'Archivo subido', 'resultado' : procesamiento})
    except Exception  as e:
        return jsonify({'error': f'Error al importar el archivo {str(e)}'}),400

@Import_export_bp.route('/api/exportar/reporte_tutoria/<no_control>', methods=['GET'])
def exportar_reporte_alumno(no_control):
    try:
        # Generar el reporte
        pdf_path = generar_reporte_tutoria(no_control)
        
        if not pdf_path or not os.path.exists(pdf_path):
            return jsonify({'error': 'No se pudo generar el archivo PDF.'}), 500

        # Enviar el archivo
        response = send_file(pdf_path, as_attachment=True, download_name=os.path.basename(pdf_path))
        
        # Opcional: Registrar auditoría si es necesario
        # registrar_audi('Reportes', 'ExportarConstancia', ID_DE_USUARIO_AQUI)

        return response

    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Ocurrió un error inesperado: {str(e)}'}), 500
    finally:
        # Limpiar el archivo generado después de enviarlo
        if 'pdf_path' in locals() and os.path.exists(pdf_path):
            # Usamos un pequeño delay o manejamos la eliminación de forma asíncrona si es necesario
            # Para este caso, una eliminación directa funcionará si el archivo no está bloqueado
            try:
                os.remove(pdf_path)
            except Exception as e:
                print(f"Error al eliminar el archivo {pdf_path}: {e}")

@Import_export_bp.route('/api/importar/docentes',methods=['POST'])
def importar_Excel_Docentes():
    try:
        UPLOAD_FOLDER = 'docentes'
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        #validaciones 
        if 'archivo' not in request.files:
            return jsonify({'error': 'No fue enviaddo un archivo'}),400
        
        archivo = request.files['archivo']

        if archivo.filename == '':
            return jsonify({'error': 'El nombre del archivo está vacío'}),400
        
        if not archivo.filename.endswith(('.xls','.xlsx')):
            return jsonify({'error':'Formato de archivo no válido'}),400
        

        ruta = os.path.join(UPLOAD_FOLDER, archivo.filename)
        archivo.save(ruta)

        procesamiento =  importar_docentes(ruta)
       

        os.remove(ruta)

        if procesamiento.startswith("No se pudo importar") or "Error" in procesamiento:
            return jsonify({'error': procesamiento}), 400
        
        registrar_audi('Alumnos','Importar grupo',212420)

        return jsonify({'mensaje':'Archivo subido', 'resultado' : procesamiento})
    except Exception  as e:
        return jsonify({'error': f'Error al importar el archivo {str(e)}'}),400

