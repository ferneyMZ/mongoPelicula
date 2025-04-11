from app import app, recaptcha
from flask import render_template, request, session, redirect
from models.usuario import Usuario
from dotenv import load_dotenv
import os
import yagmail
import threading
import string, random

load_dotenv()

@app.route("/")
def inicio():
    return render_template("frmIniciarSesion.html")

def enviarCorreo(email=None, destinatario=None, asunto=None, mensaje=None,archivosAdjunto=None):
    try:
        email.send(to=destinatario, subject=asunto, contents=mensaje, attachments=archivosAdjunto)
    except Exception as error:
        print(str(error))
        
@app.route("/usuario/", methods=['GET'])
def usuario():
    try:   
        mensaje=None     
        user= Usuario.objects()  
    except Exception as error:
        mensaje=str(error)
    
    return {"mensaje": mensaje, "peliculas":user}

@app.route("/iniciarSesion/",  methods=['POST'])
def iniciarSesion():   
    mensaje = ""
    try:    
        if request.method=='POST':               
            if recaptcha.verify():           
                username=request.form['txtUser']
                password=request.form['txtPassword'] 
                print(username,password)
                usuario = Usuario.objects(usuario=username,password=password).first()
           
                print(usuario)
                if usuario:
                    session['user']=username
                    session['name_user']=f"{usuario.nombres} {usuario.apellidos}"
                    email = yagmail.SMTP("ferney.m2003@gmail.com",os.environ.get("PASSWORD-ENVIAR-CORREO" \
                    ""), 
                                    encoding="utf-8")
                    asunto = "Ingreso al Sistema"
                    archiivosAdjunto = ["manual.pdf","static/imagenes/avatar.png"]
                    mensaje = f"Cordial saludo <b>{usuario.nombres} {usuario.apellidos}.</b> \
                            Bienvenido a nuestro aplicativo Gestión peliculas. \
                            Enviamos Manual de usuario del aplicativo en formato pdf.<br><br>\
                            Cordialmente,<br><br><br> \
                            <b>Administración<br>Aplicativo Gestión Películas.</b>"
                    thread = threading.Thread(target=enviarCorreo,
                                            args=(email, [usuario.correo,"augus.m2002@gmail.com"], asunto, mensaje,archiivosAdjunto))
                    thread.start()
                    return redirect("/home/")
                else:
                    mensaje="Credenciales no válidas"
            else:
                mensaje = "Debe validar primero el recaptcha"
        else:
            mensaje="No permitido"
    except Exception as error:
        mensaje=str(error)
    
    return render_template("frmIniciarSesion.html", mensaje=mensaje)

@app.route("/usuario/", methods=['POST'])
def addUsuario():
    try:
        mensaje=None
        estado=False
        datos= request.get_json(force=True)
        usuario = Usuario(**datos)
        usuario.save()
        estado=True
        mensaje="Usuario agregado correctamente"       
        
    except Exception as error:
        mensaje=str(error) 
        
    return {"estado":estado, "mensaje":mensaje}


@app.route("/home/")
def home():
    if("user" in session):
        return render_template("contenido.html")
    else:
        mensaje="Debe primero ingresar con credenciales válidas"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)

@app.route("/salir/")
def exit():
    session.clear()
    mensaje="Ha cerrado la sesión de forma"
    return render_template("frmIniciarSesion.html",mensaje=mensaje)
@app.route("/usuario/",methods=["GET"])
def listarUsuario():
    try:
        mensaje=None
        usuarios=Usuario.objects()
    except Exception as error:
        mensaje=str(error)
    return {"mensaje": mensaje, "usuarios": usuarios}

def generar_contraseña(n=8):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(n))

@app.route("/recuperarcontra/", methods=["GET","POST"])
def recuperarcontra():
    mensaje = ""
    try:
        if request.method == 'POST':
            usuario = request.form['username']
            correo_form = request.form['email']
            # Verifica que el usuario exista
            user = Usuario.objects(usuario=usuario, correo=correo_form).first()
            if user:
                nueva_pass = generar_contraseña()
                user.password = nueva_pass  
                user.save()

                correo_envio = os.environ.get("CORREO")
                clave_envio = os.environ.get("PASSWORD-ENVIAR-CORREO")
                email = yagmail.SMTP(correo_envio, clave_envio, encoding="utf-8")
                asunto = "se cambio la contraseña"
                mensaje = f"Hola {user.nombres}, tu contraseña es: {nueva_pass}"

                email.send(to=user.correo, subject=asunto, contents=mensaje)
                return render_template("iniciarSesion.html", mensaje="Nueva contraseña enviada al correo")
            else:
                mensaje = "Usuario o correo incorrecto"
    except Exception as e:
        mensaje = str(e)

    return render_template("Recuperar.html", mensaje=mensaje)
    
    
    
    
        
    
