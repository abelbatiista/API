#IMPORTACIONES: MÓDULOS Y LIBRERÍAS
import os, binascii
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import pickle
import datetime

#GLOBALES
LoGGEDIN = bool(False)
TOkEN = None
ASaP = int(0)

#EXTRAS
def load():

    if (os.path.exists('LoGGEDIN.txt')):
        global LoGGEDIN
        global TOkEN
        _in = open('LoGGEDIN.txt', 'rb')
        _variable = pickle.load(_in)
        _in.close()
        if (_variable == []):
            LoGGEDIN = bool(False)
            TOkEN = None
        else:
            LoGGEDIN = _variable[0]
            TOkEN = _variable[1]
load()

def save(a):
    _out = open('LoGGEDIN.txt', 'wb')
    pickle.dump(a, _out)
    _out.close()

#CREACIÓN DE LA BASE DE DATOS MySQL
def CreateDataBase():
    try:
        databases = []
        myDB = mysql.connector.connect(host="localhost", user="root", password="ABel06032001")
        myCursor = myDB.cursor()
        myCursor.execute("SHOW DATABASES")
        for k in myCursor:
            databases.append(k)
        myCursor.execute("CREATE DATABASE IF NOT EXISTS WebFinalDatos")
    except:
        print("ERROR")
CreateDataBase()

#CREACIÓN DE LA CONEXIÓN EN LA BASE DE DATOS
def Connection():
    try:
        myDB = mysql.connector.connect(host="localhost", user="root", password="ABel06032001", database="webfinaldatos")
        return myDB
    except:
        print("ERROR")

#TABLA DOCTOR

#CREACIÓN DE LA TABLA "doctor"
def CreateDoctorTable():
    try:
        connection = Connection()
        myCursor = connection.cursor()
        sql = """
                            CREATE TABLE IF NOT EXISTS doctor(
                                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                username VARCHAR(100) NOT NULL,
                                email VARCHAR(200) NOT NULL,
                                password VARCHAR(200) NOT NULL,
                                CONSTRAINT CONST_UNIQUE_DOCTOR UNIQUE (username, email)                          
                            );
        """
        myCursor.execute(sql)
    except:
        print("ERROR")
CreateDoctorTable()

#REGITRAR DATOS, INSERCIÓN
def InsertSignUpDoctor(username, email, password):
    try:
        connection = Connection()
        myCursor = connection.cursor()
        sql = """INSERT INTO doctor (username, email, password) VALUES (%s, %s, %s)"""
        values = (username, email, password)
        myCursor.execute(sql, values)
        connection.commit()
        return 1
    except:
        return 0

#SELECCIONAR DATOS INICIO DE SESIÓN.
def SelectLogInDoctor(email, password):
    try:
        connection = Connection()
        myCursor = connection.cursor()
        sql = f"""SELECT * FROM doctor WHERE email = %s AND password = %s"""
        values = (email, password)
        myCursor.execute(sql, values)
        myResult = myCursor.fetchone()
        myResult = list(myResult)
        if (myResult != None):
            return [True, myResult]
        else:
            return False
    except:
        return 0

#MODIFICAR DATOS TABLA DOCTOR
def UpdateDoctor(column, value, id):
    try:
        connection = Connection()
        myCursor = connection.cursor()
        sql = f"""UPDATE doctor SET {column} = '{value}' WHERE id = {id}"""
        myCursor.execute(sql)
        connection.commit()
        return 1
    except:
        return 0

#TABLA PACIENTE

#CREACIÓN DE LA TABLA "paciente"
def CreatePatientTable():
    try:
        connection = Connection()
        myCursor = connection.cursor()
        sql = """
                            CREATE TABLE IF NOT EXISTS patient (
                                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                iddoctor INT NOT NULL,
                                cedula VARCHAR(100) NOT NULL,
                                image LONGBLOB NOT NULL,
                                name VARCHAR(100) NOT NULL,
                                lastname VARCHAR(100) NOT NULL,
                                bloodtype VARCHAR(100) NOT NULL,
                                email VARCHAR(200) NOT NULL,
                                sex VARCHAR(100) NOT NULL,
                                birthdate DATE NOT NULL,
                                allergies VARCHAR(200) NOT NULL,
                                CONSTRAINT CONST_UNIQUE_DOCTOR UNIQUE (cedula, email),
                                FOREIGN KEY (iddoctor) REFERENCES doctor(id)                     
                            );
        """
        myCursor.execute(sql)
    except:
        print("ERROR")
CreatePatientTable()

#INSERCIÓN
def InsertPatient(cedula, image, name, lastname, bloodtype, email, sex, birthdate, allergies, iddoctor):
    try:
        connection = Connection()
        myCursor = connection.cursor()
        sql = """INSERT INTO patient (cedula, image, name, lastname, bloodtype, email, sex, birthdate, allergies, iddoctor) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (cedula, image, name, lastname, bloodtype, email, sex, birthdate, allergies, iddoctor)
        myCursor.execute(sql, values)
        connection.commit()
        id = myCursor.lastrowid
        return [1, id]
    except:
        return [0]

#ACTUALIZACIÓN
def UpdatePatient(id, cedula, image, name, lastname, bloodtype, email, sex, birthdate, allergies, iddoctor):
    try:
        connection = Connection()
        myCursor = connection.cursor()
        sql = """UPDATE patient SET cedula = %s, image = %s, name = %s, lastname = %s, bloodtype = %s, email = %s, sex = %s, birthdate = %s, allergies = %s, iddoctor = %s WHERE id = %s"""
        values = (cedula, image, name, lastname, bloodtype, email, sex, birthdate, allergies, iddoctor, id)
        myCursor.execute(sql, values)
        connection.commit()
        return 1
    except:
        return 0

#ELIMINACIÓN
def DeletePatient(id):
    try:
        connection = Connection()
        myCursor = connection.cursor()
        sql = f"""DELETE FROM patient WHERE id = {id}"""
        myCursor.execute(sql)
        connection.commit()
        return 1
    except:
        return 0

#SELECCIÓN
def SelectPatient(id, iddoctor):
    try:
        connection = Connection()
        myCursor = connection.cursor()
        sql = f"""SELECT * FROM patient WHERE id = {id} AND iddoctor = {iddoctor}"""
        myCursor.execute(sql)
        myResult = myCursor.fetchone()
        return [1, myResult]
    except:
        return [0]

#SELECCIÓN NOMBRE PACIENTES
def SelectPatientsName(iddoctor):
    try:
        connection = Connection()
        myCursor = connection.cursor()
        sql = f"""SELECT name FROM patient WHERE iddoctor = {iddoctor}"""
        myCursor.execute(sql)
        myResult = myCursor.fetchall()
        return [1, myResult]
    except:
        return 0

#BUSCAR ID DEL PACIENTE
def SearchPatientID(name, iddoctor):
    try:
        connection = Connection()
        myCursor = connection.cursor()
        sql = f"""SELECT id FROM patient WHERE name = '{name}' AND iddoctor = {iddoctor}"""
        myCursor.execute(sql)
        myResult = myCursor.fetchone()
        myResult = myResult[0]
        return [1, myResult]
    except:
        return [0]

#TABLA VISITA

#CREACIÓN DE LA TABLA "visita"
def CreateConsultTable():
    try:
        connection = Connection()
        myCursor = connection.cursor()
        sql = """
                            CREATE TABLE IF NOT EXISTS consult (
                                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                idpatient INT NOT NULL,
                                date DATE NOT NULL,
                                consultreason VARCHAR(200) NOT NULL,
                                securitynumber VARCHAR(100) NOT NULL,
                                amount DECIMAL(13,2) NOT NULL,
                                diagnosis VARCHAR(100) NOT NULL,
                                note VARCHAR(200) NOT NULL,
                                image LONGBLOB,
                                FOREIGN KEY (idpatient) REFERENCES patient(id)                    
                            );
        """
        myCursor.execute(sql)
    except:
        print("Error")
CreateConsultTable()

#INSERCIÓN
def InsertConsult(idpatient, date, consultreason, securitynumber, amount, diagnosis, note, image):
    try:
        connection = Connection()
        myCursor = connection.cursor()
        sql = """INSERT INTO consult (idpatient, date, consultreason, securitynumber, amount, diagnosis, note, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (idpatient, date, consultreason, securitynumber, amount, diagnosis, note, image)
        myCursor.execute(sql, values)
        connection.commit()
        id = myCursor.lastrowid
        return [1, id]
    except:
        return [0]

#ACTUALIZACIÓN
def UpdateConsult(id, idpatient, date, consultreason, securitynumber, amount, diagnosis, note, image):
    try:
        connection = Connection()
        myCursor = connection.cursor()
        sql = """UPDATE consult SET idpatient = %s, date = %s, consultreason = %s, securitynumber = %s, amount = %s, diagnosis = %s, note = %s, image = %s WHERE id = %s"""
        values = (idpatient, date, consultreason, securitynumber, amount, diagnosis, note, image, id)
        myCursor.execute(sql, values)
        connection.commit()
        return 1
    except:
        return 0

#ELIMINACIÓN
def DeleteConsult(id):
    try:
        connection = Connection()
        myCursor = connection.cursor()
        sql = f"""DELETE FROM consult WHERE id = {id}"""
        myCursor.execute(sql)
        connection.commit()
        return 1
    except:
        return 0

#SELECCIÓN
def SelectConsult(id, iddoctor):
    try:
        connection = Connection()
        myCursor = connection.cursor()
        sql = f"""
                SELECT * FROM consult c
                INNER JOIN patient p
                ON p.id = c.idpatient
                INNER JOIN doctor d
                ON d.id = p.iddoctor
                WHERE d.id = {iddoctor}
                AND c.id = {id}
        """
        myCursor.execute(sql)
        myResult = myCursor.fetchone()
        return [1, myResult]
    except:
        return [0]

#MÉTODOS ESPECIALES

#ZODIACAL
def getZodiacalSign(date):
    sign = ['capricornio', 'acuario', 'piscis', 'aries', 'tauro', 'geminis', 'cancer', 'leo', 'virgo', 'libra', 'escorpio', 'sagitario']
    dates = [20, 19, 20, 20, 21, 21, 22, 22, 22, 22, 22, 21]
    day = int(date[8:10])
    month = (int(date[5:7])) - 1
    if day > dates[month]:
        month += 1
        if month == 12:
            month = 0
    return sign[month].upper()

#SELECCIÓN DE TABLAS
def SELECT(tabla):
    try:
        connection = Connection()
        myCursor = connection.cursor()
        sql = f"""SELECT * FROM {tabla}"""
        myCursor.execute(sql)
        myResult = myCursor.fetchall()
        return [1, myResult]
    except:
        return [0]

#SELECCIÓN PACIENTES POR DOCTOR
def SELECTpatient(iddoctor):
    try:
        connection = Connection()
        myCursor = connection.cursor()
        sql = f"""SELECT * FROM patient WHERE iddoctor = {iddoctor}"""
        myCursor.execute(sql)
        myResult = myCursor.fetchall()
        return [1, myResult]
    except:
        return [0]

#SELECCIÓN CONSULTAS POR DOCTOR
def SELECTconsult(iddoctor):
    try:
        connection = Connection()
        myCursor = connection.cursor()
        sql = f"""
                SELECT * FROM consult c
                INNER JOIN patient p
                ON p.id = c.idpatient
                INNER JOIN doctor d
                ON d.id = p.iddoctor
                WHERE d.id = {iddoctor}
                """
        myCursor.execute(sql)
        myResult = myCursor.fetchall()
        return [1, myResult]
    except:
        return [0]

#REPORTES

#VISITAS POR FECHA
def ConsultsByDate(date, iddoctor):
    try:
        connection = Connection()
        myCursor = connection.cursor()
        sql = f"""
                SELECT * FROM consult c
                INNER JOIN patient p
                ON p.id = c.idpatient
                INNER JOIN doctor d
                ON d.id = p.iddoctor
                WHERE d.id = {iddoctor}
                AND c.date = {date}
            """
        myCursor.execute(sql)
        myResult = myCursor.fetchall()
        return [1, myResult]
    except:
        return [0]

#REPORTE ZODIACAL
def Zodiacal(iddoctor):
    try:
        connection = Connection()
        myCursor = connection.cursor()
        sql = f"""SELECT id, cedula, name, lastname, birthdate FROM patient WHERE iddoctor = {iddoctor}"""
        myCursor.execute(sql)
        myResult = myCursor.fetchall()
        return [1, myResult]
    except:
        return [0]

#REPORTE POR CANDITDAD DE VISITAS
def ConsultsQuantity(iddoctor):
    try:
        connection = Connection()
        myCursor = connection.cursor()
        sql = f"""SELECT id, name, (SELECT COUNT(id) FROM consult c WHERE c.idpatient = p.id) FROM patient p WHERE iddoctor = {iddoctor}"""
        myCursor.execute(sql)
        myResult = myCursor.fetchall()
        return [1, myResult]
    except:
        return [0]

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

#MÉTODOS JSON

#POR DEFECTO
@app.get("/")
def read_root():
    try:
        if (LoGGEDIN):
            return {
                "LogIn": LoGGEDIN,
                "Token": TOkEN
            }
        else:
            return {
                "LogIn": LoGGEDIN
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#REGISTRAR DOCTOR
@app.get("/signUpDoctor/{username},{email},{password}")
def _signUpDoctor(username: str, email: str, password: str):
    try:
        if (not LoGGEDIN):
            condicion = InsertSignUpDoctor(username, email, password)
            if (condicion != 0):
                return {
                    "Username": username,
                    "Email": email,
                    "Password": password
                }
            else:
                return {
                    "ERROR": "ERROR IN DATABASE"
                }
        else:
            return {
                "LogIn": LoGGEDIN,
                "ERROR": "CANT SIGN UP IF THE SESION WAS INITIALIZED"
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#INICIAR SESIÓN
@app.get("/logInDoctor/{email},{password}")
def _logInDoctor(email: str, password: str):
    try:
        global LoGGEDIN
        global TOkEN
        if (not LoGGEDIN):
            condicion = SelectLogInDoctor(email, password)
            if (condicion[0] != 0):
                if (condicion[0]):
                    LoGGEDIN = True
                    TOkEN = [binascii.b2a_hex(os.urandom(10)), condicion[1]]
                    array = [LoGGEDIN, TOkEN]
                    save(array)
                    return {
                        "LogIn": LoGGEDIN,
                        "Token": TOkEN
                    }
                else:
                    return {
                        "LogIn": LoGGEDIN,
                        "ERROR": "INCORRECT EMAIL OR PASSWORD"
                    }
            else:
                return {
                    "ERROR": "ERROR IN DATABASE"
                }
        else:
            return {
                "LogIn": LoGGEDIN
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#MODIFICAR NOMBRE DE USUARIO
@app.get("/updateDoctor/username/{username}")
def _updateDoctorUsername(username: str):
    try:
        global TOkEN
        if (LoGGEDIN):
            column = "username"
            condicion = UpdateDoctor(column, username, TOkEN[1][0])
            if (condicion != 0):
                TOkEN[1][1] = username
                array = [LoGGEDIN, TOkEN]
                save(array)
                return {
                    "NewUsername": username
                }
            else:
                return {
                    "ERROR": "ERROR IN DATABASE"
                }
        else:
            return {
                "LogIn": LoGGEDIN
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#MODIFICAR EMAIL
@app.get("/updateDoctor/email/{email}")
def _updateDoctorEmail(email: str):
    try:
        global TOkEN
        if (LoGGEDIN):
            column = "email"
            condicion = UpdateDoctor(column, email, TOkEN[1][0])
            if (condicion != 0):
                TOkEN[1][2] = email
                array = [LoGGEDIN, TOkEN]
                save(array)
                #return dict(NewEmail=email)
                return {
                    "NewEmail": email
                }
            else:
                return {
                    "ERROR": "ERROR IN DATABASE"
                }
        else:
            return {
                "LogIn": LoGGEDIN
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#MODIFICAR CONTRASEÑA
@app.get("/updateDoctor/password/{password}")
def _updateDoctorPassword(password: str):
    try:
        global TOkEN
        if (LoGGEDIN):
            column = "password"
            condicion = UpdateDoctor(column, password, TOkEN[1][0])
            if (condicion != 0):
                TOkEN[1][3] = password
                array = [LoGGEDIN, TOkEN]
                save(array)
                return {
                    "NewPassword": password
                }
            else:
                return {
                    "ERROR": "ERROR IN DATABASE"
                }
        else:
            return {
                "LogIn": LoGGEDIN
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#INSERTAR UN PACIENTE
@app.get("/insertPatient/{cedula},{image},{name},{lastname},{bloodtype},{email},{sex},{birthdate},{allergies}")
def _insertPatient(cedula: str, image: str, name: str, lastname: str, bloodtype: str, email: str, sex: str, birthdate: str, allergies: str):
    try:
        if (LoGGEDIN):
            condicion = InsertPatient(cedula, image, name, lastname, bloodtype, email, sex, birthdate, allergies, TOkEN[1][0])
            if (condicion[0] != 0):
                id = condicion[1]
                #FOR THE NEXT TIME return dict(ID=id, Cedula=cedula, Image=image, Name=name, Lastname=lastname, Bloodtype=bloodtype, Email=email, Sex=sex, Birthdate=birthdate, Allergies=allergies)
                return {
                    "ID": id,
                    "Doctor": {
                        "ID": TOkEN[1][0],
                        "Username": TOkEN[1][1],
                        "Email": TOkEN[1][2]
                    },
                    "Cedula": cedula,
                    "Image": image,
                    "Name": name,
                    "Lastname": lastname,
                    "Bloodtype": bloodtype,
                    "Email": email,
                    "Sex": sex,
                    "Birthdate": birthdate,
                    "Allergies": allergies
                }
            else:
                return {
                    "ERROR": "ERROR IN DATABASE"
                }
        else:
            return {
                "LogIn": LoGGEDIN
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#ACTUALIZAR UN PACIENTE
@app.get("/updatePatient/{id},{cedula},{image},{name},{lastname},{bloodtype},{email},{sex},{birthdate},{allergies}")
def _updatePatient(id: int, cedula: str, image: str, name: str, lastname: str, bloodtype: str, email: str, sex: str, birthdate: str, allergies: str):
    try:
        if (LoGGEDIN):
            condicion = UpdatePatient(id, cedula, image, name, lastname, bloodtype, email, sex, birthdate, allergies, TOkEN[1][0])
            if (condicion != 0):
                return {
                    "ID": id,
                    "Doctor": {
                        "ID": TOkEN[1][0],
                        "Username": TOkEN[1][1],
                        "Email": TOkEN[1][2]
                    },
                    "Cedula": cedula,
                    "Image": image,
                    "Name": name,
                    "Lastname": lastname,
                    "Bloodtype": bloodtype,
                    "Email": email,
                    "Sex": sex,
                    "Birthdate": birthdate,
                    "Allergies": allergies
                }
            else:
                return {
                    "ERROR": "ERROR IN DATABASE"
                }
        else:
            return {
                "LogIn": LoGGEDIN
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#ELIMINAR UN PACIENTE
@app.get("/deletePatient/{id}")
def _deletePatient(id: int):
    try:
        if (LoGGEDIN):
            condicion = DeletePatient(id)
            if (condicion != 0):
                return {
                    "DeletedPatientID": id
                }
            else:
                return {
                    "ERROR": "ERROR IN DATABASE"
                }
        else:
            return {
                "LogIn": LoGGEDIN
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#SELECCIONAR UN PACIENTE
@app.get("/selectPatient/{id}")
def _selectPatient(id: int):
    try:
        if (LoGGEDIN):
            condicion = SelectPatient(id, TOkEN[1][0])
            if (condicion[0] != 0):
                array = condicion[1]
                return {
                    "ID": array[0],
                    "Doctor": {
                        "ID": array[1],
                        "Username": TOkEN[1][1],
                        "Email": TOkEN[1][2]
                    },
                    "Cedula": array[2],
                    "Image": array[3],
                    "Name": array[4],
                    "Lastname": array[5],
                    "Bloodtype": array[6],
                    "Email": array[7],
                    "Sex": array[8],
                    "Birthdate": array[9],
                    "Allergies": array[10]
                }
            else:
                return {
                    "ERROR": "ERROR IN DATABASE"
                }
        else:
            return {
                "LogIn": LoGGEDIN
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#SELECCIONAR TODOS LOS PACIENTES DE UN DOCTOR
@app.get("/selectPatient")
def _selectPatient():
    try:
        global ASaP
        condicion = SELECTpatient(TOkEN[1][0])
        if (condicion[0] != 0):
            ASaP = int(0)
            dictionary = {}
            array = condicion[1]
            for k in array:
                dictionary.update({
                    f"Patient{ASaP}": {
                        "ID": k[0],
                        "Doctor": {
                            "ID": k[1]
                        },
                        "Cedula": k[2],
                        "Image": k[3],
                        "Name": k[4],
                        "Lastname": k[5],
                        "Bloodtype": k[6],
                        "Email": k[7],
                        "Sex": k[8],
                        "Birthdate": k[9],
                        "Allergies": k[10]
                    }
                })
                ASaP += 1
            return {
                "Patients": dictionary
            }
        else:
            return {
                "ERROR": "ERROR IN DATABASE"
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#SELECCIONAR LOS NOMBRES DE TODOS LOS PACIENTES (PARA COMBOBOX)
@app.get("/selectPatientsName")
def _selectPatientsName():
    try:
        global ASaP
        if (LoGGEDIN):
            condicion = SelectPatientsName(TOkEN[1][0])
            if (condicion[0] != 0):
                dictionary = {}
                array = condicion[1]
                ASaP = int(0)
                for k in array:
                    k = str(k)
                    dictionary.update({f"Name{ASaP}": k[2:(len(k) - 3)]})
                    ASaP += 1
                return dictionary
            else:
                return {
                    "ERROR": "ERROR IN DATABASE"
                }
        else:
            return {
                "LogIn": LoGGEDIN
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#INSERTAR UNA CONSULTA
@app.get("/insertConsult/{namepatient},{date},{consultreason},{securitynumber},{amount},{diagnosis},{note},{image}")
def _insertConsult(namepatient: str, date: str, consultreason: str, securitynumber: str, amount: float, diagnosis: str, note: str, image: str):
    try:
        if (LoGGEDIN):
            condicionID = SearchPatientID(namepatient, TOkEN[1][0])
            if (condicionID[0] != 0):
                idpatient = condicionID[1]
                condicion = InsertConsult(idpatient, date, consultreason, securitynumber, amount, diagnosis, note, image)
                if (condicion[0] != 0):
                    id = condicion[1]
                    return {
                        "ID": id,
                        "Patient": {
                            "ID": idpatient,
                            "Name": namepatient
                        },
                        "Date": date,
                        "ConsultReason": consultreason,
                        "SecurityNumber": securitynumber,
                        "Amount": amount,
                        "Diagnosis": diagnosis,
                        "Note": note,
                        "Image": image
                    }
                else:
                    return {
                        "ERROR": "ERROR IN DATABASE"
                    }
            else:
                return {
                    "ERROR": "ERROR IN DATABASE"
                }
        else:
            return {
                "LogIn": LoGGEDIN
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#ACTUALIZAR UNA CONSULTA
@app.get("/updateConsult/{id},{namepatient},{date},{consultreason},{securitynumber},{amount},{diagnosis},{note},{image}")
def _updateConsult(id: int, namepatient: str, date: str, consultreason: str, securitynumber: str, amount: float, diagnosis: str, note: str, image: str):
    try:
        if (LoGGEDIN):
            condicionID = SearchPatientID(namepatient, TOkEN[1][0])
            if (condicionID[0] != 0):
                idpatient = condicionID[1]
                condicion = UpdateConsult(id, idpatient, date, consultreason, securitynumber, amount, diagnosis, note, image)
                if (condicion != 0):
                    return {
                        "ID": id,
                        "Patient": {
                            "ID": idpatient,
                            "Name": namepatient
                        },
                        "Date": date,
                        "ConsultReason": consultreason,
                        "SecurityNumber": securitynumber,
                        "Amount": amount,
                        "Diagnosis": diagnosis,
                        "Note": note,
                        "Image": image
                    }
                else:
                    return {
                        "ERROR": "ERROR IN DATABASE"
                    }
            else:
                return {
                    "ERROR": "ERROR IN DATABASE"
                }
        else:
            return {
                "LogIn": LoGGEDIN
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#ELIMINAR UNA CONSULTA
@app.get("/deleteConsult/{id}")
def _deleteConsult(id: int):
    try:
        if (LoGGEDIN):
            condicion = DeleteConsult(id)
            if (condicion != 0):
                return {
                    "DeletedConsultID": id
                }
            else:
                return {
                    "ERROR": "ERROR IN DATABASE"
                }
        else:
            return {
                "LogIn": LoGGEDIN
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#SELECCIONAR UNA CONSULTA
@app.get("/selectConsult/{id}")
def _selectConsult(id: int):
    try:
        if (LoGGEDIN):
            condicion = SelectConsult(id, TOkEN[1][0])
            if (condicion[0] != 0):
                array = condicion[1]
                return {
                    "ID": array[0],
                    "Patient": {
                        "ID": array[1]
                    },
                    "Date": array[2],
                    "ConsultReason": array[3],
                    "SecurityNumber": array[4],
                    "Amount": array[5],
                    "Diagnosis": array[6],
                    "Note": array[7],
                    "Image": array[8]
                }
            else:
                return {
                    "ERROR": "ERROR IN DATABASE"
                }
        else:
            return {
                "LogIn": LoGGEDIN
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#SELECCIONAR TODAS LAS CONSULTAS DE LOS PACIENTES DE UN DOCTOR
@app.get("/selectConsult")
def _selectConsult():
    try:
        global ASaP
        condicion = SELECTconsult(TOkEN[1][0])
        if (condicion[0] != 0):
            ASaP = int(0)
            dictionary = {}
            array = condicion[1]
            for k in array:
                dictionary.update({
                    f"Consult{ASaP}": {
                        "ID": k[0],
                        "Patient": {
                            "ID": k[1]
                        },
                        "Date": k[2],
                        "ConsultReason": k[3],
                        "SecurityNumber": k[4],
                        "Amount": k[5],
                        "Diagnosis": k[6],
                        "Note": k[7],
                        "Image": k[8]
                    }
                })
                ASaP += 1
            return {
                "Consults": dictionary
            }
        else:
            return {
                "ERROR": "ERROR IN DATABASE"
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#CONSULTAS POR FECHA
@app.get("/consultsByDate/{date}")
def _consultsByDate(date: str):
    try:
        global ASaP
        if (LoGGEDIN):
            condicion = ConsultsByDate(date, TOkEN[1][0])
            if (condicion[0] != 0):
                ASaP = int(0)
                dictionary = {}
                array = condicion[1]
                for k in array:
                    dictionary.update({
                        f"Consult{ASaP}": {
                            "ID": k[0],
                            "Patient": {
                                "ID": k[1]
                            },
                            "Date": k[2],
                            "ConsultReason": k[3],
                            "SecurityNumber": k[4],
                            "Amount": k[5],
                            "Diagnosis": k[6],
                            "Note": k[7],
                            "Image": k[8]
                        }
                    })
                    ASaP += 1
                return {
                    "Consults": dictionary
                }
            else:
                return {
                    "ERROR": "ERROR IN DATABASE"
                }
        else:
            return {
                "LogIn": LoGGEDIN
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#REPORTE ZODIACAL
@app.get("/zodiacal")
def _zodiacal():
    try:
        global ASaP
        if (LoGGEDIN):
            condicion = Zodiacal(TOkEN[1][0])
            if (condicion[0] != 0):
                ASaP = int(0)
                dictionary = {}
                array = condicion[1]
                for k in array:
                    date = str(k[4])
                    zodiacalsign = getZodiacalSign(date)
                    dictionary.update({
                        f"Patient{ASaP}": {
                            "ID": k[0],
                            "Cedula": k[1],
                            "Name": k[2],
                            "Lastname": k[3],
                            "Birthdate": date,
                            "ZodiacalSign": zodiacalsign
                        }
                    })
                    ASaP += 1
                return {
                    "Patients": dictionary
                }
            else:
                return {
                    "ERROR": "ERROR IN DATABASE"
                }
        else:
            return {
                "LogIn": LoGGEDIN
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#REPORTE DE PACIENTES CON CANTIDAD DE VISITAS
@app.get("/consultsQuantity")
def _consultsQuantity():
    try:
        global ASaP
        if (LoGGEDIN):
            condicion = ConsultsQuantity(TOkEN[1][0])
            if (condicion[0] != 0):
                ASaP = int(0)
                dictionary = {}
                array = condicion[1]
                for k in array:
                    dictionary.update({
                        f"Patient{ASaP}": {
                            "ID": k[0],
                            "Name": k[1],
                            "ConsultsQuantity": k[2]
                        }
                    })
                    ASaP += 1
                return {
                    "Patients": dictionary
                }
            else:
                return {
                    "ERROR": "ERROR IN DATABASE"
                }
        else:
            return {
                "LogIn": LoGGEDIN
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#SELECCIONAR TABLA DOCTOR
@app.get("/doctor")
def _doctor():
    try:
        global ASaP
        condicion = SELECT("doctor")
        if (condicion[0] != 0):
            ASaP = int(0)
            dictionary = {}
            array = condicion[1]
            for k in array:
                dictionary.update({
                    f"Doctor{ASaP}": {
                        "ID": k[0],
                        "Username": k[1],
                        "Email": k[2],
                        "Password": k[3]
                    }
                })
                ASaP += 1
            return {
                "Doctors": dictionary
            }
        else:
            return {
                "ERROR": "ERROR IN DATABASE"
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#SELECCIONAR TABLA PACIENTE
@app.get("/patient")
def _patient():
    try:
        global ASaP
        condicion = SELECT("patient")
        if (condicion[0] != 0):
            ASaP = int(0)
            dictionary = {}
            array = condicion[1]
            for k in array:
                dictionary.update({
                    f"Patients{ASaP}": {
                        "ID": k[0],
                        "Doctor": {
                            "ID": k[1]
                        },
                        "Cedula": k[2],
                        "Image": k[3],
                        "Name": k[4],
                        "Lastname": k[5],
                        "Bloodtype": k[6],
                        "Email": k[7],
                        "Sex": k[8],
                        "Birthdate": k[9],
                        "Allergies": k[10]
                    }
                })
                ASaP += 1
            return {
                "Patients": dictionary
            }
        else:
            return {
                "ERROR": "ERROR IN DATABASE"
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#SELECCIONAR TABLA CONSULTA
@app.get("/consult")
def _consult():
    try:
        global ASaP
        condicion = SELECT("consult")
        if (condicion[0] != 0):
            ASaP = int(0)
            dictionary = {}
            array = condicion[1]
            for k in array:
                dictionary.update({
                    f"Consult{ASaP}": {
                        "ID": k[0],
                        "Patient": {
                            "ID": k[1]
                        },
                        "Date": k[2],
                        "ConsultReason": k[3],
                        "SecurityNumber": k[4],
                        "Amount": k[5],
                        "Diagnosis": k[6],
                        "Note": k[7],
                        "Image": k[8]
                    }
                })
                ASaP += 1
            return {
                "Consults": dictionary
            }
        else:
            return {
                "ERROR": "ERROR IN DATABASE"
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }

#CERRAR SESIÓN
@app.get("/logOut")
def _logOut():
    try:
        global LoGGEDIN
        global TOkEN
        if (LoGGEDIN):
            LoGGEDIN = False
            TOkEN = None
            array = [LoGGEDIN, TOkEN]
            save(array)
            return {
                "LogOut": True
            }
        else:
            return {
                "LogIn": LoGGEDIN
            }
    except:
        return {
            "ERROR": "FASTAPI ERROR"
        }