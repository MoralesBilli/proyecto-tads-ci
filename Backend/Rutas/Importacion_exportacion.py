from Extensiones import db
from flask import Blueprint, jsonify,request
from Funciones.ImportarExcel import importar_grupos,importar_calificaciones
from Modelos.Modelos import Grupos, Carreras
import os

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
       

        os.remove(ruta)

        if procesamiento.startswith("No se pudo importar") or "Error" in procesamiento:
            return jsonify({'error': procesamiento}), 400
        return jsonify({'mensaje': 'Archivo procesado correctamente', 'resultado': procesamiento})
    except Exception  as e:
        return jsonify({'error': f'Error al importar el archivo {str(e)}'}),400


@Import_export_bp.route('/api/importar/calificaciones',methods=['POST'])
def importar_Excel_Calificaciones():
    try:
        UPLOAD_FOLDER = 'calificacion'
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

        procesamiento = importar_calificaciones(ruta)
       

        os.remove(ruta)

        return jsonify({'mensaje':'Archivo subido', 'resultado' : procesamiento})
    except Exception  as e:
        return jsonify({'error': f'Error al importar el archivo {str(e)}'}),400

