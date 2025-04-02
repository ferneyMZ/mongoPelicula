from mongoengine import Document, StringField

class Usuario(Document):
    usuario = StringField(max_length=50, unique=True, required=True)
    password = StringField(required=True)
    nombre_completo = StringField(max_length=100, required=True)
    correo_electronico = StringField(required=True, regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    
    def __repr__(self):
        return f"Usuario({self.usuario})"

# Ejemplo de cómo crear un usuario
def crear_usuario():
    nuevo_usuario = Usuario(
        usuario="muñoz",
        password="0000",
        nombre_completo="ferney muñoz",
        correo_electronico="ferneym@gmail.com"
    )
    nuevo_usuario.save()
    print("Usuario guardado correctamente")
