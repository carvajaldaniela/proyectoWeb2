from datetime import datetime
import random
from pymongo import MongoClient
from bson.objectid import ObjectId
import requests

conex = MongoClient(host=['127.0.0.1:27017'])
db = conex.apiData_02

from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS

# Crear la aplicación Flask
app = Flask(__name__)
CORS(app)

# valida la firma digital usando una API externa
def validar_firma_digital(firma_digital, id_contribuyente):
    url_api_externa = 'https://apiexterna.com/validar_firma'  # URL de la API externa
    payload = {'firma_digital': firma_digital, 'id_contribuyente': id_contribuyente}
    try:
        response = requests.post(url_api_externa, json=payload)
        response.raise_for_status()  # tira excepcion para errores
        resultado = response.json()
        return resultado.get('valido', False)
    except requests.RequestException as e:
        print(f'Error al validar firma digital: {e}')
        return False

# registrar un nuevo contribuyente
@app.route('/contribuyente', methods=['POST'])
def registrar_contribuyente():
    if not request.json or not all(k in request.json for k in ('nombre', 'tipo', 'numero_id', 'direccion', 'correo_electronico', 'firma_digital')):
        abort(400)
    
    firma_digital = request.json['firma_digital']
    numero_id = request.json['numero_id']
    
    if not validar_firma_digital(firma_digital, numero_id):
        return jsonify({'estado': 'Firma digital inválida'}), 400
    
    contribuyente = {
        'nombre': request.json['nombre'],
        'tipo': request.json['tipo'],
        'numero_id': request.json['numero_id'],
        'direccion': request.json['direccion'],
        'correo_electronico': request.json['correo_electronico'],
        'firma_digital': request.json['firma_digital']
    }
    
    try:
        db.contribuyentes.insert_one(contribuyente)
        return jsonify({'estado': 'Contribuyente registrado exitosamente'}), 201
    except:
        abort(500)

# modificar los datos de un contribuyente
@app.route('/contribuyente/<string:id>', methods=['PUT'])
def modificar_contribuyente(id):
    if not request.json:
        abort(400)
    try:
        contribuyente = db.contribuyentes.find_one({"_id": ObjectId(id)})
        if not contribuyente:
            abort(404)
        db.contribuyentes.update_one({'_id': ObjectId(id)}, {'$set': request.json})
        return jsonify({'estado': 'Datos del contribuyente actualizados exitosamente'})
    except:
        abort(500)

# eliminar a un contribuyente
@app.route('/contribuyente/<string:id>', methods=['DELETE'])
def dar_baja_contribuyente(id):
    try:
        contribuyente = db.contribuyentes.find_one({"_id": ObjectId(id)})
        if not contribuyente:
            abort(404)
        db.contribuyentes.delete_one({'_id': ObjectId(id)})
        return jsonify({'estado': 'Contribuyente dado de baja exitosamente'})
    except:
        abort(500)

# verificar una factura
@app.route('/factura', methods=['POST'])
def emitir_factura():
    if not request.json or not all(k in request.json for k in ('id_contribuyente', 'numero_factura', 'fecha', 'items', 'monto_total', 'firma_digital')):
        abort(400)
    
    factura = {
        'id_contribuyente': request.json['id_contribuyente'],
        'numero_factura': request.json['numero_factura'],
        'fecha': request.json['fecha'],
        'items': request.json['items'],
        'monto_total': request.json['monto_total'],
        'firma_digital': request.json['firma_digital']
    }
    
    try:
        contribuyente = db.contribuyentes.find_one({"_id": ObjectId(factura['id_contribuyente'])})
        if not contribuyente:
            abort(404)
        if not validar_firma_digital(factura['firma_digital'], contribuyente['numero_id']):
            return jsonify({'estado': 'Firma digital inválida'}), 400
        db.facturas.insert_one(factura)
        return jsonify({'estado': 'Factura emitida exitosamente', 'factura_id': str(factura['_id'])}), 201
    except:
        abort(500)

# flask
if __name__ == '__main__':
    app.run(debug=True)
