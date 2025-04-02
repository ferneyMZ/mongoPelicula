from flask import Flask, render_template
from flask_mongoengine import MongoEngine


app = Flask(__name__)



@app.route("/")
def inicio():
    return render_template("contenido.html")

uri = "mongodb+srv://ferneym2003:l1rp8iL4mGaCWjj7@cluster0.kgcrm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
app.config["UPLOAD_FOLDER"] = "./static/imagenes"
app.config["MONGODB_SETTINGS"] =[ {
    "db": "GestionPeliculas",
    "host": uri
    #"port": 27017,
    
    }]
db = MongoEngine(app)

if __name__ == '__main__':
    from routes.genero import *
    from routes.pelicula import *
    from routes.usuario import *
    app.run(port=3000, host="0.0.0.0", debug=True)