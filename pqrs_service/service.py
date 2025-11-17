from spyne import ServiceBase, rpc, Integer, Unicode, Array
from db import SessionLocal
from models import PQRS
from datetime import datetime
import requests


class PQRService(ServiceBase):

    @staticmethod
    def usuario_existe(id_usuario):
        try:
            url = f"http://localhost:5001/usuarios-public/{id_usuario}"

            response = requests.get(url, timeout=3)

            if response.status_code != 200:
                return False

            data = response.json()
            return data.get("existe", False)

        except:
            return False

    @rpc(Integer, Unicode, Unicode, Unicode, Unicode, _returns=Unicode)
    def crearPQR(ctx, id_usuario, tipo, asunto, descripcion, fecha_creacion):

        if not PQRService.usuario_existe(id_usuario):
            return "El usuario no existe en el servicio de usuarios"

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

        if not PQRService.usuario_existe(id_usuario):
            return ["El usuario no existe en el servicio de usuarios"]

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
