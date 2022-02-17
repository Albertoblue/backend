from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
#from flask_cors import CORS, cross_origin

from config import config
from validaciones import *

app = Flask(__name__)

# CORS(app)
#CORS(app, resources={r"/*": {"origins": "http://127.0.0.1"}})

conexion = MySQL(app)


# Get a list of users
@app.route('/users', methods=['GET'])
def listar_cursos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM usuarios ORDER BY nombre ASC"
        cursor.execute(sql)
        data = cursor.fetchall()
        users = []
        for row in data:
            user = {'id':row[6],'nombre':row[0], 'apellido':row[1], 'telefono': row[2],"correo":row[3],"edad":row[4],"estado":row[5]}
            users.append(user)
        return jsonify({'users': users, 'mensaje': "Users List", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


#add a new user
@app.route('/add', methods=['POST'])
def addUser():
    print(request)
    try:
        curso =None
        if curso != None:
            return jsonify({'curso': curso, 'mensaje': "Curso encontrado.", 'exito': True})
        else:
            print("Estoy dentro del else")
            cursor = conexion.connection.cursor()
            sql = """INSERT INTO usuarios (nombre, apellido, telefono, correo, edad, estado) 
            VALUES ('{}', '{}', '{}','{}',{},'{}')""".format(request.json['nombre'],
            request.json['apellido'], request.json['telefono'],request.json['correo'],request.json['edad'],request.json['estado'])

            print(cursor.execute(sql))
            conexion.connection.commit()  # Confirma la acción de inserción.
            return jsonify({'mensaje': "Curso registrado.", 'exito': True})
           
    except Exception as ex:
        return jsonify({'mensaje': ex, 'exito': False})



#Update user
@app.route('/user/<id>', methods=['PUT'])
def updateUser(id):
        try:
            cursor = conexion.connection.cursor()
            sql = """UPDATE usuarios SET nombre = '{}', apellido = '{}',telefono='{}',correo='{}',edad={}, estado='{}' 
            WHERE id = '{}'""".format(request.json['nombre'],request.json['apellido'],request.json['telefono'],request.json['correo'],request.json['edad'],request.json['estado'],id )
            print(cursor.execute(sql))
            conexion.connection.commit()  # Confirma la acción de actualización.
            return jsonify({'mensaje': "User Update", 'exito': True})
    
        except Exception as ex:
            return jsonify({'mensaje': ex, 'exito': False})
    
    

#Delete user
@app.route('/delete/<id>', methods=['DELETE'])
def deleteUSer(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM usuarios WHERE id = '{}'".format(id)
        cursor.execute(sql)
        conexion.connection.commit()  
        return jsonify({'mensaje': "deleted user.", 'exito': True})

    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
