from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///refugios.db'
db = SQLAlchemy(app)

# Definición de los modelos de la base de datos
# Define las clases de modelo de la base de datos utilizando SQLAlchemy.
# La clase Refugio representa un refugio de animales y la clase Animal representa un animal en un refugio.
# Estas clases definen las columnas y relaciones de la base de datos.

class Refugio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    direccion = db.Column(db.String(100))
    descripcion = db.Column(db.String(240))
    contacto = db.Column(db.String(200))
    animales = db.relationship('Animal', backref='refugio', lazy=True)

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    especie = db.Column(db.String(50))
    sexo = db.Column(db.String(50))
    raza = db.Column(db.String(50))
    edad = db.Column(db.Integer)
    descripcion = db.Column(db.String(240))
    refugio_id = db.Column(db.Integer, db.ForeignKey('refugio.id'))

# with app.app_context():
#     db.create_all()

# Rutas de la aplicación web
# Define la ruta principal de la aplicación (/). 
# Al acceder a esta ruta, se obtienen todos los refugios de la base de datos y 
# se pasa la lista de refugios a la plantilla inicio.html para su visualización.
@app.route('/')
def inicio():
    refugios = Refugio.query.all()
    return render_template('inicio.html', refugios=refugios)
# Define la ruta /refugios/nuevo que maneja las solicitudes GET y POST.
# Si la solicitud es POST, se obtienen los datos del formulario enviado por el usuario 
# y se crea un nuevo objeto Refugio en la base de datos. Luego, se redirige al usuario a la ruta principal (/).
# Si la solicitud es GET, se muestra la plantilla nuevo_refugio.html para que el usuario ingrese los datos del nuevo 
# refugio.

@app.route('/refugios/nuevo', methods=['GET', 'POST'])
def nuevo_refugio():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        contacto = request.form['contacto']
        descripcion = request.form['descripcion']
        nuevo_refugio = Refugio(nombre=nombre, direccion=direccion, descripcion=descripcion, contacto=contacto)
        db.session.add(nuevo_refugio)
        db.session.commit()
        return redirect('/')
    return render_template('datos_refugio.html')

@app.route('/refugios')
def lista_refugio():
    animales = Animal.query.all()
    return render_template('lista_refugios.html', animales=animales)

# Define la ruta /refugios/<int:refugio_id>/animales que maneja las solicitudes GET y POST. 
# En función del refugio_id proporcionado en la URL, se obtiene el refugio correspondiente de la base de datos. 
# Si la solicitud es POST, se obtienen los datos del formulario enviado por el usuario y se crea un nuevo objeto Animal 
# asociado a ese refugio en la base de datos. Luego, se muestra la plantilla animales.html con la información del refugio y la lista de animales asociados a él. 
# Si la solicitud es GET, simplemente se muestra la plantilla animales.html 
# con la información del refugio y la lista de animales

@app.route('/refugios/animales', methods=['GET', 'POST'])
def animales():
    if request.method == 'POST':
        nombre = request.form['nombre']
        sexo = request.form['sexo']
        especie = request.form['especie']
        raza = request.form['raza']
        edad = request.form['edad']
        descripcion = request.form['descripcion']        
        nuevo_animal = Animal(nombre=nombre, sexo=sexo, especie=especie, raza=raza, edad=edad, descripcion=descripcion)
        db.session.add(nuevo_animal)
        db.session.commit()
        return redirect('/animales')
    animales = Animal.query.all()
    return render_template('datos_animal.html', animales=animales)

@app.route('/animales')
def lista_animales():
    animales = Animal.query.all()
    return render_template('lista_animales.html', animales=animales)


@app.route('/infoAnimales')
def datos_animales():
    animales = Animal.query.all()
    return render_template('infoAnimales.html', animales=animales)


#Define la ruta /animales/<int:animal_id>/apadrinar que maneja las solicitudes POST. 
# Esta ruta es utilizada para realizar alguna acción relacionada con apadrinar un animal. 
# En este caso, simplemente se redirige al usuario a la ruta principal (/).

@app.route('/animales/<int:animal_id>/apadrinar', methods=['POST', 'GET'])
def apadrinar(animal_id):
    animal = Animal.query.filter_by(id=animal_id).first()
    return render_template('form_apadri.html', animal=animal)

# Punto de entrada de la aplicación
# Si el módulo actual es el punto de entrada de la aplicación, se crea la estructura de la 
# base de datos utilizando db.create_all() y se inicia la aplicación en modo de depuración (app.run(debug=True))
if __name__ == '__main__':
    
    app.run(debug=True)
