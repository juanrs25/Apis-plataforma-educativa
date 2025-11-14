from spyne import ServiceBase, rpc, Integer, Unicode, Array
from db import SessionLocal
from models import PQRS
from datetime import datetime

class PQRService(ServiceBase):

    @rpc(Integer, Unicode, Unicode, Unicode, Unicode, _returns=Unicode)
    def crearPQR(ctx, id_usuario, tipo, asunto, descripcion, fecha_creacion):
        db = SessionLocal()
        try:
            nueva = PQRS(
                id_usuario=id_usuario,
                tipo=tipo,
                asunto=asunto,
                descripcion=descripcion,
                fecha_creacion=fecha_creacion
            )
            db.add(nueva)
            db.commit()
            return "PQR creada correctamente"
        except Exception as e:
            db.rollback()
            return f"Error: {str(e)}"
        finally:
            db.close()


    @rpc(Integer, _returns=Array(Unicode))
    def listarPQR(ctx, id_usuario):
        db = SessionLocal()
        try:
            lista = db.query(PQRS).filter_by(id_usuario=id_usuario).all()
            salida = []

            for p in lista:
                salida.append(
                    f"{p.id} | {p.tipo} | {p.asunto} | {p.descripcion} | {p.fecha_creacion}"
                )
            return salida

        except Exception as e:
            return [f"Error: {str(e)}"]
        finally:
            db.close()

    @rpc(Integer, Unicode, Unicode, Unicode, _returns=Unicode)
    def actualizarPQR(ctx, id, tipo, asunto, descripcion):
        db = SessionLocal()
        try:
            p = db.query(PQRS).filter_by(id=id).first()

            if not p:
                return "PQR no encontrada"

            p.tipo = tipo
            p.asunto = asunto
            p.descripcion = descripcion

            db.commit()
            return "PQR actualizada correctamente"

        except Exception as e:
            db.rollback()
            return f"Error al actualizar: {str(e)}"
        finally:
            db.close()

    @rpc(Integer, _returns=Unicode)
    def eliminarPQR(ctx, id):
        db = SessionLocal()
        try:
            p = db.query(PQRS).filter_by(id=id).first()

            if not p:
                return "PQR no encontrada"

            db.delete(p)
            db.commit()
            return "PQR eliminada correctamente"

        except Exception as e:
            db.rollback()
            return f"Error al eliminar: {str(e)}"
        finally:
            db.close()


