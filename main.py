#MÓDULOS
import os, binascii
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from sqlite3 import Error
import pickle

ADeNTRO = bool(False)
TOkEN = None
SECREToS = None
ASaP = int(0)

def cargar():
    if os.path.exists('txt.txt') == True:
        global ADeNTRO
        global TOkEN
        entrada = open('txt.txt', 'rb')
        variados = pickle.load(entrada)
        entrada.close()
        if (variados == []):
            ADeNTRO = bool(False)
            TOkEN = None
        else:
            ADeNTRO = variados[0]
            TOkEN = variados[1]
cargar()

def guardar(a):
    salida = open('txt.txt', 'wb')
    pickle.dump(a, salida)
    salida.close()

#BASE DE DATOS

#CONEXIÓN
def sqlConexion(archivo_bd):
    conexion = None
    try:
        conexion = sqlite3.connect(archivo_bd)
        return conexion
    except Error as e:
        print(f"ERROR: {e}")
    return conexion

#TABLA USUARIO
#CREACIÓN DE TABLA "USUARIO" E INSERCIÓN
def crear_tabla_usuario(conexion, crear_tabla_sql):
    try:
        objeto_cursor = conexion.cursor()
        objeto_cursor.execute(crear_tabla_sql)
    except Error as e:
        print(f"ERROR: {e}")
def insertar_datos_usuario(conexion, datos, tabla):
    sql = f'''
            INSERT INTO {tabla}(correo, nombre, contrasena) VALUES(?,?,?)
    '''
    objeto_cursor = conexion.cursor()
    objeto_cursor.execute(sql, datos)
    conexion.commit()
def BasesDatosInsercionUsuario(correo, nombre, contrasena):
    basedato = "DATOS.db"

    sql_crear_tabla_usuario = """
                                    CREATE TABLE IF NOT EXISTS usuario (
                                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                        correo TEXT NOT NULL UNIQUE,
                                        nombre TEXT NOT NULL,
                                        contrasena TEXT NOT NULL
                                    );
    """
    conexion = sqlConexion(basedato)
    if conexion is not None:
        crear_tabla_usuario(conexion, sql_crear_tabla_usuario)
    else:
        print("ERROR")
        return "ERROR"
    with conexion:
        datos = (correo, nombre, contrasena)
        try:
            insertar_datos_usuario(conexion, datos, "usuario")
        except Error as e:
            print(f"ERROR: {e}")
            return "ERROR"

#INICIO DE SESIÓN
def seleccionar_datos_usuario(conexion, datos, tabla):
    sql = f'''
            SELECT correo, contrasena FROM {tabla} WHERE correo = ? AND contrasena = ?
    '''
    objeto_cursor = conexion.cursor()
    objeto_cursor.execute(sql, datos)
    registro = objeto_cursor.fetchall()
    conexion.commit()
    return registro
def BasesDatosInicioSesion(correo, contrasena):
    basedato = "DATOS.db"
    conexion = sqlConexion(basedato)
    with conexion:
        datos = (correo, contrasena)
        try:
            registro = seleccionar_datos_usuario(conexion, datos, "usuario")
            if (registro != []):
                return 1
            else:
                return 0
        except Error as e:
            print(f"ERROR: {e}")
            return "ERROR"

#MODIFICACIÓN DE DATOS
def actualizar_datos_usuario(conexion, datos, tabla, columna, token):
    if (columna == "correo"):
        sql = f'''
                UPDATE {tabla} SET correo = ? WHERE correo = ?
        '''
        TOkEN[1] = datos[0]
    elif (columna == "nombre"):
        sql = f'''
                UPDATE {tabla} SET nombre = ? WHERE correo = ?
                '''
    elif (columna == "contrasena"):
        if (token != None):
            sql = f'''
                    UPDATE {tabla} SET contrasena = ? WHERE correo = ?
                    '''
        else:
            pass
    else:
        pass
    objeto_cursor = conexion.cursor()
    objeto_cursor.execute(sql, datos)
    conexion.commit()
def BasesDatosModificacionUsuario(dato, columna, token):
    basedato = "DATOS.db"
    conexion = sqlConexion(basedato)
    with conexion:
        datos = (dato, TOkEN[1])
        try:
            actualizar_datos_usuario(conexion, datos, "usuario", columna, token)
            return None
        except Error as e:
            print(f"ERROR: {e}")
            return "ERROR"

#TABLA SECRETO
#CREACIÓN DE TABLA "SECRETO" E INSERCIÓN
def crear_tabla_secreto(conexion, crear_tabla_sql):
    try:
        objeto_cursor = conexion.cursor()
        objeto_cursor.execute(crear_tabla_sql)
    except Error as e:
        print(f"ERROR: {e}")
def insertar_datos_secreto(conexion, datos, tabla):
    sql = f'''
            INSERT INTO {tabla}(titulo, descripcion, valor, fecha, lugar, latitud, longitud, id_usuario) VALUES(?,?,?,?,?,?,?,?)
    '''
    objeto_cursor = conexion.cursor()
    objeto_cursor.execute(sql, datos)
    conexion.commit()
def BasesDatosInsercionSecreto(titulo, descripcion, valor, fecha, lugar, latitud, longitud, id_usuario):
    basedato = "DATOS.db"

    sql_crear_tabla_secreto = """
                                    CREATE TABLE IF NOT EXISTS secreto (
                                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                        titulo TEXT NOT NULL UNIQUE,
                                        descripcion TEXT NOT NULL,
                                        valor TEXT NOT NULL,
                                        fecha TEXT NOT NULL,
                                        lugar TEXT NOT NULL,
                                        latitud TEXT NOT NULL,
                                        longitud TEXT NOT NULL,
                                        id_usuario INTEGER NOT NULL
                                    );
    """
    conexion = sqlConexion(basedato)
    if conexion is not None:
        crear_tabla_secreto(conexion, sql_crear_tabla_secreto)
    else:
        print("ERROR")
        return "ERROR"
    with conexion:
        datos = (titulo, descripcion, valor, fecha, lugar, latitud, longitud, id_usuario)
        try:
            insertar_datos_secreto(conexion, datos, "secreto")
        except Error as e:
            print(f"ERROR: {e}")
            return "ERROR"
#ELIMINACIÓN DE DATOS
def eliminar_datos_secreto(conexion, dato, tabla):
    try:
        sql = f'''
                DELETE FROM {tabla} WHERE id = ?
        '''
        objeto_cursor = conexion.cursor()
        objeto_cursor.execute(sql, dato)
        conexion.commit()
        return 1
    except Error:
        return 0
def BasesDatosEliminacionSecreto(id):
    basedato = "DATOS.db"
    conexion = sqlConexion(basedato)
    with conexion:
        dato = (id)
        try:
            condicion = eliminar_datos_secreto(conexion, dato, "secreto")
            return condicion
        except Error as e:
            print(f"ERROR: {e}")
            return "ERROR"

#SELECCIONAR SECRETOS
def seleccionar_datos_secreto(conexion, dato, tabla):
    try:
        sql = f'''
                SELECT * FROM {tabla} WHERE id_usuario = '{dato}'
        '''
        objeto_cursor = conexion.cursor()
        objeto_cursor.execute(sql)
        registro = objeto_cursor.fetchall()
        conexion.commit()
        return registro
    except Error:
        return []
def BasesDatosSecretoSeleccion(id_usuario):
    global SECREToS
    basedato = "DATOS.db"
    conexion = sqlConexion(basedato)
    with conexion:
        try:
            SECREToS = seleccionar_datos_secreto(conexion, id_usuario, "secreto")
            if (SECREToS != []):
                return 1
            else:
                return 0
        except Error as e:
            print(f"ERROR: {e}")
            return "ERROR"

#-MÉTODOS
def ValidarCorreoElectronico(correo):
    correo = correo.lower()
    if ("@" in correo and ".com" in correo):
        return correo
    else:
        return "ERROR CORREO"

def getUsuarioID(a):
    basedato = "DATOS.db"
    conexion = sqlConexion(basedato)
    with conexion:
        tabla = "usuario"
        try:
            sql = f'''
                        SELECT id FROM {tabla} WHERE correo = '{a}'
                '''
            objeto_cursor = conexion.cursor()
            objeto_cursor.execute(sql)
            id_usuario = int((objeto_cursor.fetchall())[0][0])
            conexion.commit()
            return id_usuario
        except Error as e:
            print(f"ERROR: {e}")
            return "ERROR"

#CREACION DEL OBJETO APP
app = FastAPI()

#ORÍGENES DESCONOCIDOS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#POR DEFECTO
@app.get("/")
def read_root():
    if (ADeNTRO):
        return {
            "InicioSesion": ADeNTRO,
            "TokenSesion": TOkEN
        }
    else:
        return {
            "InicioSesion": ADeNTRO
        }

#1-. AGREGAR USUARIO
@app.get("/agregarUsuario/{correo},{nombre},{contrasena}")
def AgregarUsuario(correo: str, nombre: str, contrasena: str):
    if (not ADeNTRO):
        correo = ValidarCorreoElectronico(correo)
        if (correo == "ERROR CORREO"):
            return {"ERROR": f"CORREO INVÁLIDO."}
        else:
            condicion = BasesDatosInsercionUsuario(correo, nombre, contrasena)
            if (condicion == "ERROR"):
                return {"ERROR": f"ERROR EN LA BASE DE DATOS.\n{Error}"}
            else:
                return {
                    "CorreoElectronico": correo,
                    "Nombre": nombre,
                    "Contrasena": contrasena
                }
    else:
        return {
            "InicioSesion": ADeNTRO,
            "PROBELMA": "No es posible agregar usuarios si hay una sesion iniciada."
        }

#2-. INICIO SESIÓN
@app.get("/inicioSesion/{correo},{contrasena}")
def InicioSesion(correo: str, contrasena: str):
    global ADeNTRO
    global TOkEN
    if (not ADeNTRO):
        variable_retorno = BasesDatosInicioSesion(correo, contrasena)
        if (variable_retorno != "ERROR"):
            if (variable_retorno == 1):
                ADeNTRO = True
                TOkEN = [binascii.b2a_hex(os.urandom(10)), correo, contrasena]
                arreglo = [ADeNTRO, TOkEN]
                guardar(arreglo)
                return {
                    "InicioSesion": ADeNTRO,
                    "TokenSesion": TOkEN
                }
            else:
                return {
                    "InicioSesion": ADeNTRO,
                    "ERROR": "CORREO O CONTRASEÑA INCORRECTA."
                }
        else:
            return {
                "InicioSesion": ADeNTRO,
                "ERROR": f"ERROR EN LA BASE DE DATOS.\n{Error}"
            }
    else:
        return {
            "InicioSesion": ADeNTRO,
            "TokenSesion": TOkEN
        }

#3-. MODIFICAR DATOS
@app.get("/modificarDatos/correo/{correo}")
def ModificarCorreo(correo: str):
    global TOkEN
    if (ADeNTRO):
        columna = "correo"
        correo = ValidarCorreoElectronico(correo)
        if (correo != "ERROR CORREO"):
            condicion = BasesDatosModificacionUsuario(correo, columna, None)
            if (condicion != "ERROR"):
                TOkEN[1] = correo
                arreglo = [ADeNTRO, TOkEN]
                guardar(arreglo)
                return {
                    "Modificación": "¡EXITOSA!",
                    "CorreoNuevo": correo
                }
            else:
                return {"ERROR": f"ERROR EN LA BASE DE DATOS.\n{Error}"}
        else:
            return {"ERROR": f"CORREO INVÁLIDO."}
    else:
        return {"InicioSesion": ADeNTRO}
@app.get("/modificarDatos/nombre/{nombre}")
def ModificarNombre(nombre: str):
    if(ADeNTRO):
        columna = "nombre"
        variable = BasesDatosModificacionUsuario(nombre, columna, None)
        if (variable != "ERROR"):
            return {
                "Modificación": "¡EXITOSA!",
                "NombreNuevo": nombre
            }
        else:
            return {"ERROR": f"ERROR EN LA BASE DE DATOS.\n{Error}"}
    else:
        return {"InicioSesion": ADeNTRO}

#4-. CAMBIAR CLAVE
@app.get("/modificarDatos/contrasena/{contrasena}")
def ModificarContrasena(contrasena: str):
    global TOkEN
    if(ADeNTRO):
        columna = "contrasena"
        variable = BasesDatosModificacionUsuario(contrasena, columna, TOkEN[0])
        if (variable != "ERROR"):
            TOkEN[2] = contrasena
            arreglo = [ADeNTRO, TOkEN]
            guardar(arreglo)
            return {
                "Modificación": "¡EXITOSA!",
                "ContrasenaNueva": contrasena
            }
        else:
            return {"ERROR": f"ERROR EN LA BASE DE DATOS.\n{Error}"}
    else:
        return {"InicioSesion": ADeNTRO}

#5-. SECRETOS
@app.get("/secretos")
def Secretos():
    global ASaP
    if (ADeNTRO):
        id_usuario = getUsuarioID(TOkEN[1])
        condicion = BasesDatosSecretoSeleccion(id_usuario)
        if (condicion != "ERROR"):
            if (condicion == 1):
                diccionarioX = {}
                diccionarioXX = {}
                ASaP = 0
                for k in SECREToS:
                    diccionario = {
                        "ID": k[0],
                        "Titulo": k[1],
                        "Descripcion": k[2],
                        "ValorMonetario": k[3],
                        "Fecha": k[4],
                        "Lugar": k[5],
                        "Latitud": k[6],
                        "Longitud": k[7]
                    }
                    diccionarioX.update({f"Secreto{ASaP}": diccionario})
                    ASaP += 1
                diccionarioXX = {
                    "SECRETOS": diccionarioX
                }
                return diccionarioXX
            elif (condicion == 0):
                return {
                    "Secretos": False
                }
            else:
                pass
        else:
            return {"ERROR": f"ERROR EN LA BASE DE DATOS.\n{Error}"}
    else:
        return {"InicioSesion": ADeNTRO}

#6-. ELIMINAR SECRETO
@app.get("/eliminarSecreto/{id}")
def EliminarSecreto(id: str):
    if (ADeNTRO):
        condicion = BasesDatosEliminacionSecreto(id)
        if (condicion != "ERROR"):
            if (condicion == 1):
                return{
                    f"Secreto": f"¡EL SECRETO ID-.{id}: FUE ELIMINADO!"
                }
            else:
                return {"Secreto": "EL SECRETO NO EXISTE EN LA BASE DE DATOS."}
        else:
            return {"ERROR": f"ERROR EN LA BASE DE DATOS.\n{Error}"}
    else:
        return {"InicioSesion": ADeNTRO}

#7-. REGISTRAR SECRETO
@app.get("/registrarSecreto/{titulo},{descripcion},{valor},{fecha},{lugar},{latitud},{longitud}")
def RegistrarSecreto(titulo: str, descripcion: str, valor: str, fecha: str, lugar: str, latitud: float, longitud: float):
    if(ADeNTRO):
        id_usuario = getUsuarioID(TOkEN[1])
        condicion = BasesDatosInsercionSecreto(titulo, descripcion, valor, fecha, lugar, latitud, longitud, id_usuario)
        if (condicion != "ERROR"):
            return {
                "Titulo": titulo,
                "Descripcion": descripcion,
                "ValorMonetario": valor,
                "Fecha": fecha,
                "Lugar": lugar,
                "Latitud": latitud,
                "Longitud": longitud
            }
        else:
            return {"ERROR": f"ERROR EN LA BASE DE DATOS.\n{Error}"}
    else:
        return {"InicioSesion": ADeNTRO}

#8-. CERRAR SESIÓN
@app.get("/cerrarSesion")
def CerrarSesion():
    global ADeNTRO
    global TOkEN
    global SECREToS
    if (ADeNTRO):
        ADeNTRO = False
        TOkEN = None
        SECREToS = None
        arreglo = [ADeNTRO, TOkEN]
        guardar(arreglo)
        return {
            "SesionCerrada": True
        }
    else:
        return {
            "InicioSesion": ADeNTRO
        }