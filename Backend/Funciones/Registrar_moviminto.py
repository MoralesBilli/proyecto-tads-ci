from Backend.Extensiones import db
from Modelos.Modelos import Auditrail
from datetime import date
def registrar_audi(origen,accion,clave,):
    try:
        
        nuevo_movimiento = Auditrail(
            origin = origen,
            accion=accion,
            clave_docente = clave,
            created_at = date.today()
        )
        db.session.add(nuevo_movimiento)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return print(f'Problemas al registrar movimiento {str(e)}' )
    
