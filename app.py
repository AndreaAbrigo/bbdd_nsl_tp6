# -*- coding: utf-8 -*-
import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

app = Flask(__name__)

# client = MongoClient(
#     os.environ['DB_PORT_27017_TCP_ADDR'],
#     27017)
# db = client.tododb

def connect_db():
    # conexion = MongoClient('localhost')
    conexion = MongoClient(
    os.environ['DB_PORT_27017_TCP_ADDR'],
    27017)
    return conexion

def seleccionarBaseDeDatos():
    conexion=connect_db()
    db = conexion.personajes
    return db

@app.route('/prueba')
def prueba():
    conexion=connect_db()
    db = conexion.personajes
    collection = db.person
    #collection.drop()
    return "hecho"

@app.route('/')
def todo():
    conexion=connect_db()
    db = seleccionarBaseDeDatos()
    collection = db.person
    resultado=collection.find()
    return render_template('todo.html', datos=resultado)
    # _items = db.tododb.find()
    # items = [item for item in _items]

    # return render_template('todo.html', items=items)

@app.route('/nuevoPersonaje')
def nuevoPersonaje():
    return render_template("cargarPersonaje.html")
    
@app.route('/altaPersonaje', methods=["POST"])
def altaPersonaje():
    conexion=connect_db()
    db = seleccionarBaseDeDatos()
    collection = db.person
    if request.method == 'POST':
        name = request.form['name']
        character = request.form['character']
        house = request.form['house']
        biography = request.form['biography']
        year = request.form['year']
        equipment = request.form['equipment']
        img1 =request.form['img1']
        img2 =request.form['img2']
        img3 =request.form['img3']
        img4 =request.form['img4']
    images=[]
    if img1 != "":
        images.append(img1)
    if img2 != "":
        images.append(img2)
    if img2 != "":
        images.append(img3)
    if img4 != "":
        images.append(img4)        
    collection.insert({
        "name":name, 
        "character":character,
        "house":house,
        "biography": biography,
        "year": year,
        "equipment": equipment,
        "images": images
        })
    resultado=collection.find({'name':name})
    return render_template('confirmacionAlta.html', datos=resultado)

@app.route('/verinfo', methods=["POST"])
def verinfo():
    conexion=connect_db()
    db = seleccionarBaseDeDatos()
    collection = db.person
    if request.method == 'POST':
        name = request.form['name']
    resultado=collection.find({'name':name})
    return render_template('mostrarInformacion.html', datos=resultado)

@app.route('/eliminar', methods=["POST"])
def eliminar():
    if request.method == 'POST':
        name = request.form['name']
    return render_template('confirmarEliminacion.html', nombre=name)

@app.route('/siEliminar', methods=["POST"])
def siEliminar():
    conexion=connect_db()
    db = seleccionarBaseDeDatos()
    collection = db.person
    if request.method == 'POST':
        name = request.form['name']
    resultado=collection.remove({'name':name})
    return render_template('eliminado.html', nombre=name)

@app.route('/editar', methods=["POST"])
def editar():
    if request.method == 'POST':
        name = request.form['name']
    return render_template('editar.html', nombre=name)

@app.route('/modificar', methods=["POST"])
def modificar():
    conexion=connect_db()
    db = seleccionarBaseDeDatos()
    collection = db.person
    if request.method == 'POST':
        name = request.form['name']
        nuevoName = request.form['nuevoName']
        nuevoCharacter = request.form['nuevoCharacter']
        nuevoHouse = request.form['nuevoHouse']
        nuevoBiography = request.form['nuevoBiography']
        nuevoYear = request.form['nuevoYear']
        nuevoEquipment = request.form['nuevoEquipment']
        nuevoImg1 =request.form['nuevoImg1']
        nuevoImg2 =request.form['nuevoImg2']
        nuevoImg3 =request.form['nuevoImg3']
        nuevoImg4 =request.form['nuevoImg4']
    
    if nuevoCharacter != "":
        resultado=collection.update({'name':name},{'$set':{'character':nuevoCharacter}})
    if nuevoHouse != "":
        resultado=collection.update({'name':name},{'$set':{'house':nuevoHouse}})
    if nuevoBiography != "":
        resultado=collection.update({'name':name},{'$set':{'biography':nuevoBiography}})
    if nuevoYear != "":
        resultado=collection.update({'name':name},{'$set':{'year':nuevoYear}})
    if nuevoEquipment != "":
        resultado=collection.update({'name':name},{'$set':{'equipment':nuevoEquipment}})
    resultado=collection.find({'name':name})
    im={}
    im[0]=""
    im[1]=""
    im[2]=""
    im[3]=""
    c=0
    for e in resultado:
        for i in e['images']:
            im[c]=i
            c=c+1
    if nuevoImg1 != "" and im[0] != "":
        print("Entro en 1")
        resultado=collection.update({'name':name, 'images':im[0]},{'$set':{'images.$':nuevoImg1}})
    if nuevoImg1 != "" and im[0] == "":
        print("Entro en 2")
        resultado=collection.update({'name':name},{'$push':{'images':nuevoImg1}})
    if nuevoImg2 != "" and im[1] != "":
        print("Entro en 3")
        resultado=collection.update({'name':name, 'images':im[1]},{'$set':{'images.$':nuevoImg2}})
    if nuevoImg2 != "" and im[1] == "":
        print("Entro en 4")
        resultado=collection.update({'name':name},{'$push':{'images':nuevoImg2}})
    if nuevoImg3 != "" and im[2] != "":
        print("Entro en 5")
        resultado=collection.update({'name':name, 'images':im[2]},{'$set':{'images.$':nuevoImg3}})
    if nuevoImg1 != "" and im[2] == "":
        print("Entro en 6")
        resultado=collection.update({'name':name},{'$push':{'images':nuevoImg3}})
    if nuevoImg4 != "" and im[3] != "":
        print("Entro en 7")
        resultado=collection.update({'name':name, 'images':im[3]},{'$set':{'images.$':nuevoImg4}})
    if nuevoImg4 != "" and im[3] == "":
        print("Entro en 8")
        resultado=collection.update({'name':name},{'$push':{'images':nuevoImg4}})
    if nuevoName != "":
        resultado=collection.update({'name':name},{'$set':{'name':nuevoName}})
        
    if nuevoName == "":
        resultado=collection.find({'name':name})
        return render_template('confirmacionModificacion.html', datos=resultado)
    else:
        resultado=collection.find({'name':nuevoName})
        return render_template('confirmacionModificacion.html', datos=resultado)

@app.route('/casaMarvel')
def casaMarvel():
    conexion=connect_db()
    db = seleccionarBaseDeDatos()
    collection = db.person
    resultado=collection.find({'house':"MARVEL"})
    return render_template('marvel.html', datos=resultado)

@app.route('/casaDC')
def casaDC():
    conexion=connect_db()
    db = seleccionarBaseDeDatos()
    collection = db.person
    resultado=collection.find({'house':"DC"})
    return render_template('dc.html', datos=resultado)

@app.route('/buscar', methods=["POST"])
def buscar():
    conexion=connect_db()
    db = seleccionarBaseDeDatos()
    collection = db.person
    if request.method == 'POST':
        palabra = request.form['palabra']
    resultado=collection.find({'name':{'$regex':palabra}})
    return render_template('index.html', datos=resultado)

@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'name': request.form['name'],
        'description': request.form['description']
    }
    db.tododb.insert_one(item_doc)

    return redirect(url_for('todo'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)