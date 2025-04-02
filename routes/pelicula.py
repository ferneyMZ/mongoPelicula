from app import app
from flask import request
from flask import render_template
from models.pelicula import Pelicula
from models.genero import Genero


@app.route("/pelicula/", methods=["GET"])
def listPelicula():
    
    try:
        mensaje=None
        peliculas = Pelicula.objects()
        
    except Exception as error:
        mensaje = str(error)
        
    return {"mensaje":mensaje, "peliculas":peliculas}

@app.route("/pelicula/", methods=["POST"])
def addPelicula():
    try:
        mensaje=None
        estado = False
        if request.method=="POST":
            datos=request.get_json(force=True)
            genero=Genero.objects(id=datos["genero"]).first()
            if genero is None:
                mensaje="Genero no existe"
            else:
                datos["genero"]=genero
                pelicula=Pelicula(**datos)
                pelicula.save()
                estado=True
                mensaje="Pelicula guardada correctamente"
        else:
            mensaje = "Metodo no permitido"
    except Exception as error:
        mensaje = str(error)
        
    return {"mensaje":mensaje, "estado":estado}

@app.route("/pelicula/", methods=["PUT"])
def updatePelicula():
    try:
        mensaje=None
        estado = False
        if request.method=="PUT":
            datos=request.get_json(force=True)
            genero=Genero.objects(id=datos["genero"]).first()
            pelicula=Pelicula.objects(id=datos["id"]).first()
            pelicula.codigo=datos["codigo"]
            pelicula.titulo=datos["titulo"]
            pelicula.protagonista=datos["protagonista"]
            pelicula.duracion=datos["duracion"]
            pelicula.resumen=datos["resumen"]
            pelicula.foto=datos["foto"]
            genero=Genero.objects(id=datos["genero"]).first()
            if genero is None:
                mensaje="Genero no existe"
            else:
                pelicula.genero=genero
                pelicula.save()
                estado=True
                mensaje =f"{mensaje}Pelicula actualizada correctamente"
        else:
            mensaje = "Metodo no permitido"
    except Exception as error:
        mensaje = str(error)
    return {"mensaje":mensaje, "estado":estado}

@app.route("/pelicula/", methods=["DELETE"])
def deletePelicula():
    try:
        mensaje=None
        estado = False
        if request.method=="DELETE":
            datos=request.get_json(force=True)
            pelicula=Pelicula.objects(id=datos["id"]).first()
            pelicula.delete()
            estado=True
            mensaje = "Pelicula eliminada correctamente"
        else:
            mensaje = "Metodo no permitido"
    except Exception as error:
        mensaje = str(error)
    return {"mensaje":mensaje, "estado":estado}

@app.route("/vistaAgreagrPelicula", methods=["GET"])
def vistaAgregarPelicuala():
    genero= Genero.objects()
    return render_template("frmAgregatPelicula.html", generos=genero)