from app import app
from flask import request
from flask import render_template
from models.genero import Genero
from models.pelicula import Pelicula

@app.route("/genero/", methods=['GET'])
def listarGenero():
    try:
        mensaje=""
        generos=Genero.objects()
    except Exception as error:
        mensaje = str(error)
    return render_template("listarGeneros.htnl",
            generos=generos,mensaje=mensaje)


@app.route("/genero/", methods=["POST"])
def addGenero():
    
    try:
        mensaje=None
        estado = False
        
        if request.method == "POST":
            datos = request.get_json(force=True)
            genero = Genero(**datos)
            genero.save()
            estado = True
            mensaje = "Genero guardado correctamente"
        else:
            mensaje = "Metodo no permitido"
        
    except Exception as error:
        mensaje = str(error)
        
    return {"estado":estado, "mensaje":mensaje}

@app.route("/genero/", methods=["PUT"])
def updateGenero():
        
        try:
            mensaje=None
            estado = False
            
            if request.method == "PUT":
                datos = request.get_json(force=True)
                genero = Genero.objects(id=datos["id"]).first()
                genero.nombre = datos["nombre"]
                genero.save()
                mensaje = "Genero actualizado correctamente"
                estado = True
            else:
                mensaje = "Metodo no permitido"
        
            
        except Exception as error:
            mensaje = str(error)
            
        return {"estado":estado, "mensaje":mensaje}
    
@app.route("/genero/", methods=["DELETE"])
def deleteGenero():
        
        try:
            mensaje=None
            estado = False
            
            if request.method == "DELETE":
                datos = request.get_json(force=True)
                genero = Genero.objects(id=datos["id"]).first()
                peliculas = Pelicula.objects(genero=genero)
                if len(peliculas)>0:
                    mensaje = "Genero no se puede eliminar porque tiene peliculas asociadas"
                
                if genero is None:
                    mensaje = "Genero no existe"
                else:
                    genero.delete()
                    mensaje = "Genero eliminado correctamente"
                    estado = True
            else:
                mensaje = "Metodo no permitido"
        
            
        except Exception as error:
            mensaje = str(error)
            
        return {"estado":estado, "mensaje":mensaje}
    
