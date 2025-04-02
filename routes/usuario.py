from app import app
from flask import request
from flask import render_template
from models.usuario import Usuario


@app.route("/usuario/", methods=['POST'])
def usuario():
    try:
        mensaje = None
        estado = False

        if request.method == "POST":
            username = request.form["txtUsername"]
            password = request.form["txtPassword"]
            nombre_completo = request.form["txtNombre_completo"]  # Corregido: request.form
            correo = request.form["txtCorreo"]  # Corregido: request.form

            # Aquí podrías agregar lógica para procesar los datos, como guardarlos en la base de datos
            estado = True
            mensaje = "Usuario registrado exitosamente"

    except Exception as error:
        mensaje = str(error)
        estado = False

    return {"mensaje": mensaje, "estado": estado}