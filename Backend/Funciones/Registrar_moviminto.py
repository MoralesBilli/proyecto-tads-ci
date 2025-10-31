from Extensiones import db
from Modelos.Modelos import Auditrail
from datetime import datetime
def registrar_audi(origen,accion,clave,):
    try:
        fecha = datetime.today()
        nuevo_movimiento = Auditrail(
            origin = origen,
            accion=accion,
            clave_docente = clave,
            create_at = fecha
        )
        db.session.add(nuevo_movimiento)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return print(f'Problemas al registrar movimiento {str(e)}' )
    
